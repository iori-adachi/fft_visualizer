# DSP Visualizer

An interactive Python application for visualizing and experimenting with digital signal processing concepts in both the time and frequency domains.

The project provides a graphical interface for generating signals, computing FFTs and spectrograms, applying frequency-domain processing, reconstructing signals, and working with audio files. I built it as a hands-on way to explore DSP concepts beyond textbook examples.

<img width="2084" height="1265" alt="image" src="https://github.com/user-attachments/assets/d23d85db-f50c-49d5-ae2a-97a909c4679a" />


## Features

- Generate sine, square, and sawtooth signals
- Combine multiple signals and add noise
- Visualize signals in the time domain
- Compute and display the Fast Fourier Transform (FFT)
- Identify dominant frequency components
- Apply window functions such as the Hann window
- Compute and visualize spectrograms using the Short-Time Fourier Transform (STFT)
- Adjust STFT window size and overlap/hop length
- Reconstruct signals using the inverse FFT
- Import WAV audio files for analysis
- Interactive GUI built with PyQtGraph

## Example Applications

The visualizer can be used to explore concepts such as:

- Harmonic content of non-sinusoidal signals
- Spectral leakage and windowing
- Time-frequency resolution
- Frequency-domain filtering
- Signal reconstruction
- Effects of noise on a signal's spectrum

For example, a square wave can be generated and compared in the time and frequency domains to observe its odd harmonic structure.

## Tech Stack

- Python
- NumPy
- SciPy
- PyQtGraph
- Qt
- Poetry

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd dsp-visualizer
```

Install the dependencies using Poetry:

```bash
poetry install
```

Run the application:

```bash
poetry run python main.py
```

> The exact entry point may differ depending on the project structure.

## How It Works

### Signal Generation

Signals are generated from user-selected parameters such as frequency and amplitude. Multiple components can be combined to create more complex signals.

For a sinusoidal signal,

\[
x(t) = A\sin(2\pi ft)
\]

where \(A\) is the amplitude and \(f\) is the frequency.

Square and sawtooth waves can also be generated to demonstrate signals containing multiple harmonic components.

### Frequency Analysis

The application uses the FFT to transform sampled signals from the time domain into the frequency domain:

\[
X[k] = \sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}
\]

For real-valued signals, the application uses NumPy's real FFT routines to efficiently calculate the positive-frequency spectrum.

Window functions can be applied before the FFT to reduce spectral leakage.

### Spectrogram

For signals whose frequency content changes over time, the application uses the Short-Time Fourier Transform.

The signal is divided into overlapping windows and an FFT is calculated for each segment. The resulting spectra are displayed as a spectrogram, showing how frequency content changes with time.

Changing the window and hop sizes demonstrates the tradeoff between time and frequency resolution.

### Signal Reconstruction

Frequency-domain data can be transformed back into the time domain using the inverse FFT, allowing modifications to the spectrum to be heard or visualized after reconstruction.

## Project Structure

```text
dsp-visualizer/
├── src/
│   └── ...
├── main.py
├── pyproject.toml
├── README.md
└── ...
```

## Motivation

I built this project while studying digital signal processing to connect the mathematical concepts of Fourier analysis with real signals and interactive visualizations.

My goal was to create a tool where I could experiment with FFTs, windowing, spectrograms, filtering, and signal reconstruction while developing practical Python signal-processing software.

## Future Improvements

Planned additions include:

- FIR and IIR filters
- Butterworth filter design
- Interactive frequency-domain filtering
- Improved inverse-STFT reconstruction
- Audio playback
- Additional window functions
- AM/FM modulation and demodulation
- Real-time signal visualization
- SDR/IQ sample support

## License

This project is intended for educational and personal use.
