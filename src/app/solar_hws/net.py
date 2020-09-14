from home_assistant.mqtt import MQTT
from home_assistant.climate import Climate, MODE_OFF, MODES
from home_assistant.sensors.temperature import Temperature
from status_led import StatusLED
from micropython import schedule
import wifi
from . import config
import secrets

try:
    from uid import UID
except:
    UID = 'Main'

class Net():
    def __init__(self, state):
        self.update_on = ('mode', 'tank_target_temp', 'tank_temp', 'pump', 'solar_temp')
        led = StatusLED(gpio=config.LED_GPIO)
        wifi.connect(secrets.WIFI_NAME, secrets.WIFI_PASSWORD, led=led)
        self.mqtt = MQTT(config.NAME, secrets, uid=UID, led=led)

        ctl = self.mqtt.add('Controller', Climate, key = 'ctl', max = config.TANK_MAX_TEMP)
        temp = self.mqtt.add('Solar', Temperature, key = 'sol')

        def set_mode(msg):
            if msg in MODES:
                state.set(mode = msg)

        self.mqtt.sub(ctl.mode_cmd_tpc(), set_mode)

        def set_targ(msg):
            state.set(tank_target_temp = round(float(msg)))

        self.mqtt.sub(ctl.targ_cmd_tpc(), set_targ)

        state.mqtt = self.mqtt.try_pub_cfg()

        self._sched = False

        def pub_state(_):
            self._sched = False
            ctl.set_mode(state.mode)
            ctl.set_targ(state.tank_target_temp)
            ctl.set_temp(state.tank_temp)
            ctl.set_actn('off' if state.mode == MODE_OFF else ('heating' if state.pump else 'idle'))
            temp.set_state(state.solar_temp)
            state.set(
                mqtt = self.mqtt.pub_state()
            )

        self.pub_state = pub_state

    def update(self, state, changed):
        if not self._sched:
            self._sched = True
            schedule(self.pub_state, 0)

    def start(self, state):
        self.pub_state(0)

    def run(self, state):
        self.mqtt.wait()

    def stop(self, state):
        self.mqtt.discon()
