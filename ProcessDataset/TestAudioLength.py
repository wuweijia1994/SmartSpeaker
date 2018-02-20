import pydub
import os
import AudioSynthesis

noisy_dir = "./noisy_trainset_wav"
clean_dir = "./clean_trainset_wav"

for audio_file in AudioSynthesis.get_subfolders(noisy_dir):
    n = pydub.AudioSegment.from_file(os.path.join(noisy_dir, audio_file), "wav")
    c = pydub.AudioSegment.from_file(os.path.join(clean_dir, audio_file), "wav")

    if(n.duration_seconds != c.duration_seconds):
        print("GG")
    else:
        print("hahahaha")