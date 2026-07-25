import scipy.fft
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.io import wavfile

class VisualizeFFT:
    def __init__(self, signal, sample_rate, window_size, hop_size):
        self.signal = signal    #signal y values not signal object
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.hop_size = hop_size
        self.window = np.hanning(self.window_size)

        self.raw_fft = None
        self.fft = None
        self.fft_log = None
        self.freqs = None
        self.times = None

        


    def short_time_fft(self):

        leftover = (len(self.signal) - self.window_size) % self.hop_size 
        if leftover == 0:
            padding = 0
        else:
            padding = self.hop_size - leftover
        padded_signal = np.pad(self.signal, (0,padding), 'constant')

        fft_result=[]

        print("Starting stft")
        for start in tqdm(range(0,len(padded_signal)-self.window_size+1,self.hop_size)):
            segment_data = padded_signal[start:start+self.window_size]
            segment_data=segment_data*self.window

            segment_result = scipy.fft.rfft(segment_data)
            fft_result.append(segment_result)

        fft_result=np.array(fft_result)
        self.raw_fft = fft_result
        self.fft = np.abs(fft_result) * 2 / self.window_size
        self.fft_log = 20 * np.log10(np.abs(fft_result)+1e-12)
        self.freqs = scipy.fft.rfftfreq(self.window_size, 1/self.sample_rate)
        self.times = np.arange(self.fft.shape[0]) * self.window_size / self.sample_rate


    def plot_spectrogram(self):
        print("starting plot")
        fig, axs = plt.subplots(2,figsize=(10, 6),sharex=True,constrained_layout=True)

        signal_time = np.arange(len(self.signal)) / self.sample_rate
        axs[0].plot(signal_time,self.signal)
        axs[0].set_ylabel("Amplitude")
        axs[0].set_title("Signal")

        im = axs[1].imshow(self.fft_log.T, origin='lower', aspect='auto', interpolation='none', extent=[0,signal_time[-1],self.freqs[0],self.freqs[-1]])
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Frequency (Hz)")
        axs[1].set_title("Spectrogram")
        fig.colorbar(im, ax=axs[1], label="Magnitude (dB)")
        plt.show()


    def ifft_by_strongest(self, num_freqs):
        magnitude = np.abs(self.raw_fft)
        filtered_fft = np.zeros_like(self.raw_fft) 

        print("Starting ifft")
        for i in range(self.raw_fft.shape[0]):
            top_freqs_index = np.argpartition(magnitude[i], -num_freqs)[-num_freqs:]
            filtered_fft[i, top_freqs_index] = self.raw_fft[i, top_freqs_index]  

        num_frames = filtered_fft.shape[0]
        output_length = (num_frames - 1) * self.hop_size + self.window_size

        reconstructed_signal = np.zeros(output_length)
        weights = np.zeros(output_length)

        for i, frame in enumerate(tqdm(filtered_fft)):
            segment = scipy.fft.irfft(frame, n=self.window_size)

            start = i * self.hop_size

            reconstructed_signal[start:start + self.window_size] += segment
            weights[start:start + self.window_size] += self.window


        threshold = 0.1 * np.max(weights)
        valid = weights > threshold

        out = np.zeros_like(reconstructed_signal)
        out[valid] = reconstructed_signal[valid] / weights[valid]

        return out

    def output_wav(self,num_freqs):
        reconstructed_signal = self.ifft_by_strongest(num_freqs)


        target_rms = np.sqrt(np.mean(self.signal.astype(np.float64)**2))

        current_rms = np.sqrt(np.mean(reconstructed_signal**2))
        if current_rms > 1e-12:
            reconstructed_signal = reconstructed_signal * (target_rms / current_rms)

        # safety: prevent clipping if the RMS-matched signal has a peak that overflows int16
        peak = np.max(np.abs(reconstructed_signal))
        if peak > 32767:
            reconstructed_signal = reconstructed_signal * (32767 / peak)

        
        filename = "output_scipy.wav"
        peak = np.max(np.abs(reconstructed_signal))
        signal_int16 = (reconstructed_signal/peak*32767).astype(np.int16)

        wavfile.write(filename, self.sample_rate, signal_int16)

        print(f"Saved {filename}")
