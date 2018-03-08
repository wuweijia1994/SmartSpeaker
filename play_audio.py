import pyaudio
import wave
import time
 # Load the required library
from gtts import gTTS
import os



chunk = 1024


def play_song(file_name):
    wf = wave.open(file_name, 'rb')

    p = pyaudio.PyAudio()

    # 打开声音输出流
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # 写声音输出流进行播放
    while True:
        data = wf.readframes(chunk)
        if data == "": break
        stream.write(data)

    stream.close()
    p.terminate()

def play_text(tx, volume = 0.3):
    time.sleep(0.5)
    mixer.init()
    mixer.music.load(tx)
    mixer.music.set_volume(volume)
    mixer.music.play()
    time.sleep(0.5)