import utils
import pyautogui
import mouse
import numpy as np

from time import sleep
from time import time

itemPath = "/Users/kunaalsharma/Desktop/bot/Invention/logs.png"
logoPath = "/Users/kunaalsharma/Desktop/bot/Invention/logo.png"

DA_KEY = '3'

def disassemble(itemLoc, logoLoc):
	if itemLoc.isEmpty():
		newLoc = pyautogui.locateOnScreen(itemPath)
		if newLoc == None:
			return False
		print(newLoc)
		itemLoc.setLoc(newLoc)

	utils.spamPress(DA_KEY)
	sleep(1)
	x, y, size = getBox(itemLoc.getLoc())
	mouse.move(x, y, size)
	pyautogui.click()

	if logoLoc.isEmpty():
		newLoc = pyautogui.locateOnScreen(logoPath)
		if newLoc == None:
			return False
		print(newLoc)
		logoLoc.setLoc(newLoc)

	return not utils.checkLocation(logoLoc, logoPath) == None


def getBox(reg):
	x1, y1, x2, y2 = reg
	return (2*x1 + x2)//8, (2*y1 + y2)//8, min(x2, y2)//4

def runBot():
	sleep(2)
	count = 0
	start = time()
	itemLoc = utils.Location()
	logoLoc = utils.Location()
	while True:
		if time() - start > 14400:
			print("Quitting after 4 hours")
			return
		succ = False
		for _ in range(3):
			sleep(1)
			succ = disassemble(itemLoc, logoLoc)
			if succ: 
				break
		if not succ:
			print(f"Failed on iteration {count}")
			return

		count += 1
		sleepDuration = -1
		while sleepDuration < 0:
			sleepDuration = np.random.normal(72, 9)
		print(f"Sleeping {sleepDuration} seconds")
		sleep(sleepDuration)


if __name__ == "__main__":
	runBot()