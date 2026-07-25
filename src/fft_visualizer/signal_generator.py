import numpy as np
import matplotlib.pyplot as plt
import json

class Signal:
    def __init__(self, sample_rate, components):
        self.sample_rate = sample_rate

        self.components = components
        self.freqs = [c['frequency'] for c in self.components]
        self.amps = [c['amplitude'] for c in self.components]
        self.starts = [c['start'] for c in self.components]
        self.stops = [c['stop'] for c in self.components]

        self.duration = max(self.stops)
        self.N = int(self.sample_rate * self.duration)

        self.generate()

    @classmethod
    def from_json(cls, filename):
        with open(filename) as f:
            data = json.load(f)

        return cls(
            data["sample_rate"],
            data["components"],
        )

    def generate(self):
        self.tval = np.linspace(0, self.duration, self.N)
        self.yval = np.zeros(len(self.tval))
        for i in range(len(self.freqs)):
            start = int(self.starts[i]*self.sample_rate)
            stop = int(self.stops[i]*self.sample_rate)
            self.yval[start:stop] += self.amps[i]*np.sin(self.freqs[i]*self.tval*(2*np.pi))[start:stop]

    def noiser(self,mu,sig):
        noise = np.random.normal(mu, sig, self.yval.shape)
        self.yval += noise

    
