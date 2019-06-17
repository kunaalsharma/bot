import pyautogui
import numpy as np

from PIL import Image
from time import sleep

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
def checkXP(iconPath):
	x,y = pyautogui.locateCenterOnScreen(iconPath)
	mouse.move(x//4,y//4,10) #error size
	sleepDuration = -1
	while sleepDuration < 0:
		sleepDuration = np.random.normal(1,0.9)
	sleep(sleepDuration)
	mouse.moveCenter()

'''
Spam clicks on a key
'''
def spamPress(key, conservative = False):
	mean = 0.8 if conservative else 0.4
	numPresses = np.random.geometric(mean)

	intervals = []
	low, high = 0, np.random.normal(0.5, 0.01)

	for _ in range(numPresses):
		interval = np.random.uniform(low, high)
		intervals.append(interval)
		low = interval

	for interval in intervals:
		pyautogui.press(key)
		sleep(interval)
	return

def checkLocation(loc, target):
	if loc.isEmpty():
		loc.setLoc(pyautogui.locateOnScreen(target))
		return loc.getLoc()
	else:
		return pyautogui.locate(target, pyautogui.screenshot().crop(convert(loc.getLoc())))

def convert(region):
	x1,y1,x2,y2 = region
	return (x1, y1, x2 + x1, y2 + y1)

class Location:

	def __init__(self):
		self.loc = None

	def getLoc(self):
		return self.loc

	def setLoc(self, loc):
		self.loc = loc

	def isEmpty(self):
		return self.loc == None








