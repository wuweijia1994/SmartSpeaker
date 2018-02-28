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


# Librosa for audio
import librosa
# And the display module for visualization
import librosa.display

# import AudioDownloader
class AudioSpectrogram:

    def __init__(self, audio_path):
        # self.input_audio_path = input_audio_path
        # self.output_audio_path = output_audio_path
        self.audio_path = audio_path
        audio_file = pydub.AudioSegment.from_file(audio_path, format=".wav")
        self.audio = np.fromstring(audio_file._data, np.int16)

        self.frame_rate = audio_file.frame_rate
        self.sr = self.frame_rate
        #numbers for each seg
        self.seg_len = int(20 * self.frame_rate / 1000)

        self.slide_len = int(self.seg_len/2)

        self.spectrogram = []


    def audio_spectrum(self, audio_slice):
        return np.fft.fft(audio_slice)

    def librosa_mfcc(self):
        y, self.sr = librosa.load(self.audio_path, sr=16000)
        # Let's make and display a mel-scaled power (energy-squared) spectrogram
        S = librosa.feature.melspectrogram(y, sr=self.sr, n_mels=128)

        # Convert to log scale (dB). We'll use the peak power (max) as reference.
        self.log_S = librosa.power_to_db(S, ref=np.max)

    def pysptk_mfcc(self):
        frame_length = 1024
        hop_length = 80

        # Note that almost all of pysptk functions assume input array is C-contiguous and np.float4 element type
        frames = librosa.util.frame(x, frame_length=frame_length, hop_length=hop_length).astype(np.float64).T

        # Windowing
        frames *= pysptk.blackman(frame_length)

        assert frames.shape[1] == frame_length


        # Order of mel-cepstrum
        order = 25
        alpha = 0.41

        mc = pysptk.mcep(frames, order, alpha)
        logH = pysptk.mgc2sp(mc, alpha, 0.0, frame_length).real
        librosa.display.specshow(logH.T, sr=self.sr, hop_length=hop_length, x_axis="time", y_axis="linear")
        colorbar()
        title("Spectral envelope estimate from mel-cepstrum")

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
    s = AudioSpectrogram("./clean_trainset_wav/a0001.wav")
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