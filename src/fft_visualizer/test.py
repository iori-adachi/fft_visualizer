import numpy as np
from scipy.io.wavfile import write

# Configuration
filename = "output_scipy.wav"
sample_rate = 44100
duration = 2.0
frequency = 440.0

# Generate time array and sine wave
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio_signal = np.sin(2 * np.pi * frequency * t)

# Scale signal to 16-bit integer range and convert type
audio_int16 = (audio_signal * 32767).astype(np.int16)

# Output directly to WAV
write(filename, sample_rate, audio_int16)

print(f"Saved {filename}")
