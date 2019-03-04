from os import listdir
from os.path import isfile, join
import csv, numpy as np, librosa

## Turns timestamps from an audiofile into Pitches
# take filename and arr of timestamps
# returns: array of pitches at those timestamps
def timestamp_to_pitch(filename, beats):
    pitches = []
    with open('./Data/2496stereo/' + filename + ".csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                curr_time = float(row[0])
                for beat in beats:
                    # print('row type: ',type(row[0]))
                    # print('beat type: ',type(beat))
                    if curr_time == beat:
                        print("??")
                        pitches.append(float(row[1]))
                line_count += 1
        x = librosa.hz_to_note(pitches)
        print(x)
    return pitches
