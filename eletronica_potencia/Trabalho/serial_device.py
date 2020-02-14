# Author: gabri
# File: serial_device
# Date: 17/11/2019
# Made with PyCharm

# Standard Library

# Third party modules
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

# Local application imports


class SerialDevice(QSerialPort):
    """
    Classe responsavel pela comunicacao serial com o arduino, bem como pelo
    envio dos comandos de ligar e desligar a esteira.
    """
    def __init__(self, debug=False, vendor_id=6790, product_id=29987):
        super().__init__()
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.available_to_use = False
        self.online = False
        self.debug = debug

        if self.debug:
            print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - -")
            print("Numero de portas seriais conectadas ao PC:"
                  f" {len(QSerialPortInfo().availablePorts())}")

        for port_info in QSerialPortInfo().availablePorts():
            if self.debug:
                print(f"Dispositivo: {port_info.portName}:")
                print(f"ID Vendedor: {port_info.vendorIdentifier()}")
                print(f"ID Produto: {port_info.productIdentifier()}\n")
            if (port_info.hasVendorIdentifier() and
                    port_info.hasProductIdentifier()):
                if (port_info.vendorIdentifier() == vendor_id and
                        port_info.productIdentifier() == product_id):
                    self.port_name = port_info.portName()
                    self.available_to_use = True

        if self.available_to_use:
            if self.debug:
                print("Dispositivo serial encontrado com sucesso!")
            self.setPortName(self.port_name)
            self.setBaudRate(QSerialPort.Baud9600, QSerialPort.AllDirections)
            self.setDataBits(QSerialPort.Data8)
            self.setParity(QSerialPort.NoParity)
            self.setStopBits(QSerialPort.OneStop)
            self.setFlowControl(QSerialPort.NoFlowControl)

            # Apos todas as configuracoes tenta conectar com a porta serial
            if self.open(QSerialPort.ReadWrite):
                if self.debug:
                    print("Comunicacao estabelecida com sucesso!")
                self.online = True
            else:
                if self.debug:
                    print("Erro: nao foi possivel estabelecer a comunicacao")
        else:
            if self.debug:
                print("Aviso: dispositivo nao encontrado.")
                print("- - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

