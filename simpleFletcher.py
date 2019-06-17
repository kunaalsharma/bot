import detectImage
import mouse
import utils
import pyautogui

import numpy as np

from time import sleep
from time import time
from PIL import Image

size = detectImage.BOX_SIZE_SMALL
code = detectImage.IMAGE_FULL

bankInterfacePath = "/Users/kunaalsharma/Desktop/bot/Fletching/Interface/Bank Interface.png"
fletchInterfacePath = "/Users/kunaalsharma/Desktop/bot/Fletching/Interface/Fletch Interface.png"

LOG_KEY = '5'
PRESET_KEY = '2'

chestLocs = []

def findBank():
	global chestLocs
	print("Searching for bank")
	rawPoints = detectImage.getNLocations("Fletching/Bank Images/vals.txt", size, code, N = 5)
	cleanPoints = []

	for x, y in rawPoints:
		cleanPoints.append((x//4, y//4))

	chestLocs = cleanPoints
	print("Found bank")
	return

def initialize():
	findBank()

def performAction(action, success):
	action()
	sleep(1)
	if success():
		print("Success")
		return True

	for _ in range(10): #reperform action and hope for success
		if not success():
			action()
			sleep(1)
		else:
			print("Success")
			return True
	print("Failure")
	return False

def openBankAction():
	ind = float('inf')
	while ind >= len(chestLocs):
		ind = np.random.geometric(0.2)
	x , y = chestLocs[ind]

	mouse.move(x, y, 50, teleportRandom = True)
	pyautogui.click()

def makeKeyPressAction(key):
	def keyPressAction():
		utils.spamPress(key)

	return keyPressAction

def makeSuccess(loc, target, negative):
	def success():
		present = utils.checkLocation(loc, target)
		print(f"{present} at {loc.getLoc()}")
		return not present if negative else present
	return success

def runBot():
	initialize()
	sleep(2)
	count = 0
	start = time()
	bankLoc = utils.Location()
	fletchLoc = utils.Location()
	while True:
		if time() - start > 8 * 3600:
			print("Final quit")
			return
		print("Opening bank")
		succ = performAction(openBankAction, makeSuccess(bankLoc, bankInterfacePath, False)) 
		if not succ:
			print(f"Failed on iteration {count}")
			return
		sleep(1)
		print("Withdrawing logs")
		succ = performAction(makeKeyPressAction(PRESET_KEY), makeSuccess(bankLoc, bankInterfacePath, True))
		if not succ:
			print(f"Failed on iteration {count}")
			return
		sleep(1)
		print("Opening fletching interface")
		succ = performAction(makeKeyPressAction(LOG_KEY), makeSuccess(fletchLoc, fletchInterfacePath, False))
		if not succ:
			print(f"Failed on iteration {count}")
			return
		sleep(1)
		print("Starting fletching")
		succ = performAction(makeKeyPressAction('space'), makeSuccess(fletchLoc, fletchInterfacePath, True))
		if not succ:
			print(f"Failed on iteration {count}")
			return

		count += 1
		sleepDuration = -1
		while sleepDuration < 0:
			sleepDuration = np.random.normal(55, 4)
		print(f"Sleeping {sleepDuration} seconds")
		sleep(sleepDuration)

if __name__ == "__main__":
	runBot()