from time import sleep
from pyautogui import locateOnScreen
from pyautogui import click
from pyautogui import press
from PIL import Image
from random import randint

import detectImage
import mouse

chestPath = "/Users/kunaalsharma/Desktop/bot/Fletching/Bank Images/vals.txt"

bankImagePath = "/Users/kunaalsharma/Desktop/bot/Fletching/Interface/Bank Interface.png"
bankImage = Image.open(bankImagePath,"r")
bankRegion = None

fletchImagePath = "/Users/kunaalsharma/Desktop/bot/Fletching/Interface/Fletch Interface.png"
fletchImage = Image.open(fletchImagePath,"r")
fletchRegion = None

FLETCH_DURATION = 50 #seconds
LOGOUT_CHANCE = 1/200
NUM_TRIES = 3

chestX = None
chestY = None


def init():
	for i in range(NUM_TRIES):
		chestX,chestY = getScreenLocation(chestPath,
			detectImage.BOX_SIZE_SMALL,
			detectImage.IMAGE_FULL)
		if chestX != -1 and chestY != -1:
			break

	if chestX == -1 or chestY == -1:
		return False

'''
Checks three times to see if the bank interface is open. Returns 
True if the interface is open, False otherwise
'''
def waitForBankOpen():
	if bankRegion == None:
		for i in range(NUM_TRIES):
			bankRegion = locateOnScreen(bankImagePath)
		return bankRegion!=None

	for i in range(NUM_TRIES):
		sleep(0.5)
		success = detectImage.checkScreenLocation(bankRegion,bankImage)
		if success:
			return True
	return False

'''
Checks three times to see if the fletching interface is open. Returns
True if the interface is open, False otherwise
'''
def waitForFletchOpen():
	if fletchRegion == None:
		for i in range(NUM_TRIES):
			fletchRegion = locateOnScreen(fletchImagePath)
		return fletchRegion!=None

	for i in range(NUM_TRIES):
		sleep(0.5)
		success = detectImage.checkScreenLocation(fletchRegion,fletchImage)
		if success:
			return True
	return False

'''
Logs out of Runescape 
'''
def logout();
	pass

'''
Randomly returns True if the bot should stop running, False otherwise.
Stopping condition for while loop which runs bot
'''
def botDoneRunning():
	if (randint(0,int(1/LOGOUT_CHANCE))==0):
		return True
	return False

'''
Clicks somewhere in the square that the bank was detected in 
'''
def openBank():
	mouse.moveTo(chestX,chestY,detectImage.BOX_SIZE_SMALL)
	click()
'''
Presses the key 2
'''
def press2():
	press("2")

def runAction(action,successAction):
	for i in range(NUM_TRIES):
		action()
		if successAction():
			return True
	return False

def runFletchingBot():
	if !init():
		logout()
		return

	while(!botDoneRunning()):
		if !runAction(openBank,waitForBankOpen):
			break
		if !runAction(press2,waitForBankClose):
			break
		if !runAction(press2,waitForFletchOpen):
			break
		if !runAction()





	logout()
	return 








