import os
import random
import librosa



def getFileName(dir):
	x = os.listdir(dir)
	sz =len(x)
	rind = random.randrange(0, sz - 1)
	file = x[rind]
	return file


def dataPrep():
	file = getFileName('2496stereo')
	fp = './2496stereo/'
	aud = librosa.load(fp + file, sr=None)[0]
	return aud
