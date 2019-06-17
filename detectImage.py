from pyautogui import screenshot
from PIL import Image

import computeHistogram, math
import numpy as np
import imagehash

from sklearn.cluster import KMeans
import numpy as np

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

def getScreenLocation(path,size,code,show=False,N=3,random=True):
	image = screenshot()
	image = cropImage(image,code)
	images, imagesMap = tesselateScreenshot(image,size)
	imageHistograms = computeHistogram.computeAllVals(images)
	targetHistograms = computeHistogram.read(path)

	locationIndexes = getMinNHistograms(imageHistograms,targetHistograms,N)
	pos = []
	for ind in locationIndexes:
		pos.append(imagesMap[ind])

	if show:
		NMarkImage(pos,size,image)

	if random:
		return selectRandom(pos) #Min N histograms
	else:
		return pos[0] #Min histogram

def getNLocations(path, size, code, N=20):
	image = screenshot()
	image = cropImage(image, code)
	images, imagesMap = tesselateScreenshot(image, size)
	imageHistograms = computeHistogram.computeAllVals(images)
	targetHistograms = computeHistogram.read(path)

	locationIndexes = getMinNHistograms(imageHistograms, targetHistograms, N)
	pos = []
	for ind in locationIndexes:
		pos.append(imagesMap[ind])

	return prunePoints(pos)

def selectRandom(pos):
	ind = int(np.random.uniform(0,len(pos)))
	return pos[ind]

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

def getMinNHistograms(imageHistograms, targetHistograms, N):
	distances = []
	for index,hist in enumerate(imageHistograms):
		for target in targetHistograms:
			distances.append((index, computeHistogram.compare(hist,target)))
	distances = sorted(distances, key = lambda pair : pair[1])
	minHistograms = {}
	ret = []
	for index, _ in distances:
		if not index in minHistograms:
			minHistograms[index] = -1
			ret.append(index)
		if len(minHistograms)==N:
			break
	return ret

def shouldBeMarked(x,y,positions,size):
	for xT,yT in positions:
		if y==yT:
			if x>=xT and x < xT + size:
				return True
		elif y==yT + size:
			if x>=xT and x < xT + size:
				return True
		elif x==xT:
			if y>=yT and y < yT + size:
				return True
		elif x==xT + size:
			if y>=yT and y < yT + size:
				return True
	return False

def NMarkImage(positions,size,image):
	newImage = []
	imageData = reshape(image)

	for y in range(image.size[1]):
		for x in range(image.size[0]):
			if shouldBeMarked(x,y,positions,size):
				newImage.append((0,255,0,255))
			else:
				newImage.append(imageData[y][x])
	markedImage = Image.new(image.mode,image.size)
	markedImage.putdata(newImage)
	markedImage.show()
	return	

def prunePoints(points):

	def distance(p1, p2):
		(x1, y1), (x2, y2) = p1, p2
		return ((x1-x2)**2 + (y1-y2)**2)**0.5

	numPoints = len(points)
	distances = []
	for i in range(numPoints):
		point = points[i]
		overallDist = 0
		for j in range(numPoints):
			overallDist += distance(point, points[j])
		distances.append(overallDist/numPoints)


	means = KMeans(n_clusters = 2)
	means.fit(np.array(distances).reshape(-1,1))

	c1, c2 = [], []
	for ind, dist in enumerate(distances):
		if means.predict(dist)==0:
			c1.append(points[ind])
		else:
			c2.append(points[ind])
	if len(c1) > len(c2):
		return c1
	return c2

def markWholeImage(affinities, indMap, size, image, N=20, prune=True):

	def averagePixel(pix, col):
		return tuple([int((pix[i]+col[i])/2) for i in range(len(pix))])

	def genColor(curr):
		intensity = curr/worstAffinity
		return (255 * (1 - intensity), 20, 60, 255) 

	def genPos():
		pos = {}
		for ind in indMap:
			pos[indMap[ind]] = ind
		return pos 

	def getTopNPoints():

		def insert(lis, inds, val, valInd):
			if len(lis)==0:
				return [val], [valInd]
			for ind, cVal in enumerate(lis):
				if val < cVal:
					lis.insert(ind, val)
					inds.insert(ind, valInd)
					break
			if len(lis) < N:
				lis.insert(len(lis), val)
				inds.insert(len(lis), valInd)
			return lis[:N], inds[:N]

		best, inds = [], []
		for i, affinity in enumerate(affinities):
			best, inds = insert(best, inds, affinity, i)

		return [indMap[i] for i in inds]

	worstAffinity = max(affinities)
	colors = [genColor(affinity) for affinity in affinities]
	positions = genPos()

	imageData = reshape(image)
	newImage = []
	for y in range(image.size[1]):
		for x in range(image.size[0]):
			currRGB = imageData[y][x]
			currInd = (x - (x % size), y - (y % size))
			newImage.append(averagePixel(currRGB, colors[positions[currInd]]))

	markedImage = Image.new(image.mode,image.size)
	markedImage.putdata(newImage)
	
	points = prunePoints(getTopNPoints()) if prune else getTopNPoints()
	NMarkImage(points, size, markedImage)


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


if __name__ == "__main__":
	size = 50
	image = Image.open("/Users/kunaalsharma/Desktop/test.png")
	images, imagesMap = tesselateScreenshot(image,size)

	targets = computeHistogram.read("/Users/kunaalsharma/Desktop/bot/Mining/Dark Animica/vals.txt")
	
	def getBestAffinity(hist):
		currAffinities = []
		for target in targets:
			currAffinities.append(computeHistogram.compare(hist, target))
		return min(currAffinities)

	affinities = []
	for img in images:
		affinities.append(getBestAffinity(computeHistogram.getVals(img)))

	markWholeImage(affinities, imagesMap, size, image, N=5)




