#!/usr/bin/python
# -*- coding: UTF-8 -*-
import scipy
import pydub
import numpy as np
import os
import AudioSynthesis

import pysptk
import seaborn
import matplotlib

import matplotlib.pyplot as plt
# Librosa for audio
import librosa
# And the display module for visualization
import librosa.display
from scipy.io import wavfile

# import AudioDownloader
class AudioSpectrogram:

    def __init__(self, audio_path):
        # self.input_audio_path = input_audio_path
        # self.output_audio_path = output_audio_path
        self.audio_path = audio_path
        if self.audio_path.endswith("wav"):
            audio_file = pydub.AudioSegment.from_file(audio_path, format=".wav")
        elif self.audio_path.endswith("mp3"):
            audio_file = pydub.AudioSegment.from_file(audio_path, format="mp3")
        self.audio = np.fromstring(audio_file._data, np.int16)
        # self.sr, self.audio = wavfile.read(audio_path)

        self.frame_rate = audio_file.frame_rate
        self.sr = self.frame_rate
        #numbers for each seg
        self.seg_len = int(20 * self.frame_rate / 1000)

        self.slide_len = int(self.seg_len/2)

        self.spectrogram = []

    def np_fft(self):
        self.sp = np.fft.fft(self.audio)
        self.freq = np.fft.fftfreq(self.audio.shape[-1]) * self.sr
        plt.plot(self.freq, self.sp.real)

    def np_ifft(self):
        self.resynthesis_audio = np.fft.ifft(self.sp)

    def audio_spectrum(self, audio_slice):
        return np.fft.fft(audio_slice)

    def librosa_mfcc(self):
        y, self.sr = librosa.load(self.audio_path, sr=16000)
        # Let's make and display a mel-scaled power (energy-squared) spectrogram
        S = librosa.feature.melspectrogram(y, sr=self.sr, n_mels=128)

        # Convert to log scale (dB). We'll use the peak power (max) as reference.
        self.log_S = librosa.power_to_db(S, ref=np.max)

    def pysptk_mfcc(self):
        self.frame_length = 1024
        self.hop_length = 80
        self.pitch = pysptk.swipe(self.audio.astype(np.float64), fs=self.sr, hopsize=self.hop_length, min=60, max=240, otype="pitch")
        self.source_excitation = pysptk.excite(self.pitch, self.hop_length)

        # Note that almost all of pysptk functions assume input array is C-contiguous and np.float4 element type
        frames = librosa.util.frame(self.audio, frame_length=self.frame_length, hop_length=self.hop_length).astype(np.float64).T

        # Windowing
        frames *= pysptk.blackman(self.frame_length)

        assert frames.shape[1] == self.frame_length

        # Order of mel-cepstrum
        self.order = 25
        self.alpha = 0.41

        self.mc = pysptk.mcep(frames, self.order, self.alpha)
        logH = pysptk.mgc2sp(self.mc, self.alpha, 0.0, self.frame_length).real
        librosa.display.specshow(logH.T, sr=self.sr, hop_length=self.hop_length, x_axis="time", y_axis="linear")
        # colorbar()
        # title("Spectral envelope estimate from mel-cepstrum")

    def pysptk_imfcc(self):
        from pysptk.synthesis import MLSADF, Synthesizer

        # Convert mel-cesptrum to MLSADF coefficients
        b = pysptk.mc2b(self.mc, self.alpha)

        synthesizer = Synthesizer(MLSADF(order=self.order, alpha=self.alpha), self.hop_length)

        x_synthesized = synthesizer.synthesis(self.source_excitation, b)

        librosa.display.waveplot(x_synthesized, sr=self.sr)
        a = 0
        # title("Synthesized waveform by MLSADF")
        # Audio(x_synthesized, rate=self.sr)

    def librosa_plot_audio(self, audio):
        librosa.display.waveplot(audio, sr=self.sr)

    def librosa_plot_mfcc(self):
        # matplotlib for displaying the output
        import matplotlib.pyplot as plt
        # Make a new figure
        plt.figure(figsize=(12, 4))

        # Display the spectrogram on a mel scale
        # sample rate and hop length parameters are used to render the time axis
        librosa.display.specshow(self.log_S, sr=self.sr, x_axis='time', y_axis='mel')

        # Put a descriptive title on the plot
        plt.title('mel power spectrogram')

        # draw a color bar
        plt.colorbar(format='%+02.0f dB')

        # Make the figure layout compact
        plt.tight_layout()

    def audio_segmentation(self):
        size = len(self.audio)
        i = 0
        while((i+self.seg_len)<size):
            audio_seg = self.audio[i : i+self.seg_len]
            i = i+self.slide_len
            self.spectrogram.append(self.audio_spectrum(audio_seg))

        if(i < size):
            audio_seg = np.zeros(self.seg_len, np.float)
            audio_seg[0:size-i-1] = self.audio[i : size-1]
            self.spectrogram.append(self.audio_spectrum(audio_seg))

    def save_result(self):
        file_name = os.path.splitext(os.path.basename(self.audio_path))[0]
        par_path = os.path.basename(os.path.dirname(self.audio_path)) + "_npy"
        AudioSynthesis.build_directory(par_path)
        np.save(os.path.join(par_path, file_name), self.spectrogram)

if __name__ == '__main__':
    # s = AudioSpectrogram("./clean_p226_060.wav")
    s = AudioSpectrogram("./Having A Shower.mp3")
    s.np_fft()
    s.librosa_plot_audio(s.audio)
    s.pysptk_mfcc()
    s.pysptk_imfcc()
    s.librosa_mfcc()
    s.librosa_plot_mfcc()


    folder_path = "./small_mix"
    for file_path in AudioSynthesis.get_subfolders(folder_path):
        s = AudioSpectrogram(os.path.join(folder_path, file_path))
        s.audio_segmentation()
        s.save_result()

        # c = np.load("a0001.npy")
        # audio_file = pydub.AudioSegment.from_file("./wav/a0001.wav", format=".wav")
        # output_audio = np.fromstring(audio_file._data, np.int16)

    v = scipy.__version__