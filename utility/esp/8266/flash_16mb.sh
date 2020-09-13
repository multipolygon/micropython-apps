PORT=$(ls /dev/tty.usbserial-* | head -n1)
pipenv run python -m esptool --port $PORT --baud 115200 write_flash 0xffc000 ./utility/esp/8266/firmware/esp_init_data_default.bin
pipenv run python -m esptool --port $PORT --baud 115200 write_flash -fm dio -fs 16MB 0x00000 `ls ./utility/esp/8266/firmware/esp8266* | tail -1`
