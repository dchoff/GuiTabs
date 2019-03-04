from os import listdir
from os.path import isfile, join
import csv, numpy as np

### 
# Looks through each .wav file and names the notes that are being played in that file according to our convention
###
for fi in listdir("./Data/2496stereo/") :
    if isfile("./Data/2496stereo/" + fi):
        first_note = fi[15:17]
        if("." in fi[17:19]):
            sec_note = ""
        elif "b" in fi[17:19]:
            sec_note = fi[17:20]
        else:
            sec_note = fi[17:19]
        # print(first_note, sec_note)

###
# Looks through each CSV and generates tuples (time, average frequency)
# time = Starting time of the average frequency within our given range
# average frequency = average frequency that crepe detected within a given bound
###
for fi in listdir("./Data/2496stereoAnalysis/"):
    print(fi)
    with open("./Data/2496stereoAnalysis/" + fi) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        notes_detected = []
        freq_range_detected = []
        frequencies_detected = []
        timestamp_ranges = []
        timestamps = []
        print("For",fi)
        for row in csv_reader:
            # Print Column Titles
            if line_count == 0:
                line_count += 1
            # Set Initial values on first line of values
            elif line_count == 1:
                prev_note_freq = row[1]
                prev_note_timestamp = row[0]
                frequencies_detected.append(float(prev_note_freq))
                line_count += 1
            # Capture 20Hz differences as different notes for rest of values
            else:
                curr_conf = float(row[2])
                curr_freq = row[1]
                curr_time = row[0]
                if curr_conf <= 0.6:
                    if(frequencies_detected):
                        freq_range_detected.append(frequencies_detected)
                        timestamp_ranges.append(curr_time)
                    frequencies_detected = []
                    continue
                if np.absolute(float(curr_freq) - float(prev_note_freq)) > 20:
                    prev_note_freq = curr_freq
                    if(frequencies_detected):
                        freq_range_detected.append(frequencies_detected)
                        timestamp_ranges.append(curr_time)
                    frequencies_detected = []
                else: 
                    frequencies_detected.append(float(curr_freq))
                line_count += 1
        # if we're at the end:
        # freq_range_detected.append(frequencies_detected)
        for freq_range in freq_range_detected:
            notes_detected.append("{0:.2f}".format(np.mean(freq_range)))
        note_time_ranges = zip(timestamp_ranges,notes_detected)
        print(list(note_time_ranges))
