from machine import Pin
from status_led import StatusLED
from . import config

led = StatusLED(gpio=config.LED_GPIO)

class Pump():
    def __init__(self, state):
        self.update_on = ('pump',)
        self.pin = Pin(config.PUMP_GPIO, mode=Pin.OUT)
        self.pin.value(config.PUMP_OFF)
        led.off()

    def update(self, state, changed):
        led.set(state.pump == config.PUMP_ON)
        led.on() if state.pump == config.PUMP_ON else status_led.off()

