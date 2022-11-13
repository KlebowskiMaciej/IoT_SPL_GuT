import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import time,wave,datetime,os,csv
import struct
import InitParam
import audioop
import AudioStream
import InitParam
import numpy as np
import AudioAnalyze
from math import log10
from threading import Timer

class AudioStream(object):
    
    global dataGraber
    dataGraber = []
    
    def __init__(self):
        self.pause = False
        self.param = InitParam.InitParam()
        
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format = self.param.pyaudio_format,
                    rate = self.param.SAMP_RATE,
                    channels = self.param.CHANNEL,
                    #input_device_index = self.param.DEV_INDEX,
                    input = True,
                    frames_per_buffer=self.param.CHUNK)
        
        self.Processing()
        
        
    def Processing(self):
        print('stream started')
        frame_count = 0
        seconds=30
        start_time = time.time()
        
        while not self.pause:
            
            try:
                stream_data = self.stream.read(self.param.CHUNK,exception_on_overflow=False) # grab data frames from buffer
                current_time=time.time()
            except IOError as e:
                error_count+=1
                print("(%d) Error %s"& (error_count,e))
            else:
                #dataGraber.append(self.audioProcess(stream_data))# analysis section
                elapsed_time=current_time-start_time
                print(self.audioProcess(stream_data))
            
         #   if elapsed_time > seconds:
           #     start_time=time.time()
           #     print(sum(dataGraber)/len(dataGraber))
          #      print(max(dataGraber))
          #      print(min(dataGraber))   
          #      dataGraber.clear()
                
        
           
            #Pierwsza opcja 
            #data = self.stream.read(self.param.CHUNK)
            #data_int = struct.unpack(str(2 * self.param.CHUNK) + 'B', data)
            #data_np = np.array(data_int, dtype='b')[::2] + 128
            #print(data_np);
            #data_vec=1
            
            #Druga opcja
            #data = np.frombuffer(stream_data,dtype=self.param.buffer_format) # grab the data array
            
            
        else:
            self.fr = frame_count / (time.time() - start_time)
            print('average frame rate = {:.0f} FPS'.format(self.fr))
            self.exit_app()
    
    def exit_app(self):
        print('stream closed')
        self.p.close(self.stream)

    def onClick(self, event):
        self.pasue = True
    
    
    def fft(self,data_vec):
        data_vec = data_vec*np.hanning(len(data_vec)) # hanning window
        N_fft = len(data_vec) # length of fft
        freq_vec = (float(self.param.SAMP_RATE)*np.arange(0,int(N_fft/2)))/N_fft # fft frequency vector
        fft_data_raw = np.abs(np.fft.fft(data_vec)) # calculate FFT
        fft_data = fft_data_raw[0:int(N_fft/2)]/float(N_fft) # FFT amplitude scaling
        fft_data[1:] = 2.0*fft_data[1:] # single-sided FFT amplitude doubling
        return freq_vec,fft_data   
    
    def audioloopp(self,data):
        audioop.rms(data,2)
        d=np.frombuffer(data,np.int16)
        np.sqrt((d*d).sum()/(1.*len(d)))
        d = np.frombuffer(data, np.int16).astype(np.float)
        return(np.sqrt((d*d).sum()/len(d)))
    
    def audioProcess(self,data_vec):
        db = 20 * log10(self.audioloopp(data_vec))
        return db
