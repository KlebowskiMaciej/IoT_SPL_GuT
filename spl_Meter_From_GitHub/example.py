import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import time

plt.style.use('ggplot')
plt.rcParams['font.size']=18

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 44100 # 2^12 samples for buffer
dev_index = 1 # device index found by p.get_device_info_by_index(ii)

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)

# record data chunk 
stream.start_stream()
data = np.fromstring(stream.read(chunk),dtype=np.int16)
stream_data = data
stream.stop_stream()

# mic sensitivity correction and bit conversion
mic_sens_dBV = 47.0 # mic sensitivity in dBV + any gain
mic_sens_corr = np.power(10.0,mic_sens_dBV/20.0) # calculate mic sensitivity conversion factor

# (USB=5V, so 15 bits are used (the 16th for negatives)) and the manufacturer microphone sensitivity corrections
data = ((data/np.power(2.0,15))*5.25)/(mic_sens_corr) 

# compute FFT parameters
f_vec = samp_rate*np.arange(chunk/2)/chunk # frequency vector based on window size and sample rate
mic_low_freq = 100 # low frequency response of the mic (mine in this case is 100 Hz)
low_freq_loc = np.argmin(np.abs(f_vec-mic_low_freq))
fft_data = (np.abs(np.fft.fft(data))[0:int(np.floor(chunk/2))])/chunk
fft_data[1:] = 2*fft_data[1:]

max_loc = np.argmax(fft_data[low_freq_loc:])+low_freq_loc

# plot
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
plt.plot(f_vec,fft_data)
ax.set_ylim([0,2*np.max(fft_data)])
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [Pa]')
plt.grid(True)
plt.annotate(r'$\Delta f_{max}$: %2.1f Hz' % (samp_rate/(2*chunk)),xy=(0.7,0.92),\
             xycoords='figure fraction')
annot = ax.annotate('Freq: %2.1f'%(f_vec[max_loc]),xy=(f_vec[max_loc],fft_data[max_loc]),\
                    xycoords='data',xytext=(0,30),textcoords='offset points',\
                    arrowprops=dict(arrowstyle="->"),ha='center',va='bottom')
    
ax.set_xscale('log')
plt.tight_layout()
plt.savefig('fft_real_signal.png',dpi=300,facecolor='#FCFCFC')
plt.show()

# A-weighting function and application
f_vec = f_vec[1:]
R_a = ((12194.0**2)*np.power(f_vec,4))/(((np.power(f_vec,2)+20.6**2)*np.sqrt((np.power(f_vec,2)+107.7**2)*(np.power(f_vec,2)+737.9**2))*(np.power(f_vec,2)+12194.0**2)))
a_weight_data_f = (20*np.log10(R_a)+2.0)+(20*np.log10(fft_data[1:]/0.00002))
a_weight_sum = np.sum(np.power(10,a_weight_data_f/20)*0.00002)
print(20*np.log10(a_weight_sum/0.00002))