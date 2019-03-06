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
--start_times: Contains potential beat onsets to start from in the Crepe file

Output:
Three parallel arrays that can be used to calculate durattions of a pitch and the note that pitch
    approximates 
--frequency_ranges
A Tuple in the form ()
'''
def readCrepe(filename, start_times=[]):
    with open("./Data/2496stereoAnalysis/" + filename + ".csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0

        frequency_ranges = []
        frequencies_detected = []
        start_times = []
        end_times = []
        # Go through entire file and group based on what we read from CSV file, no onsets used
        if (not start_times):
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                elif line_count == 1:
                    start_time = float(row[0])
                    prev_freq = float(row[1])
                    frequencies_detected.append(prev_freq)
                    start_times.append(start_time)
                else:
                    curr_time = float(row[0])
                    curr_freq = float(row[1])
                    confidence = float(row[2])
                    if not frequencies_detected:
                        start_times.append(curr_time)
                    if confidence >= 0.6 and np.absolute(curr_freq - prev_freq) < 10:
                        frequencies_detected.append(curr_freq)
                        line_count+=1
                    elif confidence < 0.6 and np.absolute(curr_freq - prev_freq) < 10:
                        line_count +=1
                        continue
                    elif confidence >= 0.6:
                        end_times.append(curr_time)
                        if(frequencies_detected):
                            frequency_ranges.append(frequencies_detected)
                        frequencies_detected = []
                        line_count+=1
                    # if frequencies_detected and len(frequency_ranges) == len(start_times):
                    #     start_times.append(curr_time)
            
            return frequency_ranges, start_times, end_times
            notes = []
            durations = []
            for freq_range in frequency_ranges:
                notes.append("{0:.2f}".format(np.mean(freq_range)))
            print(len(start_times),len(end_times))
            for i in range(len(start_times)):
                durations.append(end_times[i] - start_times[i])
            print((durations,notes))
                    
readCrepe('Guitar.ff.sulA.A2B2.f0', start_times=[])

def findDurationsPitches(frequency_ranges, start_times, end_times)