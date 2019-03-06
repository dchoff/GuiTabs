import librosa
import timestamp_to_pitch as tp
import numpy as np	

def findBeats(aud, sr):
	tempo, bt = librosa.beat.beat_track(aud, sr=sr, units='time', trim=False)
	return bt

def main(name):
	fp = '2496stereo/'
	aud, sr = librosa.load(fp + name)
	bt = findBeats(aud, sr)
	round_bt = np.round(bt, decimals=2)
	notes, pitches = tp.timestamp_to_pitch(name, round_bt)
	##note_names = librosa.hz_to_note(pitches)
	return notes

notes = main("Guitar.ff.sulA.C4E4.wav")
print(notes)