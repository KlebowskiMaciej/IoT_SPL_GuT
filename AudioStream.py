import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import time,wave,datetime,os,csv
import struct
import InitParam
import AudioAnalyze

class AudioStream(object):
    def __init__(self):
        self.pause = False
        self.param = InitParam.InitParam()

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format = self.param.pyaudio_format,
                    rate = self.param.SAMP_RATE,
                    channels = self.param.CHANNEL,
                    input_device_index = self.param.DEV_INDEX,
                    input = True,
                    frames_per_buffer=self.param.CHUNK)
        
        self.Processing()
        
        
    def Processing(self):
        print('stream started')
        frame_count = 0
        start_time = time.time()

        while not self.pause:
            
            #Pierwsza opcja 
            #data = self.stream.read(self.param.CHUNK)
            #data_int = struct.unpack(str(2 * self.param.CHUNK) + 'B', data)
            #data_np = np.array(data_int, dtype='b')[::2] + 128
            #print(data_np);
            #data_vec=1
            
            #Druga opcja
            stream_data = self.stream.read(self.param.CHUNK,exception_on_overflow=False) # grab data frames from buffer
            data = np.frombuffer(stream_data,dtype=self.param.buffer_format) # grab the data array
            AudioAnalyze.AudioAnalyze(stream_data)   # analysis section
            
        else:
            self.fr = frame_count / (time.time() - start_time)
            print('average frame rate = {:.0f} FPS'.format(self.fr))
            self.exit_app()
    
    def exit_app(self):
        print('stream closed')
        self.p.close(self.stream)

    def onClick(self, event):
        self.pasue = True
        
    
    
