from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from scipy import signal


class Wave(ABC):

    @abstractmethod
    def generate(self, time):
        pass

    @abstractmethod
    def description(self):
        pass

@dataclass(frozen=True)
class SineWave(Wave):
    frequency: float
    amplitude: float = 1.0
    phase: float = 0.0

    def generate(self, time):
        return self.amplitude * np.sin(2*np.pi * self.frequency * time + self.phase)

    def description(self):
        phase_degrees = np.rad2deg(self.phase)
        return (
            f"Sine | {self.frequency:g} Hz | "
            f"A={self.amplitude:g} | φ={phase_degrees:g}°"
        )


@dataclass(frozen=True)
class SquareWave(Wave):
    frequency: float
    amplitude: float = 1.0
    phase: float = 0.0

    def generate(self, time):
        return self.amplitude * signal.square(2*np.pi * self.frequency * time + self.phase)

    def description(self):
            phase_degrees = np.rad2deg(self.phase)
            return (
                f"Square | {self.frequency:g} Hz | "
                f"A={self.amplitude:g} | φ={phase_degrees:g}°"
            )

@dataclass(frozen=True)
class SawWave(Wave):
    frequency: float
    amplitude: float = 1.0
    phase: float = 0.0

    def generate(self, time):
        return self.amplitude * signal.sawtooth(2*np.pi * self.frequency * time + self.phase)

    def description(self):
            phase_degrees = np.rad2deg(self.phase)
            return (
                f"Saw | {self.frequency:g} Hz | "
                f"A={self.amplitude:g} | φ={phase_degrees:g}°"
            )


@dataclass(frozen=True)
class WhiteNoise(Wave):
    amplitude: float = 1.0
    seed:int = None

    def generate(self, time):
        rng = np.random.default_rng(self.seed)
        return self.amplitude * rng.standard_normal(len(time))

    def description(self):
            return (
                f"Noise | A={self.amplitude:g}"
            )


@dataclass(frozen=True)
class SampledWave(Wave):
    samples: np.ndarray  # already resampled to the generator's sample rate
    amplitude: float = 1.0

    def generate(self, time):
        n = len(time)
        data = self.samples
        if len(data) < n:
            data = np.pad(data, (0, n - len(data)))
        elif len(data) > n:
            data = data[:n]
        return self.amplitude * data

    def description(self):
        return f"Sample | {len(self.samples)} samples | A={self.amplitude:g}"