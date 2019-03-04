import librosa
import numpy as np

def main(name):
	fp = '2496stereo/'
	aud, sr = librosa.load(fp + name)
	bt = findBeats(aud, sr)
	round_bt = np.round(bt, decimals=2)
	##pitches = timestamp_to_pitch(name, bt)
	##note_names = librosa.hz_to_note(pitches)
	return round_bt

def findBeats(aud, sr):
	tempo, bt = librosa.beat.beat_track(aud, sr=sr, units='time', trim=False)
	return bt