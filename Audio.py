import pyaudio
import numpy as np
import time
import audioop
import datetime
import GoogleSheets
import threading

class Recorder(object):

    # Data pack locally
    global local_data

    local_data = []

    #Data pack Globally
    global global_data

    global_data = []

    CHUNK = 1024  # frames to keep in buffer between reads
    SAMP_RATE = 44100  # sample rate [Hz]
    FORMAT = pyaudio.paInt16  # 16-bit device
    # BUFFOR_FORMAT  = np.int16 # 16-bit for buffer
    CHANNEL = 1  # only read 1 channel mono 2 stereo
    DEV_INDEX = 0  # index of sound device
    PAUSE = False
    FRAME_COUNT = 0
    SECONDS = 30
    SIZE_SEND_DATA = 10

    def __init__(self):

        self.analyzer()

   

    def analyzer(self):
        self.set()
        error_count = 0
        start_time = time.time()

        print('stream started')

        while not self.PAUSE:
            try:
                stream_data = self.stream.read(self.CHUNK, exception_on_overflow=False)  # grab data frames from buffer
                current_time = time.time()
            except IOError as e:
                error_count += 1
                print("(%d) Error %s" & (error_count, e))
            else:
                elapsed_time = current_time - start_time
                local_data.append(self.process(stream_data))
                if elapsed_time > self.SECONDS:
                    start_time = time.time()
                    self.send()
                    local_data.clear()


        else:
            fr = self.FRAME_COUNT / (time.time() - start_time)
            print('average frame rate = {:.0f} FPS'.format(fr))

    def process(self, data_vec):
        reading = audioop.max(data_vec, 2)
        return 20 * (np.log10(abs(reading)))

    def set(self):
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


    def send(self):
        value = max(local_data)
        global_data.append(value)

        if len(global_data)>=10:
           now = datetime.datetime.now()
            google = GoogleSheets.GoogleWrite()
            time = ""+str(now.hour)+":"+str(now.minute)+":"+str(now.second)
            value = max(global_data)
            
            global_data.clear()
            
            task_google = threading.Thread(target=google.send,args=(value,time))
            task_azure = threading.Thread(target=print,args=("Azure send"))
            #Send To Azure
            task_azure.start()
            
            #Send To Google Sheets            
            task_google.start()



if __name__ == '__main__':
    Recorder()
