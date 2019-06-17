import mouse
import detectImage 
import numpy as np
import pyautogui 
import utils

from time import sleep
from time import time

animicaPath = "Mining/Dark Animica/vals.txt"
miningIconPath = "Mining/logo.png"
porterIconPath = "Mining/porter.png"

FAMILIAR_KEY = 't'
JUJU_KEY = '1'
PRAYER_KEY = '4'
BOX_KEY = '3'
PORTER_KEY = 'e'

locs = []

'''
Sleeps for a random amount of time.
'''
def sleepRandom():
	sleepDuration = -1
	while sleepDuration < 0:
		sleepDuration = np.random.normal(30,6)
	if sleepDuration < 5:
		print("Random long sleep.")
		sleepDuration = -1
		while sleepDuration < 0:
			sleepDuration = np.random.normal(60,40)

	print(f"Sleeping {sleepDuration} seconds")
	sleep(sleepDuration)

'''
Finds Animica Ore on the screen, and clicks on it. 
'''
def clickOnAnimica():
	if locs == []: 
		rawLocs = detectImage.getNLocations(animicaPath, 50, 5)
		for loc in rawLocs:
			 x , y = loc
			 locs.append((x//4, y//4))

	ind = np.random.geometric(0.1)
	while ind >= len(locs):
		ind = np.random.geometric(0.1)
	
	x , y = locs[ind]
	print(f"Clicking at {x},{y}")
	mouse.move(x, y, 50, teleportRandom=True)
	pyautogui.click()

'''
Checks on the screen for the mining icon.
'''
def iconPresent(icon):
	loc = pyautogui.locateOnScreen(icon)
	if loc==None:
		return False
	return True

'''
Checks the current XP
'''
def checkXP():
	x,y = pyautogui.locateCenterOnScreen(miningIconPath)
	mouse.move(x//4,y//4,10) #error size
	sleepDuration = -1
	while sleepDuration < 0:
		sleepDuration = np.random.normal(1,0.9)
	sleep(sleepDuration)
	mouse.moveCenter()


'''
Does hourly tasks
'''
def doHourly(): #This method needs to be reworked!!!
	utils.spamPress(JUJU_KEY, conservative = True)

'''
Equips a sign of the porter if one is present, and 
stores ore in the mining box
'''
def clearInventory():
	if iconPresent(porterIconPath):
		print("Equipped sign of porter")
		utils.spamPress(PORTER_KEY)
	sleep(np.random.normal(2,0.1))
	utils.spamPress(BOX_KEY)
	print("Filled ore box")
	return 

'''
Runs an extremely simple mining bot.
'''
def runBot():
	pyautogui.FAILSAFE = False  # this is just annoying
	count = 0
	lastTime = 0
	
	while True:
		sleepRandom()
		clickOnAnimica()
		sleepDuration = -1
		while sleepDuration < 0:
			sleepDuration = np.random.normal(0.4,0.3)
		sleep(sleepDuration)
		mouse.moveCenter()

		#is inventory full?
		if not iconPresent(miningIconPath):
			clearInventory()
			sleep(2)
			if not iconPresent(miningIconPath):
				print(f"Bot failed. Quitting after {count} iterations.")
				return

		# check XP
		if int(np.random.uniform(0,10))==0:
			checkXP()

		# do hourlies
		if time() - lastTime > 3500:
			doHourly()
			lastTime = time()

		count += 1

if __name__ == "__main__":
	runBot()