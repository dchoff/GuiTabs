from os import listdir
from os.path import isfile, join
import csv, numpy as np, librosa

## Turns timestamps from an audiofile into Pitches
# take filename and arr of timestamps
# returns: array of pitches at those timestamps
def timestamp_to_pitch(filename, beats):
    pitches = []
    print(beats)
    with open('./2496stereo/' + filename[:-3] + "f0.csv") as csv_file:
        
    # with open('./2496stereoAnalysis/Guitar.mf.sulA.C4E4.f0.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                curr_time = float(row[0])
                for beat in beats:
                    if curr_time == beat:
                        pitches.append(float(row[1]))
                line_count += 1
        # print(pitches)
        notes = librosa.hz_to_note(pitches)
    return notes, pitches
