import pyaudio
import numpy as np
import AudioStream


class InitParam():
    CHUNK          = 4096  # frames to keep in buffer between reads
    SAMP_RATE      = 44100 # sample rate [Hz]
    pyaudio_format = pyaudio.paInt16 # 16-bit device
    buffer_format  = np.int16 # 16-bit for buffer
    CHANNEL        = 1 # only read 1 channel mono 2 stereo
    DEV_INDEX      = 0 # index of sound device
    
    
if __name__ == '__main__':
    AudioStream.AudioStream()
    
