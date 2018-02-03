import pydub
import numpy as np
import array
import os

shower_audio_path = "/Users/weijiawu/Documents/GitHub/SmartSpeaker/audio"
normal_audio_path = "/Users/weijiawu/Documents/GitHub/SmartSpeaker/ProcessDataset/wav"

def get_subfolders(dir):
    if os.path.exists(dir):
        filtered_dir = os.listdir(dir)
        #special for MAC
        if(filtered_dir.count(".DS_Store") > 0):
            filtered_dir.remove(".DS_Store")
        return filtered_dir
    else:
        print("There is no such directory: " + dir)
        return ""

def get_array_from_audio(file_path, format):
    file = pydub.AudioSegment.from_file(file_path, format=format)
    # file.frame_rate = 16000
    data = np.fromstring(file._data, np.int16)
    return data

def mix_single_audio(normal_audio, noise_audio):
    normal_length = len(normal_audio)
    noise_length = len(noise_audio)

    while(normal_length > noise_length):
        noise_audio = noise_audio.append(noise_audio)
        noise_length = len(noise_audio)

    revised_noise_audio = noise_audio[0:normal_length]
    return revised_noise_audio.overlay(normal_audio)

def save_audio(common_path, noise_name, file_name, audio):
    origin_audio = pydub.AudioSegment.from_file(os.path.join(common_path, file_name), format="wav")
    # audio_array = array.array(origin_audio.array_type, audio.astype(int))
    # new_audio = origin_audio._spawn(audio_array)

    noise_path = os.path.join("./mix/", os.path.splitext(noise_name)[0])
    build_directory(noise_path)
    output_file_path = os.path.join(noise_path, file_name)
    audio.export(output_file_path, format='wav')

def build_directory(file_path):
    if not(os.path.exists(file_path)):
        os.mkdir(file_path)
        print("Build up directory successfully: " + file_path)
    else:
        print("This directory has been built: " + file_path)

def mix_all_audio(noise_audio_path, normal_audio_path):
    mix_dir = "./mix/"
    build_directory(mix_dir)
    normal_wav_files = get_subfolders(normal_audio_path)
    shower_mp3_files = get_subfolders(noise_audio_path)
    for shower_file in shower_mp3_files:
        for normal_file in normal_wav_files:
            normal_audio = pydub.AudioSegment.from_file(os.path.join("wav", normal_file), format="wav")
            noise_audio = pydub.AudioSegment.from_file(os.path.join(os.pardir, "audio", shower_file), format="mp3")
            mix_audio = mix_single_audio(normal_audio, noise_audio)
            save_audio("./wav/", shower_file, normal_file, mix_audio)

if __name__ == '__main__':
    mix_all_audio(shower_audio_path, normal_audio_path)
#读取mp3
song_file = pydub.AudioSegment.from_mp3('1.mp3')
#转换成数字矩阵
song_data = np.fromstring(song_file._data, np.int16)

water_file = pydub.AudioSegment.from_mp3('./audio/Having A Shower.mp3')
water_data = np.fromstring(water_file._data, np.int16)

clean_file = pydub.AudioSegment.from_file('./_caustic_-20170306-smy/wav/en-0185.wav', format='wav')
clean_data = np.fromstring(clean_file._data, np.int16)
half = water_data[0:len(song_data)]

synthesis_data = song_data/2 + half/2
synthesis_data_array = array.array(song_file.array_type, synthesis_data.astype(int))
new_song = song_file._spawn(synthesis_data_array)
new_song.export('./new_1.mp3', format = 'mp3')

a = 1


#required libraries
import urllib
import scipy.io.wavfile
import pydub

#read mp3 file
mp3 = pydub.AudioSegment.from_mp3("1.mp3")
#convert to wav
mp3.export("1.wav", format="wav")
#read wav file
rate,audData=scipy.io.wavfile.read("1.wav")

print(rate)
print(audData)