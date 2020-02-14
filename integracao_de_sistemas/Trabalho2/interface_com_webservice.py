# Author: gabri
# File: interface_com_webservice
# Date: 04/09/2019
# Made with PyCharm

# Standard Library
import sys
import threading
import time
from queue import Queue

# Third party modules
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, Qt
import requests

# Local application imports
from main_window import Ui_MainWindow


# Classe para fazer requisicoes GET
class HttpGetter:
    def __init__(self, url, process_name):
        self.url = url
        self.process_name = process_name
        self.get_response = None

    def get(self):
        response = requests.get(self.url)
        self.get_response = str(response.text)
        print('\n{} -> GET:\nStatus: {}\nResponse: {}\n'.format(
            self.process_name, response.status_code, self.get_response), end='')
        return self.get_response


# Classe para fazer requisicoes PUT
class HttpPutter:
    def __init__(self, url, process_name):
        self.url = url
        self.process_name = process_name

    def put(self, data):
        response = requests.put(self.url, data=data)
        print('\n{} -> PUT:\nStatus: {}\nData: {}'.format(
                self.process_name, response.status_code, data))


# Derivacao da classe HttpGetter, eh adicionado a funcao run com o objetivo
# ela seja rodada em uma thread, executando GET requests de 1 em 1 segundo.
class TimedHttpGetter(HttpGetter):
    def __init__(self, *args, operation_delay=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.operation_delay = operation_delay
        self.can_run = True
    
    def reset(self):
        self.can_run = True
    
    def run(self):
        while self.can_run:
            self.get()
            time.sleep(self.operation_delay)
    
    def stop(self):
        self.can_run = False


# Derivacao da classe TimedHttpGetter, inclui uma variavel do tipo evento,
# que indica a confirmacao de que o Arduino esta offline. No caso de enviar
# um comando de desligar ao Arduino, nao basta que ele seja enviado, mas que
# tambem o microcontrolador confirme que recebeu a resposta e a executou.
class EventTimedHttpGetter(TimedHttpGetter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = threading.Event()

    def get(self):
        super().get()
        if isinstance(self.get_response, str):
            if self.get_response == 'OFF':
                self.event.set()
            else:
                self.event.clear()


class WorkerQueue:
    sentinel = object()

    def __init__(self, max_workers=0):
        self.queue = Queue(maxsize=max_workers)

    def add_work(self, work, *args, **kwargs):
        self.queue.put((work, args, kwargs))

    def finish_works(self):
        self.queue.put(self.sentinel)

    def run(self):
        while True:
            try:
                # Bloqueia ate ter item na fila para dar 'get()'
                item = self.queue.get()
                if item is self.sentinel:
                    return
                work, args, kwargs = item
                work(*args, **kwargs)
            finally:
                # Importante para o caso de multithreading para quando der
                # join na fila
                self.queue.task_done()


# Janela da interface grafica
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.system_on = False

        # Aplicacao http do PC
        self.host = "http://200.135.72.64"
        self.port = 8080
        self.application_path = "/webservice/dados"
        self.get_distance_path = "/get_dist"
        self.put_distance_threshold_path = "/put_dist_limite"
        self.get_led_state_path = "/get_status_led"
        self.put_program_state_path = "/put_status_prog"
        self.get_arduino_state_path = "/get_status_arduino"

        # Cria os objetos para fazer as requisicoes
        self.distance_getter = TimedHttpGetter(
            self.host + ':' + str(self.port) + self.application_path +
            self.get_distance_path, "Distance Getter")
        self.led_state_getter = TimedHttpGetter(
            self.host + ':' + str(self.port) + self.application_path +
            self.get_led_state_path, "Led State Getter")
        self.program_state_putter = HttpPutter(
            self.host + ':' + str(self.port) + self.application_path +
            self.put_program_state_path, "Program State Putter")
        self.arduino_state_getter = EventTimedHttpGetter(
            self.host + ':' + str(self.port) + self.application_path +
            self.get_arduino_state_path, "Arduino State Getter")
        self.distance_threshold_putter = HttpPutter(
            self.host + ':' + str(self.port) + self.application_path +
            self.put_distance_threshold_path, "Distance Threshold Putter")

        # Cria as filas de trabalho que farao as requisicoes PUT
        self.distance_threshold_putter_queue = WorkerQueue()
        self.program_state_putter_queue = WorkerQueue()
        self.create_request_threads()

        # Configuracao do elementoes da interface grafica
        self.timer = QTimer()
        self.ui.slider_dist_led.sliderReleased.connect(
            self.slider_dist_led_released)
        self.ui.slider_dist_led.valueChanged.connect(
            self.slider_dist_led_value_changed)
        self.ui.start_button.clicked.connect(self.start_button_pressed)
        self.ui.stop_button.clicked.connect(self.stop_button_pressed)
        self.timer.timeout.connect(
            self.dist_sensor_value_changed)
        self.timer.timeout.connect(
            self.led_state_value_changed)
        self.ui.slider_dist_led.setDisabled(True)

    def create_request_threads(self):
        # Cria threads relacionadas com cada uma das cinco funcoes. Duas
        # funcionam com filas de trabalho, e tres funcionam com loops
        # temporizados
        self.distance_getter_thread = threading.Thread(
            target=self.distance_getter.run)
        self.led_state_getter_thread = threading.Thread(
            target=self.led_state_getter.run)
        self.arduino_state_getter_thread = threading.Thread(
            target=self.arduino_state_getter.run)
        self.distance_threshold_putter_queue_thread = threading.Thread(
            target=self.distance_threshold_putter_queue.run)
        self.program_state_putter_queue_thread = threading.Thread(
            target=self.program_state_putter_queue.run)

    def start_program(self):
        if not self.system_on:
            print('\nSistema Iniciado\n', end='')
            self.create_request_threads()
            self.ui.slider_dist_led.setEnabled(True)
            self.program_state_putter_queue.add_work(
                self.program_state_putter.put, 'ON')
            self.distance_getter_thread.start()
            self.led_state_getter_thread.start()
            self.arduino_state_getter_thread.start()
            self.distance_threshold_putter_queue_thread.start()
            self.program_state_putter_queue_thread.start()
            self.timer.start(1000)
            self.system_on = True

    def stop_program(self):
        if self.system_on:
            print('\nParando sistema . . .\n', end='')
            self.ui.slider_dist_led.setDisabled(True)
            self.program_state_putter_queue.add_work(
                self.program_state_putter.put, 'OFF')

            # Para as filas
            self.program_state_putter_queue.finish_works()
            self.distance_threshold_putter_queue.finish_works()

            # Envia o comando de parada para os "requesters"
            self.distance_getter.stop()
            self.led_state_getter.stop()

            # Espera as threads terminarem
            self.distance_getter_thread.join()
            self.led_state_getter_thread.join()
            self.distance_threshold_putter_queue_thread.join()
            self.led_state_getter.reset()
            self.distance_getter.reset()

            # Espera cinco segundos para o arduino confirmar que esta offline,
            # caso contrario mostra uma mensagem de erro
            if not self.arduino_state_getter.event.wait(timeout=5.0):
                print('\nErro: sem resposta do arduino!\n', end='')
            else:
                print('\nArduino parou.\n', end='')

            # Envia comando de parada para os "requesters" restantes
            self.arduino_state_getter.stop()
            self.timer.stop()
            self.program_state_putter_queue_thread.join()
            self.arduino_state_getter_thread.join()
            self.arduino_state_getter.reset()

            print('\nSistema Parado\n', end='')
            self.system_on = False

    def closeEvent(self, event):
        self.stop_program()
        event.accept()

    # Slots
    def slider_dist_led_released(self):
        self.distance_threshold_putter_queue.add_work(
            self.distance_threshold_putter.put,
            str(self.ui.slider_dist_led.value()))

    def slider_dist_led_value_changed(self):
        self.ui.label_dist_led.setText(
            str(self.ui.slider_dist_led.value()) + ' cm')

    def stop_button_pressed(self):
        self.stop_program()

    def start_button_pressed(self):
        self.start_program()

    def dist_sensor_value_changed(self):
        self.ui.label_dist_sensor.setText(
            self.distance_getter.get_response + ' cm')

    def led_state_value_changed(self):
        self.ui.label_led_state.setText(self.led_state_getter.get_response)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
