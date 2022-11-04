import audioop
import AudioStream
import InitParam
import numpy as np
import AudioAnalyze
from math import log10


class AudioAnalyze(object):
    def __init__(self,data_vec):
        self.param = InitParam.InitParam()
        db = 20 * log10(self.audioloopp(data_vec))
        #freq_ii,fft_ii= self.fft(data_vec) # calculate fft for chunk
        #print("chunk freq data: "+ str(freq_ii)+", chunk fft data: "+str(fft_ii)+"RMS dB: "+str(self.audioloopp(data_vec)))
        print(db)
   
   
    #
    ##############################################
    # function for FFT
    ##############################################
    #
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