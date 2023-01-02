import pyaudio
import numpy as np
import time
import audioop
import datetime
import GoogleSheets
import threading

class Recorder(object):

    local_data = []
    global_data = []

    CHUNK = 1024  # frames to keep in buffer between reads
    SAMP_RATE = 44100  # sample rate [Hz]
    FORMAT = pyaudio.paInt16  # 16-bit device
    CHANNEL = 1  # only read 1 channel mono 2 stereo
    DEV_INDEX = 0  # index of sound device
    PAUSE = False # variable that stops the application running
    FRAME_COUNT = 0
    SECONDS = 30  # number of seconds from which one maximum is taken
    SIZE_SEND_DATA = 10 #  total number of max to compare 

    def __init__(self):
        self.process()

    def process(self):
        
        self.set_mic()
        error_count = 0
        start_time = time.time()
        print('stream started')
        while not self.PAUSE:
            try:
                stream_data = self.stream.read(self.CHUNK, exception_on_overflow=False)  
                current_time = time.time()
            except IOError as e:
                error_count += 1
                print("({}) Error {}".format(error_count, e))
            else:
                elapsed_time = current_time - start_time  #
                self.local_data.append(self.to_dB(stream_data))
                if elapsed_time >= self.SECONDS:
                    start_time = time.time()
                    self.send_data()
                    self.local_data.clear()
        else:
            fr = self.FRAME_COUNT / (time.time() - start_time)
            print("average frame rate = {:.0f} FPS".format(fr))

    def to_dB(self, data_vec):
        reading = audioop.max(data_vec, 2)
        return 20 * (np.log10(abs(reading)))

    def set_mic(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.FORMAT,
                                      channels=self.CHANNEL,
                                      rate=self.SAMP_RATE,
                                      input=True,
                                      output=False,
                                      frames_per_buffer=self.CHUNK)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def send_data(self):
        value = max(self.local_data)
        self.global_data.append(value)

        if len(self.global_data)>=10:
            now = datetime.datetime.now()
            google = GoogleSheets.GoogleWrite()
            var_time = ""+str(now.hour)+":"+str(now.minute)+":"+str(now.second) # stacking the hour to a variable
            var_data = max(self.global_data)
            self.global_data.clear()
            
            try:
                task_google = threading.Thread(target=google.send,args=(var_data,var_time))
                task_azure = threading.Thread(target=print,args=("Azure send"))
                
                task_azure.start()    
                task_google.start()
            
            except Exception as e:
                print(e)  # writing out a exception message 
                pass
            
            finally:
                print("\nValue in dB: "+str(var_data)+" Time: "+str(var_time))

if __name__ == '__main__':
    Recorder()
