import os
import pydub
import AudioSynthesis

class EchoMaker():
    def __init__(self, audio):
        self.audio = audio

    def set_period(self, period):
        self.period = period

    #time is miliseconds
    def make_echo(self, times):
        return pydub.AudioSegment.silent(duration=self.period * times).append(self.audio) - times*3

    def set_echo_times(self, times = 1):
        self.times = times

    def rebounce(self):
        for index in range(self.times):
            self.audio = self.audio.overlay(self.make_echo(index+1))

    def save(self, file_name = "echo.wav", format = "wav"):
        self.audio.export(file_name, format)

    def default_rebounce_save(self, file_name = "echo.wav", format = "wav"):
        self.set_period(100)
        self.set_echo_times(2)
        self.rebounce()
        self.save(file_name, format)

if __name__ == '__main__':
    file_path = "./noisy_trainset_wav"
    for file in AudioSynthesis.get_subfolders(file_path):
        audio = pydub.AudioSegment.from_file(os.path.join(file_path, file), "wav")
        echoed_audio = EchoMaker(audio)
        echoed_audio.default_rebounce_save(file_name=os.path.join(file_path, file))

    # First test
    # a = pydub.AudioSegment.from_mp3("../1.wav")
    # b = EchoMaker(a)
    # b.set_period(1000)
    # b.set_echo_times(2)
    # b.rebounce()
    # b.save()

