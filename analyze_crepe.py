from os import listdir
from os.path import isfile, join
import csv, numpy as np, crepe as crp, librosa

'''
Takes a CSV Crepe output's filename, and potentially start_times for beats. 
Goes through the CSV and captures frequencies within 10Hz of eachother whom have
a confidence of 60% or higher. Finds the duration during which these frequencies occur,
and maps that duration to the mean frequency in that duration.

Inputs:
--filename: A filename of a Crepe CSV with columns Time [float], Frequency [float], and
            Confidence [float]
--onsets: Contains potential beat onsets to start from in the Crepe file

Output:
Three parallel arrays that can be used to calculate durattions of a pitch and the note that pitch
    approximates 
--frequency_ranges
A Tuple in the form ()
'''
def readCrepe(filename, onsets=[]):
    with open("./Data/2496stereoAnalysis/" + filename + '.f0.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        notes_detected = []
        freq_range_detected = []
        frequencies_detected = [] 
        timestamp_ranges = []
        end_time = 0.0
        conf_counter = 0
        # print(filename)
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
                    # Band-Aid?
                    # conf_counter += 1
                    # if(conf_counter >= 10):
                    #     conf_counter = 0
                    #     end_time = curr_time
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
        pitches_and_times = zip(timestamp_ranges,notes_detected)
        # if not list(note_time_ranges):
        #     print("Crepe wasn't confident about anything in this file.")
        return list(pitches_and_times)
                    
A2_B2 = readCrepe('Guitar.mf.sulA.C4E4')
print("a2, b2:",A2_B2)

def findDurationsPitches(pitches_and_times):
    notes = []
    durations = []
    for pair in pitches_and_times:
        pitch = pair[1]
        times = pair[0]
        print ('times', times)
        start_time = times[0]
        end_time = times[1]
        print('s', start_time)
        print('e',end_time)
        duration = end_time - start_time
        print('d', duration)
        print('pitch', pitch)
        note = librosa.hz_to_note(float(pitch))
        durations.append(duration)
        notes.append(note)
    return durations, notes

durations, notes = findDurationsPitches(A2_B2)
print((durations,notes))