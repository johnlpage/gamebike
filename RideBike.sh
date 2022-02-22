while true
do
  cd /home/pi/gamebike
  /home/pi/gamebike/RideBike.py 2>&1 | tee  /tmp/control.log| sudo tee /dev/console
done

