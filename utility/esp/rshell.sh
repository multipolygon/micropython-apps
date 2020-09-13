cd /dev
PORT=$(ls tty.usbserial-* | head -n1)
cd -
pipenv run rshell -p /dev/$PORT
