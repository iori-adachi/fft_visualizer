from .signal_generator import Signal
from .custom_fft import VisualizeFFT
import numpy as np
import matplotlib.pyplot as plt
import json
import scipy.fft
from scipy.io import wavfile


'''signal = Signal.from_json("src/fft_visualizer/signals.json")
signal.noiser(0,1)
visualize = VisualizeFFT(signal.yval, signal.sample_rate, 4800)
visualize.short_time_fft()
visualize.plot_spectrogram()'''

file_name = 'Flawed Mangoes_Dramamine.wav'
sample_rate, data = wavfile.read(file_name)
data=data[:,0]
visualize = VisualizeFFT(data, sample_rate, 128,64)
visualize.short_time_fft()
visualize.output_wav(2)
#visualize.plot_spectrogram()