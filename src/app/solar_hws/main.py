from .config import TANK_TARGET_TEMP, RETAIN
from hub import Hub

hub = Hub(
    solar_temp = None,
    tank_temp = None,
    tank_target_temp = TANK_TARGET_TEMP,
    pump = False,
    mode = 'auto',
)

from .net import Net
internet = hub.add(Net)

from .temp import Temp
hub.add(Temp)

from .ctrl import Ctrl
hub.add(Ctrl, priority=True)

from .pump import Pump
hub.add(Pump, priority=True)

from components.retain import Retain
hub.add(Retain, RETAIN=RETAIN)

## Not enough memory on the 8266 for this:
# from .display import Display
# hub.add(Display, priority=True)

hub.run()
