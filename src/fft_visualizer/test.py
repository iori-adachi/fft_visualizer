import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter, freqz

# 1. Generate a sample noisy signal
fs = 1000.0       # Sampling rate (Hz)
t = np.arange(0, 1.0, 1/fs) # 1 second time vector

# Signal components: 5 Hz (clean data) + 150 Hz (high frequency noise)
clean_signal = np.sin(2 * np.pi * 5 * t)
noise = 0.5 * np.sin(2 * np.pi * 150 * t)
noisy_signal = clean_signal + noise

# 2. Design the FIR Low-Pass Filter
numtaps = 65      # Number of coefficients (Filter length)
cutoff = 50.0     # Cutoff frequency (Hz)

# Calculate filter coefficients (taps) using a Hamming window
taps = firwin(numtaps, cutoff, fs=fs, window='hamming')

# 3. Apply the FIR filter to the data
# For FIR filters, the denominator (a) is always [1.0]
filtered_signal = lfilter(taps, 1.0, noisy_signal)

# 4. (Optional) Analyze the Frequency Response
w, h = freqz(taps, worN=8000, fs=fs)

# --- Plotting results ---
plt.figure(figsize=(10, 6))

# Plot Signal Comparison
plt.subplot(2, 1, 1)
plt.plot(t, noisy_signal, label='Noisy Signal (5Hz + 150Hz)', color='orange', alpha=0.6)
plt.plot(t, filtered_signal, label='Filtered Signal (FIR output)', color='blue', linewidth=2)
plt.title('Time Domain Filtering')
plt.xlabel('Time [seconds]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Plot Frequency Response
plt.subplot(2, 1, 2)
plt.plot(w, 20 * np.log10(np.abs(h)), color='red')
plt.axvline(cutoff, color='black', linestyle='--', label=f'Cutoff ({cutoff} Hz)')
plt.title('FIR Filter Frequency Response')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Gain [dB]')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
