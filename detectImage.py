from pyautogui import screenshot
from PIL import Image

import computeHistogram, math

BOX_SIZE_SMALL = 50
BOX_SIZE_MED = 100
BOX_SIZE_LARGE = 150
BOX_SIZE_XLARGE = 200

IMAGE_TOP_LEFT = 0
IMAGE_TOP_RIGHT = 1
IMAGE_BOTTOM_RIGHT = 2
IMAGE_BOTTOM_LEFT = 3
IMAGE_CENTER = 4
IMAGE_FULL = 5

BANK_VALS_PATH = "/Users/kunaalsharma/Desktop/bot/Bank Images/vals.txt"
INTERFACE_VALS_PATH = "/Users/kunaalsharma/Desktop/bot/Interface/vals.txt"

def getScreenLocation(path,size,code):
	image = screenshot()
	image = cropImage(image,code)
	images, imagesMap = tesselateScreenshot(image,size)
	imageHistograms = computeHistogram.computeAllVals(images)
	targetHistograms = computeHistogram.read(path)

	locationIndex = getMinHistogram(imageHistograms,targetHistograms)
	x,y = imagesMap[locationIndex]
	markImage(x,y,size,image)
	return (x,y,image.crop(x,y,x+size,y+size))

def checkScreenLocation(region,image):
	screen = screenshot(region)
	screenData = screen.getdata()
	imageData = image.getData()

	for i in range(len(screenData)):
		if screenData[i][0] != imageData[i][0]: #Only need to check one channel
			return False

	return True

def tesselateScreenshot(screenshot,size):
	images = []
	imagesMap = {}
	imageIndex = 0
	xLim = screenshot.size[0]
	yLim = screenshot.size[1]
	for x in range(0,xLim,size):
		for y in range(0,yLim,size):
			images.append(screenshot.crop((x,y,x+size,y+size)))
			imagesMap[imageIndex] = (x,y)
			imageIndex +=1
	imagesMap[-1] = (-1,-1)
	return images, imagesMap

def getMinHistogram(imageHistograms,targetHistograms):
	minValue = math.inf 
	minIndex = -1
	for i in range(len(imageHistograms)):
		for target in targetHistograms:
			val = computeHistogram.compare(imageHistograms[i],target)
			if val<minValue:
				minValue = val
				minIndex = i
	if minValue > 1.0:
		return -1
	return minIndex

def markImage(xT,yT,size,image):
	newImage = []
	imageData = reshape(image)

	for y in range(image.size[1]):
		for x in range(image.size[0]):
			if (x >= xT) and (x < xT + size) and (y == yT):
				newImage.append((255,0,0,255))
			elif (x >= xT) and (x < xT + size) and (y == yT + size):
				newImage.append((255,0,0,255))
			elif (y >= yT) and (y < yT + size) and (x == xT):
				newImage.append((255,0,0,255))
			elif (y >= yT) and (y < yT + size) and (x == xT + size):
				newImage.append((255,0,0,255))
			else:
				newImage.append(imageData[y][x])

	markedImage = Image.new(image.mode,image.size)
	markedImage.putdata(newImage)
	markedImage.show()
	return

def reshape(image):
	imageData = image.getdata()
	xLim = image.size[0]
	yLim = image.size[1]
	reshapedData = []
	currentPixel = 0

	for y in range(0,yLim):
		currentCol = []
		for x in range(0,xLim):
			currentCol.append(imageData[currentPixel])
			currentPixel+=1
		reshapedData.append(currentCol)

	return reshapedData

def cropImage(image,code):
	x = image.size[0] // 2
	y = image.size[1] // 2

	if code==IMAGE_FULL:
		return image
	elif code==IMAGE_CENTER:
		x = image.size[0] // 4
		y = image.size[1] // 4
		return image.crop((x,y,x + 2*x,y + 2*y))
	elif code==IMAGE_TOP_LEFT:
		return image.crop((0,0,x,y))
	elif code==IMAGE_TOP_RIGHT:
		return image.crop((x,0,x+x,y))
	elif code==IMAGE_BOTTOM_RIGHT:
		return image.crop((x,y,x+x,y+y))
	elif code==IMAGE_BOTTOM_LEFT:
		return image.crop((0,y,x,y+y))
