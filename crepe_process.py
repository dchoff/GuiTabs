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

# def findDurationsNotes()
for fi in listdir("./Data/2496stereoAnalysis/"):
    with open("./Data/2496stereoAnalysis/" + fi) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        notes_detected = []
        freq_range_detected = []
        frequencies_detected = [] 
        timestamp_ranges = []
        timestamps = []
        end_time = 0.0
        print(fi)
        for row in csv_reader:
            # Print Column Titles
            if line_count == 0:
                line_count += 1
            # Capture 20Hz differences as different notes for rest of values
            else:
                curr_conf = float(row[2])
                curr_freq = float(row[1])
                curr_time = float(row[0])
                # Set Initial values on first line of values
                if not frequencies_detected and curr_conf >= 0.60:
                    ref_note_freq = curr_freq
                    start_time = curr_time
                    frequencies_detected.append(curr_freq)
                    line_count += 1
                    continue

                if curr_conf < 0.6 or np.isnan(curr_conf):
                    continue
                
                if np.absolute(curr_freq - ref_note_freq) < 10:
                    end_time = curr_time
                    frequencies_detected.append(curr_freq)
                else:
                    if frequencies_detected:
                        freq_range_detected.append(frequencies_detected)
                        timestamp_ranges.append((start_time, end_time)) 
                    frequencies_detected = []
                line_count += 1
        if frequencies_detected:
            freq_range_detected.append(frequencies_detected)
            timestamp_ranges.append((start_time,end_time))
        for note in freq_range_detected:
            # print(note)
            notes_detected.append("{0:.2f}".format(np.mean(note)))
        note_time_ranges = zip(timestamp_ranges,notes_detected)
        # if not list(note_time_ranges):
        #     print("Crepe wasn't confident about anything in this file.")
        print(list(note_time_ranges))

