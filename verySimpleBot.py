import mouse
import detectImage 
from time import sleep
import numpy as np
import pyautogui 

baniteValsPath = "/Users/kunaalsharma/Desktop/bot/Mining/Banite/Normal Rock/vals.txt"
miningIconPath = "/Users/kunaalsharma/Desktop/bot/Mining/logo.png"
familiarIconPath = "/Users/kunaalsharma/Desktop/bot/Resources/familiar.png"

'''
Sleeps for a random amount of time.
'''
def sleepRandom():
	sleepDuration = -1
	while sleepDuration < 0:
		sleepDuration = np.random.normal(10,6)
	if sleepDuration < 1:
		print("Random long sleep.")
		sleepDuration = -1
		while sleepDuration < 0:
			sleepDuration = np.random.normal(60,40)

	print(f"Sleeping {sleepDuration} seconds")
	sleep(sleepDuration)

'''
Finds Banite Ore on the screen, and clicks on it. 
Extremely computationally expensive.
'''
def clickOnBanite():
	print("Searching for target")
	x, y  = detectImage.getScreenLocation(baniteValsPath,detectImage.BOX_SIZE_SMALL,detectImage.IMAGE_FULL,N=3)
	x = x//4
	y = y//4
	print(f"Found target at {x},{y}")
	mouse.move(x,y,detectImage.BOX_SIZE_SMALL//4)
	pyautogui.click()
	print(f"Clicked")

'''
Checks on the screen for the mining icon.
'''
def iconPresent(icon):
	loc = pyautogui.locateOnScreen(icon)
	if loc==None:
		return False
	return True

'''
Logs out by clicking on the x icon.
'''
def logout():
	logoutX = 13
	logoutY = 36
	pyautogui.moveTo(logoutX,logoutY)
	pyautogui.click()

'''
Checks the current XP
'''
def checkXP():
	x,y = pyautogui.locateCenterOnScreen(miningIconPath)
	mouse.move(x//4,y//4,10) #error size
	sleepDuration = -1
	while sleepDuration < 0:
		sleepDuration = np.random.normal(0,0.9)
	sleep(sleepDuration)
	mouse.moveCenter()


'''
Runs an extremely simple mining bot.
'''
def runBot():
	count = 0
	while True:
		sleepRandom()
		clickOnBanite()
		if int(np.random.uniform(0,10))==0:
			checkXP()
		mouse.moveCenter()
		if not iconPresent(miningIconPath):
			print(f"Click failed. Logging out after {count} iterations.")
			logout()
			return

		count += 1


if __name__ == "__main__":
	runBot()



