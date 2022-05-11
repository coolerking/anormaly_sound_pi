#!/bin/sh
# crontab -e
# 0-59 * * * * /home/pi/projects/anormaly_sound_pi/anormaly_sound_pi/record.sh
export PATH=${PATH}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games:.
#source ${HOME}/env/bin/activate
cd ${HOME}/projects/anormaly_sound_pi/anormaly_sound_pi
/home/pi/env/bin/python record.py --datadir data --age 5 --sec 1 --dev_index 1 --debug True
exit $?