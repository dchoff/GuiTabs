import librosa
import timestamp_to_pitch as tp
import read_csv_onsets as rco
import numpy as np	
import crepe as crp
from scipy.io import wavfile
from timeit import default_timer as timer
import sys, os
sys.path.insert(0, "../bin")
from sys import argv
import guitab as gt

def generateCSV(filepath):
	os.system("crepe " + filepath)

def findBeats(aud, sr):
	tempo, bt = librosa.beat.beat_track(aud, sr=sr, units='time', trim=False)
	return bt
	
def normalize(aud):
	max = np.max(aud)
	div = np.full(max)

	norm_aud = np.divide(aud,div)
	return norm_aud

def main(name):
	start = timer()

	fp = '2496stereo/'
	aud, sr = librosa.load(fp + name)
	bt = findBeats(aud, sr)
	round_bt = np.round(bt, decimals=2)
	#run crepe
	generateCSV(fp + name)
	duration, notes = rco.fileOnsetsToDurationsNotes(name[:-4])
	#call lilypond
	gt.write_mscx_file(name[:-4], notes)
	gt.generate_pdf(name[:-4])
	print(notes, round_bt)
	end = timer()
	print(end - start, "seconds") # Time in seconds, e.g. 5.38091952400282	
	return True
	
if __name__ == "__main__":
	main(argv[1])

