# resistor controlado por tensao
class VoltageResistor:
    def __init__(self, resistance, voltage=0):
        self._voltage = voltage
        self.resistance = resistance
        
    
    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self._current = voltage / self._resistance

    @property
    def resistance(self):
        return self._resistance

    @resistance.setter
    def resistance(self, resistance):
        if resistance <= 0:
            raise ValueError("Resistance must be > 0.")

        self._resistance = resistance
        self._current = self._voltage / resistance

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        raise AttributeError("Can't set this attribute.")


R = VoltageResistor(100)
R.voltage = 5
print(R.current)
R.resistance = 500
print(R.current)
print(R.__dict__)
