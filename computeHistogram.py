import os, sys, math
from PIL import Image
import numpy as np


BUCKET_SIZE = 10
OUTPUT_NAME = "vals.txt"

'''
Lists all files in a directory. Vists each file one by one and computes
the histogram values for that file using getVals(file). Saves
the output at the end using save().
'''
def runPipeline():
	imageFiles = os.listdir()
	histogramVals = []

	for image in imageFiles:
		if image == ".DS_Store":
			continue
		histogramVals.append(getVals(Image.open(image,"r")))

	save(histogramVals, OUTPUT_NAME)
	return

'''
Computes the histogram values for each image provided, using the
getVals function
'''
def computeAllVals(images):
	allHistograms = []
	for image in images:
		allHistograms.append(getVals(image))
	return allHistograms

'''
Computes the normalized histogram values of an image. Uses BUCKET_SIZE and returns values as a list
'''
def getVals(image):
	rHistogram = [0] * int(255/BUCKET_SIZE)
	gHistogram = [0] * int(255/BUCKET_SIZE)
	bHistogram = [0] * int(255/BUCKET_SIZE)
	allPixels = image.getdata()

	for pixel in allPixels:
		r = pixel[0]
		g = pixel[1]
		b = pixel[2]
		for i in range(0,len(rHistogram)):
			if r < BUCKET_SIZE * i:
				rHistogram[i-1]+=1
				break
			elif i==len(rHistogram)-1:
				rHistogram[len(rHistogram)-1]+=1
		for i in range(0,len(gHistogram)):
			if r < BUCKET_SIZE * i:
				gHistogram[i-1]+=1
				break
			elif i==len(gHistogram)-1:
				gHistogram[len(gHistogram)-1]+=1
		for i in range(0,len(bHistogram)):
			if r < BUCKET_SIZE * i:
				bHistogram[i-1]+=1
				break
			elif i==len(bHistogram)-1:
				bHistogram[len(bHistogram)-1]+=1

	numPixels = len(allPixels)
	rHistogram = [i/numPixels for i in rHistogram]
	gHistogram = [i/numPixels for i in gHistogram]
	bHistogram = [i/numPixels for i in bHistogram]
	return [rHistogram,gHistogram,bHistogram]

'''
Saves the provided histogram data as a text file specified by 
the name argument
'''
def save(allImageData, name):
	outputFile = open(name,"w+")

	for imageData in allImageData:
		for histogram in imageData:
			outputFile.write(str(histogram))
		outputFile.write("\n")

	outputFile.close()

'''
Helper function that removes leading and trailing brackets from a line
'''
def bracketStrip(line):
	if line[0][0] == '[':
		line[0] = line[0][1:]
	if line[-1][-2:] == ']\n':
		line[-1] = line[-1][:-2]
	return line
'''
Reads in histogram data saved by save. Returns a list of histograms
'''
def read(name):
	inputFile = open(name,"r+")
	allHistograms = []

	for line in inputFile:
		line = line.split("][")
		line = bracketStrip(line)
		line = [[float(bucket) for bucket in hist.split(",")] for hist in line]
		allHistograms.append(line)

	return allHistograms
'''
Computes the similarity of two image histograms. Returns the difference
as an integer
'''
def compare(a,b):
	difference = 0

	for i in range(0,len(a)):
		for j in range(0,len(a[i])):
			difference += abs(a[i][j] - b[i][j])
	return difference
'''
Changes to the appropriate directory and calls computeHistogramValues()
'''
if __name__=="__main__":
	if (len(sys.argv)<2):
		print("Missing path argument")
		quit()
	os.chdir(sys.argv[1])
	runPipeline()
