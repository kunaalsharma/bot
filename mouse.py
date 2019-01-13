from pyautogui import moveTo
from pyautogui import position
from random import randint
from time import sleep

from PIL import Image
from detectImage import reshape
import pyautogui

MIN_DURATION = 8 #ms
X_MIN, X_MAX, Y_MIN, Y_MAX = 100,1300,100,700 #Dimensions of 1440x900 screen

'''
Generates points along a bezier curve. Moves along the bezier curve 
every 30 ms with randomly generated noise between -10 and 10 ms.
'''
def move(xT,yT,size):
	teleportMouseRandom()
	controlPoints = generateControlPoints(xT+randInt(xT,xT+size),yT+randInt(yT,yT+size))
	duration = moveDuration(xT,yT)
	mousePositions = generateBezierCurve(controlPoints,duration)
	ewma = randint(0,MIN_DURATION) - MIN_DURATION/2

	for position in mousePositions:
		sleep((ewma + MIN_DURATION)/1000)
		moveTo(position)
		ewma = 0.6 * ewma + 0.4 * (randint(0,MIN_DURATION) - MIN_DURATION/2)

'''
Generates control points for a bezier curve. Uses the starting and ending
points as the first and last control points, and randomly generates
the rest in the rectangle formed by the first and last.
'''
def generateControlPoints(xT,yT,n=4):
	x,y = position()
	controlPoints = [(x,y)]

	for i in range(n-2):
		xGen = randint(min(x,xT),max(x,xT))
		yGen = randint(min(y,yT),max(y,yT))
		controlPoints.append((xGen,yGen))

	controlPoints.append((xT,yT))
	return controlPoints

'''
Generates the mouse positions for a mouse following the bezier curve
parameterized by the given control points. Based upon the duration, will 
generate a variable number of mouse positions (each move is minimum 30ms).
'''
def generateBezierCurve(controlPoints,duration):
	sampleGranularity = 1000//(duration//MIN_DURATION)
	tVals = [i/1000 for i in range(0,1000+sampleGranularity,sampleGranularity)]
	mousePositions = []
	for t in tVals:
		xGen, yGen = binomial(t,controlPoints)
		mousePositions.append((xGen,yGen))
	return mousePositions

'''
Helper function for bezier curve calculation
'''
def binomial(t,controlPoints):
	n = len(controlPoints) - 1
	x = 0
	y = 0
	for i in range(n + 1):
		term = nCr(n,i) * (1-t)**(n-i) * t ** i
		x = x + term * controlPoints[i][0]
		y = y + term * controlPoints[i][1]
	return x,y

'''
Helper function for bezier curve calculation. nCr.
'''
def nCr(n,r):
	return factorial(n)//(factorial(r)*factorial(n-r))

'''
Helper function for bezier curve calculation. Factorial.
'''
def factorial(n):
	product = 1
	for i in range(1,n+1):
		product *= i
	return product

'''
Calculates the amount of time it should take the mouse to move 
from the current position to xT,yT. The duration is based upon 
the distance, and is the root of distance (short moves are quick, 
longer moves are slow, but the growth is not linear). Constant of 12, 
as the maximum move on a 1440x900 screen should take 500ms
'''
def moveDuration(xT,yT):
	fConstant = 12 #1693 distance should take 500 ms

	x,y = position()
	distance = ((x-xT)**2 + (y-yT)**2)**0.5
	return int(fConstant * distance**0.5)

'''
Teleports the mouse to a location chosen uniformly at random
'''
def teleportMouseRandom():
	moveTo(randInt(X_MIN,X_MAX),randInt(Y_MIN,Y_MAX))
