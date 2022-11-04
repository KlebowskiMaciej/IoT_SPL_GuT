import pyaudio
import numpy as np


class InitParam():
    CHUNK          = 1024*2  # frames to keep in buffer between reads
    SAMP_RATE      = 44100 # sample rate [Hz]
    pyaudio_format = pyaudio.paInt16 # 16-bit device
    buffer_format  = np.int16 # 16-bit for buffer
    CHANNEL        = 1 # only read 1 channel
    DEV_INDEX      = 0 # index of sound device