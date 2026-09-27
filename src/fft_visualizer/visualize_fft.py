import scipy.fft
import numpy as np

class VisualizeFFT:
    def __init__(self, sample_rate, window_size=1024, hop_size=512):
        self.signal = None
        self.sample_rate = sample_rate

        self.window_size = window_size
        self.hop_size = hop_size
        self.window = np.hanning(window_size)

        self.raw_fft = None
        self.magnitude = None
        self.magnitude_db = None
        self.freqs = None

        self.fft = None
        self.fft_log = None
        self.times = None

    def set_signal(self, signal):
        self.signal = np.asarray(signal)

    def calculate_fft(self):
        num_samples = len(self.signal)

        self.raw_fft = scipy.fft.rfft(self.signal)
        self.freqs = scipy.fft.rfftfreq(num_samples, d=1/self.sample_rate)
        self.magnitude = (2*np.abs(self.raw_fft))/num_samples
        self.magnitude_db = 20 * np.log10(np.maximum(self.magnitude,1e-12))

    def get_spectrum(self):
        return self.freqs, self.magnitude

    def calculate_stft(self):
        leftover = (len(self.signal) - self.window_size) % self.hop_size 
        if leftover == 0:
            padding = 0
        else:
            padding = self.hop_size - leftover
        padded_signal = np.pad(self.signal, (0,padding), 'constant')

        fft_result=[]

        for start in range(0,len(padded_signal)-self.window_size+1,self.hop_size):
            segment_data = padded_signal[start:start+self.window_size]
            segment_data=segment_data*self.window

            segment_result = scipy.fft.rfft(segment_data)
            fft_result.append(segment_result)

        fft_result=np.array(fft_result)
        self.raw_fft = fft_result
        self.fft = np.abs(fft_result) * 2 / self.window_size
        self.fft_log = 20 * np.log10(np.abs(fft_result)+1e-12)
        self.freqs = scipy.fft.rfftfreq(self.window_size, 1/self.sample_rate)
        self.times = np.arange(self.fft.shape[0]) * self.hop_size / self.sample_rate

    

