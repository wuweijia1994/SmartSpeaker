import sys
sys.path.append('../../snowboy/examples/Python')
sys.path.append('../../snowboy')
sys.path.append('./cloud-client')
sys.path.append('../')

import client

cnt = client.RaspConnection()
cnt.connect()
cnt.send_commands('1')

import time
import speech_text as si
import play_audio as pa
import random
from pygame import mixer
file_name = ["1.mp3", "2.mp3", "3.mp3", "4.mp3", "5.mp3"]
not_know = "good.mp3"

volume = 0.3

mixer.init()

import snowboydecoder
import snowboythreaded
import signal
import speech_recognition as sr
import os
import threading
import vad
import transcribe
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/weijiawu/Documents/GitHub/SmartSpeaker/GoogleSpeechRecognition/SmartSpeaker-52c5ddbd2e5c.json"

from enum import Enum
CMD= Enum('CMD', ('PLAY', 'NEXT', 'STOP', "HIGH", 'LOW', 'IDLE'))

command = CMD.IDLE

interrupted = False

def audioRecorderCallback(fname):
    global command
    global cnt
    cnt.send_commands('3')
    print("converting audio to text")
    voice_cmd = transcribe.transcribe_file(fname).upper()
    for cmd in CMD:
        if voice_cmd.find(cmd.name)!=-1:
            command = cmd
            break

    print(voice_cmd)

    # snowboydecoder.play_audio_file(fname)
    # print(fname)
    # r = sr.Recognizer()
    # with sr.AudioFile(fname) as source:
    #     audio = r.record(source)  # read the entire audio file
    # # recognize speech using Google Speech Recognition
    # try:
    #     # for testing purposes, we're just using the default API key
    #     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    #     # instead of `r.recognize_google(audio)`
    #     print(r.recognize_google(audio))
    # except sr.UnknownValueError:
    #     print "Google Speech Recognition could not understand audio"
    # except sr.RequestError as e:
    #     print "Could not request results from Google Speech Recognition service; {0}".format(e)
    if mixer.music.get_busy() & (command != CMD.STOP) & (command != CMD.NEXT):
        mixer.music.unpause()

    os.remove(fname)

def detectedCallback():
    global cnt
    cnt.send_commands('2')
    sys.stdout.write("recording audio...")
    if mixer.music.get_busy():
        mixer.music.pause()

  # vad.voice_activity_detect()

    sys.stdout.flush()

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def detected_callback():
    # vad
    # nlp
    # change cmd global cmd
     print ("hotword detected")

# detector = snowboydecoder.HotwordDetector("/Users/weijiawu/Documents/GitHub/snowboy/resources/models/snowboy.umdl", sensitivity=0.7, audio_gain=1)

threaded_detector = snowboythreaded.ThreadedDetector("/Users/weijiawu/Documents/GitHub/snowboy/resources/models/snowboy.umdl", sensitivity=0.7, audio_gain=1)
# print("Listening... Press Ctrl+C to exit")
# print(detector.detector.SampleRate())
# args =（detectedCallback, interrupt_callback, 0.05, audioRecorderCallback, 15, 50)


threaded_detector.start()

print('Listening... Press Ctrl+C to exit')

# main loop
threaded_detector.start_recog(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               # interrupt_check=interrupt_callback,
               sleep_time=0.05,
               recording_timeout=50)

# t = threading.Thread(target=detector.start,（detectedCallback, interrupt_callback, 0.05, audioRecorderCallback, 15, 50))
# t.start()
# detector.start(detected_callback=detectedCallback,
#                audio_recorder_callback=audioRecorderCallback,
#                interrupt_check=interrupt_callback,
#                sleep_time=0.05,
#                recording_timeout=50)

file_num = 1
while True:
    cnt.send_commands('1')
    if command == CMD.PLAY:
        mixer.music.load(file_name[file_num])
        mixer.music.set_volume(volume)
        mixer.music.play()
        time.sleep(5)
        command = CMD.IDLE
        #play music
    elif command == CMD.NEXT:
        mixer.music.stop()
        if file_num == 4:
            file_num = 0
        else:
            file_num = file_num + 1
        mixer.music.load(file_name[file_num])
        mixer.music.set_volume(volume)
        mixer.music.play()
        time.sleep(5)
        command = CMD.IDLE
        #next play
    elif command == CMD.STOP:
        #stop
        mixer.music.stop()
        time.sleep(1)
        cnt.send_commands('4')
        command = CMD.IDLE
    elif command == CMD.HIGH:
        #higher volume
        if(volume < 0.7):
            volume += 0.2
        # mixer.music.stop()
        mixer.music.set_volume(volume)
        # mixer.music.play()
        command = CMD.IDLE
        time.sleep(1)
    elif command == CMD.LOW:
        #lower volume
        if(volume > 0.3):
            volume -= 0.2
        # mixer.music.stop()
        mixer.music.set_volume(volume)
        # mixer.music.play()
        command = CMD.IDLE
    time.sleep(6)

