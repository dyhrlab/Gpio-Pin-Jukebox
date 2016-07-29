#!/.virtualenvs/cv/bin python


from os import listdir
import subprocess
from time import sleep

import RPi.GPIO as GPIO, time, os

Debug = 1, True
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GREEN_LED = 17
RED_LED = 4

GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
def RCtime (RCpin):
	reading = 0
	GPIO.setup(RCpin, GPIO.OUT)
	GPIO.setup(RCpin, GPIO.LOW)
	time.sleep(1)

	GPIO.setup(RCpin, GPIO.IN)
	
	while (GPIO.input(RCpin) == GPIO.LOW):
		reading +=1
	return reading

mp3_files = [ f for f in listdir('.') if f[-4:] == '.mp3']

if not (len(mp3_files) > 0):
    print "Ohhh NO!-No mp3 file found!"

print '---Yay- availble mp3 files---'
print mp3_files
print '---Press button 1 to select song, press button 2 to start song, decrease light over photo sensor to terminate song, press button 3 to terminate lights---'

index = 0
while True:
    if (GPIO.input(23) == False):
       	index  += 1
	if index >= len(mp3_files):
	    index = 0
	print "---" + mp3_files[index] + "---"
    if  (GPIO.input(24) == False):
	 subprocess.Popen(['mpg123', mp3_files[index]])
	 GPIO.output(GREEN_LED, True)
	 GPIO.output(RED_LED, False)
	 print '--- Now Playing ' +mp3_files[index] + ' ---'
	 print '---Press Button 3 to turn off the lights ---'
    if (RCtime(18) >= 500):
        subprocess.call(['killall', 'mpg123'])
	GPIO.output(RED_LED, True)
        GPIO.output(GREEN_LED, False)
        print '--- Cleared all existing MP3s. ---'
    if (GPIO.input(25) == False):
        GPIO.output(GREEN_LED, False)
        GPIO.output(RED_LED, False)
        subprocess.call(['killall', 'mpg123'])
        print '--- Exiting program. ---'
        break

    sleep(0.05);
