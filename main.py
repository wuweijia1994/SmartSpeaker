#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_text as si
import play_audio as pa
import random
import os
from playsound import playsound

import time
from threading import Thread


# Create and launch a thread

global order
file_name = ["1.mp3", "2.mp3", "3.mp3", "4.mp3", "5.mp3"]
not_know = "good.mp3"

volumn = 0.1

while(True):
    # try:

    order = si.speech_recognition()
    # except si.sr.WaitTimeoutError:
    #     print("Wait for a long time")
    split_order = order.split()
    if(split_order[0] == "play"):
        pa.play_text(file_name[random.randint(0,3)], volumn)
        time.sleep(6)
        # if(split_order[1] == "1"):
        #     pa.play_text(file_name[0], volumn)
        #     time.sleep(7)
        # elif(split_order[1] == "2"):
        #     pa.play_text(file_name[1], volumn)
        #     time.sleep(7)
        # elif(split_order[1] == "3"):
        #     pa.play_text(file_name[2], volumn)
        #     time.sleep(7)
        # elif(split_order[1] == "4"):
        #     pa.play_text(file_name[3], volumn)
        #     time.sleep(7)
        # else:
        #     pa.play_text(file_name[4], volumn)
        #     time.sleep(7)
    elif(split_order[0] == "thank"):
        pa.play_text("thank.mp3")
        time.sleep(1)

    elif(split_order[0] == "higher"):
        if(volumn < 0.7):
            volumn += 0.3
        pa.play_text("ok.mp3", volume=volumn)
        time.sleep(1)
    elif(split_order[0] == "lower"):
        if(volumn > 0.3):
            volumn -= 0.3
        pa.play_text("ok.mp3", volume=volumn)
        time.sleep(1)
    else:
        pa.play_text(not_know, volumn)
        time.sleep(2)
    # else:
    #     # playsound(not_know)
    #     pa.play_text(not_know)
    #     print("Had played")
    #     # pa.play_text("I don't know what you said.")