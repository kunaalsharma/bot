from pyautogui import click
from pyautogui import press

from random import randint

from time import sleep 

'''
Literally the simplest possible bot
'''

'''
Click, 
wait 0.5 seconds,
press 2,
wait 0.5 seconds,
press 2,
wait 0.5 seconds,
press space,
wait 50 seconds
'''
sleep(2)
while(True):
	click()
	sleep(1+randint(0,1000)/1000 - 0.5)
	press("2")
	sleep(1+randint(0,1000)/1000 - 0.5)
	press("2")
	sleep(1+randint(0,1000)/1000 - 0.5)
	press(" ")
	press(" ")
	press(" ")
	sleep(70+randint(0,25)-12.5)
