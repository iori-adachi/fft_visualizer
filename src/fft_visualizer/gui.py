from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSplitter,
    QLabel,
    QComboBox,
    QSlider,
    QListWidget,
)

from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import time
import pyqtgraph as pg
from scipy.io import wavfile
import numpy as np
from .signal_generator import SignalGenerator
from .waves import *
from .visualize_fft import VisualizeFFT
from scipy.signal import resample

SAMPLE_RATE = 48000

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FFT Visualizer")
        self.resize(1200, 700)

        self.generator = SignalGenerator(sample_rate=SAMPLE_RATE, duration=60.0)
        self.visualizer = VisualizeFFT(sample_rate=SAMPLE_RATE)


        # -----------------------
        # Controls panel (left)
        # -----------------------
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)

        control_layout.addWidget(QLabel('Create Wave'))

        #Wave type
        self.wave_type_box = QComboBox()
        self.wave_type_box.addItems(['Sine','Square','Saw','Noise'])
        control_layout.addWidget(self.wave_type_box)

        #Frequency Controls
        self.frequency_label = QLabel('Frequency: 1000Hz')
        self.frequency_slider = QSlider(Qt.Orientation.Horizontal)
        self.frequency_slider.setRange(1,int(SAMPLE_RATE/2))
        self.frequency_slider.setValue(1000)

        control_layout.addWidget(self.frequency_label)
        control_layout.addWidget(self.frequency_slider)

        # Amplitude control
        self.amplitude_label = QLabel("Amplitude: 1.00")
        self.amplitude_slider = QSlider(Qt.Orientation.Horizontal)
        self.amplitude_slider.setRange(0, 200)
        self.amplitude_slider.setValue(100)

        control_layout.addWidget(self.amplitude_label)
        control_layout.addWidget(self.amplitude_slider)

        # Phase control
        self.phase_label = QLabel("Phase: 0")
        self.phase_slider = QSlider(Qt.Orientation.Horizontal)
        self.phase_slider.setRange(-180, 180)
        self.phase_slider.setValue(0)

        control_layout.addWidget(self.phase_label)
        control_layout.addWidget(self.phase_slider)

        # Add button
        self.add_wave_button = QPushButton("Add Wave")
        control_layout.addWidget(self.add_wave_button)

        # Existing wave list
        control_layout.addWidget(QLabel("Added Waves"))
        self.wave_list = QListWidget()
        control_layout.addWidget(self.wave_list)

        # Remove and clear buttons
        self.remove_wave_button = QPushButton("Remove Selected")
        self.clear_waves_button = QPushButton("Clear All")

        control_layout.addWidget(self.remove_wave_button)
        control_layout.addWidget(self.clear_waves_button)

        # Toggle Spectrogram
        self.spectrogram_toggle = QPushButton("Show Spectrogram")
        self.spectrogram_toggle.setCheckable(True)
        control_layout.addWidget(self.spectrogram_toggle)

        # Keep controls aligned near the top
        control_layout.addStretch()

        # Push everything to the top
        #control_layout.setRowStretch(99, 1)

        # -----------------------
        # Plot panel (right)
        # -----------------------
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        
        # Signal plot
        self.signal_plot = pg.PlotWidget(labels={'left':'Amplitude', 'bottom':'Time (s)'})
        self.signal_plot.setMouseEnabled(x=True, y=False)
        plot_layout.addWidget(self.signal_plot)
        self.signal_curve = self.signal_plot.plot()

        # Spectrum plot
        self.spectrum_plot = pg.PlotWidget(labels={'left':'Amplitude', 'bottom':'Frequency [Hz]'})
        self.spectrum_plot.setMouseEnabled(x=True, y=False)
        plot_layout.addWidget(self.spectrum_plot)
        self.spectrum_curve = self.spectrum_plot.plot()
        self.spectrogram_image = pg.ImageItem()
        self.spectrum_plot.addItem(self.spectrogram_image)
        self.spectrogram_image.setVisible(False)
        self.spectrogram_image.setColorMap(pg.colormap.get('viridis'))


        # -----------------------
        # Splitter
        # -----------------------
        splitter = QSplitter(Qt.Orientation.Horizontal)

        splitter.addWidget(control_widget)
        splitter.addWidget(plot_widget)

        # Initial widths (pixels)
        splitter.setSizes([300, 900])

        # Plot expands more than controls
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)


        # -----------------------
        # GUI events
        # -----------------------
        self.frequency_slider.valueChanged.connect(self.update_control_labels)
        self.amplitude_slider.valueChanged.connect(self.update_control_labels)
        self.phase_slider.valueChanged.connect(self.update_control_labels)
        self.add_wave_button.clicked.connect(self.add_wave)
        self.remove_wave_button.clicked.connect(self.remove_selected_wave)
        self.clear_waves_button.clicked.connect(self.clear_waves)
        self.spectrogram_toggle.toggled.connect(self.on_spectrogram_toggled)

        self.make_menu()
        self.refresh_plot()


    def update_control_labels(self):
        frequency = self.frequency_slider.value()
        amplitude = self.amplitude_slider.value() / 100
        phase = self.phase_slider.value()

        self.frequency_label.setText(
            f"Frequency: {frequency} Hz"
        )
        self.amplitude_label.setText(
            f"Amplitude: {amplitude:.2f}"
        )
        self.phase_label.setText(
            f"Phase: {phase}°"
        )

    def add_wave(self):
        frequency = float(self.frequency_slider.value())
        amplitude = self.amplitude_slider.value() / 100
        phase_degrees = self.phase_slider.value()
        phase_radians = np.deg2rad(phase_degrees)
        wave_type = self.wave_type_box.currentText()

        if wave_type == 'Sine': wave = SineWave(frequency=frequency, amplitude=amplitude, phase=phase_radians)
        elif wave_type == 'Square': wave = SquareWave(frequency=frequency, amplitude=amplitude, phase=phase_radians)
        elif wave_type == 'Saw': wave = SawWave(frequency=frequency, amplitude=amplitude, phase=phase_radians)
        elif wave_type == 'Noise': wave = WhiteNoise(amplitude=amplitude,seed=5)
        else: return

        self.generator.add_wave(wave)
        self.wave_list.addItem(wave.description())
        self.refresh_plot()

    def remove_selected_wave(self):
        selected_row = self.wave_list.currentRow()

        if selected_row < 0: return

        self.generator.remove_wave(selected_row)
        self.wave_list.takeItem(selected_row)
        self.refresh_plot()

    def clear_waves(self):
        self.generator.clear()
        self.wave_list.clear()
        self.refresh_plot()

    def refresh_plot(self):
        time, signal = self.generator.generate()
        self.signal_curve.setData(time, signal)

        if self.spectrogram_toggle.isChecked():
            self.update_spectrogram(signal)
        else:
            self.visualizer.set_signal(signal)
            self.visualizer.calculate_fft()
            freqs, mags = self.visualizer.get_spectrum()
            self.spectrum_curve.setData(freqs,mags)


    def on_spectrogram_toggled(self, checked):
        self.spectrogram_toggle.setText("Show Spectrum" if checked else "Show Spectrogram")
        self.spectrum_curve.setVisible(not checked)
        self.spectrogram_image.setVisible(checked)

        if checked:
            self.spectrum_plot.setLabels(left='Frequency [Hz]', bottom='Time [s]')
        else:
            self.spectrum_plot.setLabels(left='Amplitude', bottom='Frequency [Hz]')

        self.refresh_plot()
        self.spectrum_plot.autoRange()


    def update_spectrogram(self, signal):
        self.visualizer.set_signal(signal)
        self.visualizer.calculate_stft()

        self.spectrogram_image.setImage(self.visualizer.fft_log, autoLevels=True)
        self.spectrogram_image.setRect(
            pg.QtCore.QRectF(
                self.visualizer.times[0],
                self.visualizer.freqs[0],
                self.visualizer.times[-1] - self.visualizer.times[0],
                self.visualizer.freqs[-1] - self.visualizer.freqs[0],
            )
        )
        self.spectrum_plot.autoRange()  


    def make_menu(self):

        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        open_action = QAction("Open WAV...", self)

        open_action.triggered.connect(self.open_file)

        file_menu.addAction(open_action)

    def open_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self, "Open WAV File", "", "Wave Files (*.wav)"
        )
        if not filename:
            return

        sample_rate, signal = load_wav(filename)

        # Resample to match the app's sample rate if needed
        if sample_rate != SAMPLE_RATE:
            num_samples = int(len(signal) * SAMPLE_RATE / sample_rate)
            signal = resample(signal, num_samples)

        wave = SampledWave(samples=signal)
        self.generator.add_wave(wave)
        self.wave_list.addItem(wave.description())
        self.refresh_plot()

def load_wav(filename):
    sample_rate, data = wavfile.read(filename)

    # Convert stereo -> mono
    if data.ndim == 2:
        data = data.mean(axis=1)

    # Normalize
    data = data.astype(np.float32)

    data /= np.max(np.abs(data))

    return sample_rate, data