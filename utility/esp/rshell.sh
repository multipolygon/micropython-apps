TODAY=`date +"%Y-%m-%d"`
echo VERSION\=\"$TODAY\" > src/version.py
cd /dev
PORT=$(ls tty.usbserial-* | head -n1)
cd -
pipenv run rshell -p /dev/$PORT
