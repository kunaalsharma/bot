import pyautogui, time

from detectImage import checkScreenLocation
from detectImage import getScreenLocation
from detectImage import markImage

from pyautogui import locateOnScreen
from pyautogui import locate

from PIL import Image

bankImagePath = "/Users/kunaalsharma/Desktop/bot/Interface/Bank Interface.png"
bankImage = Image.open(bankImagePath,"r")
bankRegion = None

fletchImagePath = "/Users/kunaalsharma/Desktop/bot/Interface/Fletch Interface.png"
fletchImage = Image.open(fletchImagePath,"r")
fletchRegion = None



'''
The idea is to:
	When you don't know where the bank or the chest are, 
	use the fine grained check to get coordinates.

	Then, save those coordinates and the corresponding image.
	Then, only take screenshots of those coordinates and compare
	them against the image which is important.

		If it matches, then you're good.
		If it doesn't match, then start again.
'''

def openBank():
	pass

def pressKey():
	pass

def 


