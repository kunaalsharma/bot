import mouse
import detectImage 
import time
import numpy as np
import pyautogui 

baniteValsPath = "/Users/kunaalsharma/Desktop/bot/Mining/Banite/Normal Rock/vals.txt"

while True:
	sleepDuration = -1
	while sleepDuration < 0:
		sleepDuration = np.random.normal(5,20)
	print(f"Sleeping {sleepDuration} seconds")
	time.sleep(sleepDuration)
	print("Searching for target")
	x, y  = detectImage.getScreenLocation(baniteValsPath,detectImage.BOX_SIZE_SMALL,detectImage.IMAGE_FULL,show=False)
	x = x//4
	y = y//4
	print(f"Found target at {x},{y}")
	mouse.move(x,y,10) #10 = error box size
	pyautogui.click()
	print(f"Clicked")