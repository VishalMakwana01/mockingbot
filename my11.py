import numpy as np
import wave
import struct
import os

sampling_freq = 44100	                                                                                            # Sampling frequency of audio signal
window_size = 2205                                                                                                  # Window size for silence detection
notes=['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3',
			 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
			 'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
	         'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
    	     'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8']
rep=[2,3,4,5,6,0,1,9,10,11,12,13,7,8,16,17,18,19,20,14,15]                                                                                                                    #notes-list containing all the notes in order
                                                                                                                   
note_freq=[130.81, 146.83, 164.81, 174.61, 196.00, 220.0, 246.94,
			 261.63, 293.66, 329.63, 349.23, 392.0, 440.0, 493.88,
			 1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53,
    	     2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07,
        	 4186.01, 4698.63, 5274.04, 5587.65, 6271.93, 7040.00, 7902.13]
    #note_freq-list containing the upper limit of
    # #the frequencies respective to the note array
Identified_Notes1=[]
#it is the array storing the final notes
mapNotes=[]
k=[]#it is storing the frequncies calculated from the samples

def findNote(frequency):
    print(frequency)
    Identified_Notes=[]
    idx = (np.abs(note_freq-frequency)).argmin()
    Identified_Notes.append(notes[idx])
    print Identified_Notes

def findFrequency():
    #this function removes the repetitive values corresponding to the same note
	#and silences and gets the notes for the found frequencies 
    j=0              
    temp=1
    while(j<len(k)-4):
        if(k[j]==0):
            temp=1
        if((k[j]!=temp) & (k[j]!=0)):
            if(k[j]==k[j+1]):
                temp=k[j]
                findNote (temp)

        j=j+1

def play(sound_file):  
    file_length = sound_file.getnframes()                                                                             #finds the length of audio file

    for i in range(int(file_length/window_size)):
        data = sound_file.readframes(window_size)                                                                     #reads the data for window_size frames
        data = struct.unpack('{n}h'.format(n=window_size), data)                                                      #converts data to decimal format
        sound = np.array(data)
        w = np.fft.fft(sound)                                                                                         #finds fourier transform 
        freqs = np.fft.fftfreq(len(w))                                                                                #finds frequency with respect to data 
        idx = np.argmax(np.abs(w))                                                                                    #finds the max argument(frequency) index
        freq = freqs[idx]                                                                                             #retrieves the frequency
        k.append(abs(freq * sampling_freq))                                                                           #appends the frequency to k
    findFrequency()
         #calls findFrequency function

############################### Main Function ##############################################

if __name__ == "__main__":

    #   Instructions
    #   ------------
    #   Do not edit this function.

    # code for checking output for single audio file
    path = os.getcwd()

    file_name = path + "\Task_1.1_Audio_files\Audio_1.wav"
    audio_file = wave.open(file_name)

    play(audio_file)
    k=[]
    # code for checking output for all audio files
    x = raw_input("\n\tWant to check output for all Audio Files - Y/N: ")

    if x == 'Y':

        Detected_Note_list = []

        file_count = len(os.listdir(path + "\Task_1.1_Audio_files"))

        for file_number in range(1, file_count):

            file_name = path + "\Task_1.1_Audio_files\Audio_" + str(file_number)+".wav"
            audio_file = wave.open(file_name)
            print(str(file_number) + ": \n")
            play(audio_file)
            k=[]
            #Detected_Note_list.append(Detected_Note)

        #print("\n\tDetected Notes = " + str(Detected_Note_list))
