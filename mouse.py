from pyautogui import moveTo
from pyautogui import position
from random import randint
from time import sleep

from PIL import Image
from detectImage import reshape
import pyautogui

def move(x,y,size):
	controlPoints = generateControlPoints(x,y)
	mousePositions = generateBezierCurve(controlPoints)


	print(controlPoints)

	for position in mousePositions:
		print(position)
		moveTo(position)
		sleep(0.5)
	return mousePositions

def generateControlPoints(xT,yT,n=6):
	x,y = (0,0) #position()
	controlPoints = [(x,y)]

	for i in range(n-2):
		xGen = randint(min(x,xT),max(x,xT))
		yGen = randint(min(y,yT),max(y,yT))
		controlPoints.append((xGen,yGen))

	controlPoints.append((xT,yT))
	return controlPoints

def generateBezierCurve(controlPoints):
	tVals = [i/100 for i in range(0,105,5)]
	mousePositions = []
	for t in tVals:
		xGen, yGen = binomial(t,controlPoints)
		mousePositions.append((xGen,yGen))
	return mousePositions

def binomial(t,controlPoints):
	n = len(controlPoints) - 1
	x = 0
	y = 0
	for i in range(n + 1):
		term = nCr(n,i) * (1-t)**(n-i) * t ** i
		x = x + term * controlPoints[i][0]
		y = y + term * controlPoints[i][1]
	return x,y

def nCr(n,r):
	return factorial(n)//(factorial(n)*factorial(n-r))

def factorial(n):
	product = 1
	for i in range(1,n+1):
		product *= i
	return product

def teleportMouseRandom():
	pass

if __name__=="__main__":
	pyautogui.FAILSAFE = False
	mousePositions = move(1000,700,1)
	#image = Image.open("/Users/kunaalsharma/Desktop/bot/Test Images/1.png")
	#marked = markMousePath(mousePositions,image)
	#marked.show()

