import numpy as np
import torch
import ProcessDataset.AudioSynthesis
import os
from sklearn.preprocessing import normalize

from torch.utils.data import Dataset

class audio_dataset(Dataset):
    def __init__(self, input_dir, label_dir, num_spc = 5, transform=None):
        """
        Args:
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.input_dir = input_dir
        self.label_dir = label_dir
        self.transform = transform

        self.input_audio = np.log(abs(np.load(self.input_dir)))
        # self.input_audio = normalize(self.input_audio)

        self.label_audio = np.log(abs(np.load(self.label_dir)))
        # self.label_audio = normalize(self.label_audio)

        self.num_spc = num_spc
        self.shape_label = self.label_audio.shape

        # self.input_files = ProcessDataset.AudioSynthesis.get_subfolders(self.input_dir)
        # self.label_files = ProcessDataset.AudioSynthesis.get_subfolders(self.label_dir)
    def __len__(self):
        # shape_input = self.input_audio.shape
        return self.shape_label[0] - (2*self.num_spc)

    def __getitem__(self, idx):
        sample = {'input': torch.from_numpy(abs(self.input_audio[idx:idx+2*self.num_spc+1,0:int(self.shape_label[1]/2+1)])).float(),\
                  'label': torch.from_numpy(abs(self.label_audio[idx+self.num_spc, 0:int(self.shape_label[1]/2+1)])).float()}

        if self.transform:
            sample = self.transform(sample)

        return sample

if __name__ == '__main__':
    a = audio_dataset("./ProcessDataset/small_mix_npy/a0001.npy", "./ProcessDataset/small_wav_npy/a0001.npy")
    b = a.__len__()
    c = a.__getitem__(0)
    d = a.__getitem__(a.__len__()-1)
    b = 1