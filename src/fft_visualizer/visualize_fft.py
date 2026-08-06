import scipy.fft
import numpy as np

class VisualizeFFT:
    def __init__(self, sample_rate):
        self.signal = None
        self.sample_rate = sample_rate

        self.raw_fft = None
        self.magnitude = None
        self.magnitude_db = None
        self.freqs = None

    def set_signal(self, signal):
        self.signal = np.asarray(signal)

    def calculate_fft(self):
        num_samples = len(self.signal)

        self.raw_fft = scipy.fft.rfft(self.signal)
        self.freqs = scipy.fft.rfftfreq(num_samples, d=1/self.sample_rate)
        self.magnitude = (2*np.abs(self.raw_fft))/num_samples
        self.magnitude_db = 20 * np.log10(np.maximum(self.magnitude,1e-12))

    def get_sepctrum(self):
        return self.freqs, self.magnitude

