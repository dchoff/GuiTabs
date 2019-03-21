from os import listdir
from os.path import isfile, join
import csv, numpy as np, librosa

def fileOnsetsToDurationsNotes(filename, onsets=[]):
    pitches_times = readNotesCSV(filename, onsets)
    durations, notes = findDurationsNotes(pitches_times)
    return durations, notes

def readNotesCSV(filename, onsets=[]):
    with open("./2496stereo/" + filename + '.f0.csv') as csv_file:
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
                curr_time = float(row[0])
                curr_freq = float(row[1])
                curr_conf = float(row[2])
                is_onset = next((True for onset in onsets if onset == curr_time), False)

                #Assign pitches from given start to end times
                if onsets != []:
                    for onset in onsets:
                        if onset == curr_time:
                            start_time = onset
                            frequencies_detected.append(curr_freq)
                            ref_note_freq = curr_freq
                            continue

                    if frequencies_detected:
                        if np.absolute(curr_freq - ref_note_freq) < 10:
                            end_time = curr_time
                            frequencies_detected.append(curr_freq)
                        else:
                            freq_range_detected.append(frequencies_detected)
                            timestamp_ranges.append((start_time, end_time)) 
                            frequencies_detected = []
                    line_count += 1
                    
                #Run through the entire CSV and find areas of high confidence to assign pitches
                else:
                    # Starting
                    if not frequencies_detected: 
                        if not curr_conf >= 0.60:
                            continue
                        conf_counter = 0
                        frequencies_detected.append(curr_freq)
                        ref_note_freq = curr_freq
                        start_time = curr_time
                        line_count += 1
                        continue
                    if curr_conf >= 0.60:
                        conf_counter = 0

                    #Handle Low Confidence
                    if curr_conf < 0.6 or np.isnan(curr_conf):
                        if conf_counter < 100:
                            conf_counter += 1
                            line_count += 1
                        else:
                            conf_counter = 0
                            timestamp_ranges.append((start_time,end_time))
                            freq_range_detected.append(frequencies_detected)
                            frequencies_detected = []
                            line_count += 1
                        continue

                    #When frequencies have large enough differences in Hz
                    if np.absolute(curr_freq - ref_note_freq) < 10:
                        end_time = curr_time
                        frequencies_detected.append(curr_freq)
                    else:
                        if frequencies_detected:
                            freq_range_detected.append(frequencies_detected)
                            timestamp_ranges.append((start_time, end_time)) 
                        frequencies_detected = []
                    line_count += 1

        #Handle hanging pitches and times at the end
        if frequencies_detected:
            freq_range_detected.append(frequencies_detected)
            timestamp_ranges.append((start_time,end_time))
        
        #Format frequencies to be readable pitches
        for note in freq_range_detected:
            notes_detected.append("{0:.2f}".format(np.mean(note)))

        pitches_and_times = zip(timestamp_ranges,notes_detected)
        return list(pitches_and_times)
                    
def findDurationsNotes(pitches_and_times):
    notes = []
    durations = []
    for pair in pitches_and_times:
        pitch = pair[1]
        times = pair[0]
        start_time = times[0]
        #print(start_time, float(pitch))
        end_time = times[1]
        duration = end_time - start_time
        if float(pitch) == 0.0:
           continue
        notes, durations = elimArtifacts(float(pitch), notes, duration, durations)
    durations,notes = combineNotes(durations, notes)
    return durations, notes
           
def elimArtifacts(pitch, notes, duration, durations):
    if(pitch > 82 and pitch < 1175):
        note = librosa.hz_to_note(float(pitch))
        durations.append(round(duration,2))
        notes.append(note)
    return notes, durations
	
		   
def combineNotes(durations, notes):
    for i in range(len(notes)):
        if i == 0:
            continue
        pitch = librosa.note_to_hz(notes[i-1])
        curr_pitch = librosa.note_to_hz(notes[i])

        #If duration of the note is too short and it's about an octave off, combine it
        if durations[i-1] < 0.05 and durations[i] > 0.05:
            if np.abs((pitch * 2) - curr_pitch) > 10 or np.abs((pitch / 2) - curr_pitch) > 10:
                pitch = curr_pitch
                durations[i] = durations[i-1] + durations[i]
                notes[i] = librosa.hz_to_note(float(pitch))
                del durations[i-1]
                del notes[i-1]

        if durations[i] < 0.05 and durations[i-1] > 0.05:
            if np.abs((pitch * 2) - curr_pitch) > 10 or np.abs((pitch / 2) - curr_pitch) > 10:
                pitch = curr_pitch
                durations[i-1] = durations[i] + durations[i-1]
                notes[i] = librosa.hz_to_note(float(pitch))
                del durations[i]
                del notes[i]
        return durations, notes
