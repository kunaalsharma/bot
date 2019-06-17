import utils
import pyautogui

import numpy as np

from time import sleep
from time import time

divInterfacePath = "/Users/kunaalsharma/Desktop/bot/Fletching/Interface/Fletch Interface.png"

ENERGY_KEY = '5'

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
	sleep(2)
	count = 0
	divLoc = utils.Location()
	start = time()
	while True:
		succ = performAction(makeKeyPressAction(ENERGY_KEY), makeSuccess(divLoc, divInterfacePath, False))
		if not succ:
			print(f"Failed on iteration {count}")
			return
		sleep(1)
		succ = performAction(makeKeyPressAction('space'), makeSuccess(divLoc, divInterfacePath, True))
		if not succ:
			print(f"Failed on iteration {count}")
			return
		count += 1
		sleepDuration = -1
		while sleepDuration < 0:
			sleepDuration = np.random.normal(15, 1)
		print(f"Sleeping {sleepDuration} seconds")
		sleep(sleepDuration)
		if time() - start > 3600 * 8:
			print("Finished running, quitting after 8 hours.")
			return 

if __name__ == "__main__":
	runBot()