import numpy as np
import wave
import struct
import math
#Teams can add other helper functions
#which can be added here
array = [130.81, 146.83, 164.81, 174.61, 196.00, 220.0, 246.94,
             261.63, 293.66, 329.63, 349.23, 392.0, 440.0, 493.88,
             1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53,
             2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07,
             4186.01, 4698.63, 5274.04, 5587.65, 6271.93, 7040.00, 7902.13]

notes = ['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3',
             'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
             'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
             'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
             'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8']


split=[]
sampling_freq = 44100   # Sampling frequency of audio signal
win_size=882            # Window Size is 882 frames
def matching_freq(freq):
    Identified_Notes=[]
    for i in freq:
        idx = (np.abs(array-i)).argmin()
        Identified_Notes.append(notes[idx])
    return Identified_Notes


def rms(sound,count,win_size):           #Function to calculate the rms Value
    sum=0
    for j in range(count,count+win_size):
            sum=sum+(sound[j]*sound[j])
    sum=sum/win_size
    result=math.sqrt(sum)
    
    return result

def f_equ(sound,start,end):              #Function to calculate Frequency
    start1=start*win_size
    end1=(end+1)*win_size
    split=sound[start1:end1] 
    ftransform=np.fft.fft(split)
    ft=np.argsort(ftransform)
    rev=ft[::-1]
    l=(end-start+1)*win_size
    f=(rev[0]*sampling_freq)/l
    if(f>10000):
        f=44100-f
    print f
    return f
    

def play(sound_file):
    file_length=sound_file.getnframes()      
    sound= np.zeros(file_length)        
    for i in range(file_length):
        data = sound_file.readframes(1)
        data= struct.unpack("<h",data)
        sound[i]=int(data[0])
    sound= np.divide(sound, float(2**15))

    #Detecting silence
    
    T_hld=0.0319366455078125                # Threshold value 
    re=np.zeros(file_length/win_size)       # Array to store the result of silence
    for i in range(file_length/win_size):
        count=i*win_size
        Rms=rms(sound,count,win_size) 
        if(Rms<T_hld):
            re[i]=0
        else:
            re[i]=1
            
    #Detecting location of notes
            
    ST=0               # Start point of frame
    freq=[]            # List to store frequencies
    f_ct=0             # Index for frequency list
    FL=re[0]           # Flag registere for detecting location
    for i in range(file_length/win_size):
        if(re[i]!=FL):
            FL=re[i]
            end=i-1
            if(re[i-1]==1):
                freq.append(f_equ(sound,ST,end))
                f_ct=f_ct+1
                ST=end+1
            else:
                ST=end+1
                
    Identified=matching_freq(freq)
    return Identified

############################## Read Audio File #############################

if __name__ == "__main__":
    #code for checking output for single audio file
    #sound_file = wave.open('Audio_files/Audio_2.wav', 'r')
    #Identified_Notes = play(sound_file)
    #print "Notes = ", Identified_Notes

    #code for checking output for all images
    Identified_Notes_list = []
    for file_number in range(1,7):
        file_name = "Task_1.1_Audio_files/Audio_"+str(file_number)+".wav"      #specif file path here
        sound_file = wave.open(file_name)
        Identified_Notes = play(sound_file)
        
        print Identified_Notes
    
