# MicroPython Apps

Most of the code is for the ESP8266.

This project includes a lib for registering devices with Home Assistant via the MQTT-discovery protocol.

https://www.home-assistant.io/docs/mqtt/discovery

See `src/lib/home_assistant`.

## Use

Apps for various use-cases are found in `src/app`.

Edit `src/main.py` to import the desired app.

For example:

    from app.solar_hws import main

or another example:

    from app.temp_sensor import main

## Install

### System Tools

    pip install --user pipenv

*or*

    brew install pipenv

then

    pipenv install

### Erase

    ./utility/esp/erase.sh

### Flash

    ./utility/esp/8266/flash_4mb.sh

*or*

    ./utility/esp/8266/flash_16mb.sh

### Transfer py files

    ./utility/esp/rshell.sh

Then run the rshell command:

    rsync ./src/ /pyboard/

And see if it worked:

    ls /pyboard/

### Run / Test

    repl

And hit [CTRL+D] to reboot device (which will then automatically run `main.py`).

---

## Notes

### Resources

https://github.com/espressif/esptool

https://github.com/dhylands/rshell

https://github.com/wendlers/mpfshell

http://micropython.org/webrepl/

### USB on Linux

Give user access to /dev/ttyUSB0:

    sudo usermod -a -G dialout $USER
    sudo usermod -a -G tty $USER
    sudo reboot

### Firmware Downloads

https://micropython.org/download#esp8266

https://micropython.org/download#esp32

### 16MB

Instructions from here:

https://github.com/micropython/micropython/issues/2335#issuecomment-520210822

### Output

    screen /dev/ttyUSB0 115200

To exit: `ctl-a d`

### Erasing and Flashing

If esptool is trying to connect and you get something like this:

```
esptool.py v2.7
Serial port /dev/tty.usbserial-1420
Connecting........_____....._____....._____....._____....._____....._____....._
```

...then hold down the reset button and release it to time with the first _ (underscore).


