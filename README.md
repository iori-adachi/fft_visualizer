# FFT Visualizer

An interactive Python application for generating signals and visualizing their frequency content using the Fast Fourier Transform (FFT) and Short-Time Fourier Transform (STFT).

I built this project while studying digital signal processing to experiment with Fourier analysis, spectral content, and time-frequency representations through an interactive GUI rather than only working through textbook examples.

## Features

- Generate and combine multiple signal types:
  - Sine waves
  - Square waves
  - Sawtooth waves
  - White noise
- Adjust frequency, amplitude, and phase
- Add and remove individual signal components
- Visualize the combined signal in the time domain
- Compute and display the FFT magnitude spectrum
- Display a spectrogram using a custom STFT implementation
- Switch interactively between spectrum and spectrogram views
- Load WAV files for signal analysis
- Interactive GUI built with PyQt6 and PyQtGraph

## Screenshots

<img width="2084" height="1265" alt="image" src="https://github.com/user-attachments/assets/b5c4ae18-3393-4d76-9bb6-f3d1d5226e18" />


## DSP Implementation

### FFT

The frequency spectrum is calculated using SciPy's real-valued FFT:

```python
self.raw_fft = scipy.fft.rfft(self.signal)
self.freqs = scipy.fft.rfftfreq(num_samples, d=1/self.sample_rate)
self.magnitude = (2*np.abs(self.raw_fft))/num_samples
```

For a discrete signal \(x[n]\), the Discrete Fourier Transform is

\[
X[k] = \sum_{n=0}^{N-1} x[n]e^{-j2\pi kn/N}.
\]

Because the generated signals are real-valued, only the non-negative frequency components need to be calculated.

This makes it possible to directly observe features such as the fundamental frequency of a sine wave and the harmonic content of square and sawtooth waves.

### Short-Time Fourier Transform

A normal FFT shows which frequencies are present over the entire signal but does not show when those frequencies occur.

The visualizer therefore also implements an STFT. The signal is divided into overlapping frames, each frame is multiplied by a Hann window, and an FFT is calculated for each segment.

```python
for start in range(0, len(padded_signal)-self.window_size+1, self.hop_size):
    segment_data = padded_signal[start:start+self.window_size]
    segment_data = segment_data*self.window
    segment_result = scipy.fft.rfft(segment_data)
```

The resulting spectra are displayed as a spectrogram, providing a time-frequency representation of the signal.

The default STFT parameters are:

- Window size: 1024 samples
- Hop size: 512 samples
- Window: Hann

## Signal Generation

Signals are represented as individual wave objects and combined by the signal generator.

Currently supported waveforms include:

### Sine

\[
x(t) = A\sin(2\pi ft + \phi)
\]

### Square

A square wave generated from the selected frequency, amplitude, and phase.

### Sawtooth

A sawtooth wave generated from the selected frequency, amplitude, and phase.

### White Noise

Random normally distributed samples with adjustable amplitude.

Multiple waveforms can be added simultaneously, making it possible to observe how different signal components appear in both the time and frequency domains.

## Tech Stack

- Python
- NumPy
- SciPy
- PyQt6
- PyQtGraph
- Poetry

## Installation

Clone the repository:

```bash
git clone https://github.com/iori-adachi/fft_visualizer.git
cd fft_visualizer
```

Install the dependencies with Poetry:

```bash
poetry install
```

Run the application:

```bash
poetry run python -m fft_visualizer.main
```

## Project Structure

```text
fft_visualizer/
├── src/
│   └── fft_visualizer/
│       ├── main.py
│       ├── gui.py
│       ├── visualize_fft.py
│       ├── signal_generator.py
│       └── waves.py
├── tests/
├── pyproject.toml
├── poetry.lock
└── README.md
```

### Main Components

**`gui.py`**  
Implements the PyQt6/PyQtGraph interface and connects the signal controls to the visualizations.

**`waves.py`**  
Defines the waveform classes used by the application, including sine, square, sawtooth, white noise, and sampled signals.

**`signal_generator.py`**  
Combines individual waveform objects into a sampled signal.

**`visualize_fft.py`**  
Handles FFT and STFT calculations used for the spectrum and spectrogram displays.


## Future Improvements

Possible future additions include:

- Adjustable STFT window and hop sizes
- Additional window functions
- FIR and IIR filtering
- Interactive low-pass, high-pass, and band-pass filters
- Inverse FFT/STFT reconstruction
- Audio playback
- Improved WAV-file controls
- Real-time audio input
- IQ signal support for software-defined radio applications
- AM/FM and digital modulation demonstrations

## License

This project is intended for educational and personal use.
