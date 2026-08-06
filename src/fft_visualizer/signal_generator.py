import numpy as np
import matplotlib.pyplot as plt
from .waves import Wave

class SignalGenerator:
    def __init__(self, sample_rate: int = 48000, duration: float = 1.0):
        self.sample_rate = sample_rate
        self.duration = duration
        self._waves: list[Wave] = []
        number_of_samples = int(sample_rate * duration)
        self.time = (np.arange(number_of_samples, dtype=np.float64)/ sample_rate)

    def add_wave(self, wave:Wave):
        self._waves.append(wave)

    def remove_wave(self, index:int):
        if index < 0 or index >= len(self._waves):
            raise IndexError('Wave index is out of range')
        return self._waves.pop(index)

    def clear(self):
        self._waves.clear()

    def generate(self):
        time = self.time
        signal = np.zeros_like(time)

        for wave in self._waves:
            signal += wave.generate(time)

        return time, signal
    
