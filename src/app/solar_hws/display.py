from machine import I2C, Pin
from lib.esp.esp8266.wemos.d1mini import pinmap
from vendor.ssd1306 import SSD1306
from utime import sleep
import wifi

class Display():
    def __init__(self, state):
        self.update_on = ('mqtt', 'solar_temp', 'tank_temp', 'tank_target_temp', 'mode', 'pump')
        i2c = I2C(-1, Pin(pinmap.SCL), Pin(pinmap.SDA))
        self.oled = SSD1306(i2c)
        self.update(state, [])

    def update(self, state, changed):
        self.oled.rst()
        self.oled.txt(
            'WIFI:%3d' % (wifi.rssi() if wifi.is_connected() else 0)
        )
        self.oled.txt(
            'MQTT:%3s' % ('OK' if hasattr(state, 'mqtt') and state.mqtt else '--')
        )
        self.oled.txt(
            'SOLR:%3d' % state.solar_temp
        )
        self.oled.txt(
            'TANK:%3d' % state.tank_temp
        )
        self.oled.txt(
            'TARG:%3d' % state.tank_target_temp
        )
        self.oled.txt(
            '%-4s:%3s' % (state.mode.upper(), 'ON' if state.pump else 'OFF')
        )

    def stop(self, state):
        self.oled.clear()
        self.oled.power_off()
