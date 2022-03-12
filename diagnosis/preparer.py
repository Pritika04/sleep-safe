# import required module
import os
import math, random
import torch
import torchaudio
from torchaudio import transforms
from IPython.display import Audio
import torchvision.transforms as T
from PIL import Image
import numpy as np

# assign directory
directory = 'D:\\Documents\\python projects\\sleepDiagnosis\\Respiratory_Sound_Database\\Respiratory_Sound_Database\\audio_and_txt_files'
 
def open(audio_file):
    sig, sr = torchaudio.load(audio_file)
    return (sig, sr)

# def rechannel(aud, new_channel):
#     sig, sr = aud

#     if (sig.shape[0] == new_channel):
#       # Nothing to do
#       return aud

#     if (new_channel == 1):
#       # Convert from stereo to mono by selecting only the first channel
#       resig = sig[:1, :]
#     else:
#       # Convert from mono to stereo by duplicating the first channel
#       resig = torch.cat([sig, sig])

#     return ((resig, sr))

def pad_trunc(aud, max_ms):
    sig, sr = aud
    num_rows, sig_len = sig.shape
    max_len = sr//1000 * max_ms

    if (sig_len > max_len):
      # Truncate the signal to the given length
      sig = sig[:,:max_len]

    elif (sig_len < max_len):
      # Length of padding to add at the beginning and end of the signal
      pad_begin_len = random.randint(0, max_len - sig_len)
      pad_end_len = max_len - sig_len - pad_begin_len

      # Pad with 0s
      pad_begin = torch.zeros((num_rows, pad_begin_len))
      pad_end = torch.zeros((num_rows, pad_end_len))

      sig = torch.cat((pad_begin, sig, pad_end), 1)
      
    return (sig, sr)

def spectro_gram(aud, n_mels=64, n_fft=1024, hop_len=None):
    sig,sr = aud
    top_db = 80

    # spec has shape [channel, n_mels, time], where channel is mono, stereo etc
    spec = transforms.MelSpectrogram(sr, n_fft=n_fft, hop_length=hop_len, n_mels=n_mels)(sig)

    # Convert to decibels
    spec = transforms.AmplitudeToDB(top_db=top_db)(spec)
    return (spec)

newLabels = np.empty((920,2))

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        if f.endswith('.wav'):
            print(f)
            aud = open(f)
            aud = pad_trunc(aud, 15000)
            sig, sr = aud
            print(sig, sr)
            spec = spectro_gram(aud)
            print(spec)
            print(spec.shape)
            transform = T.ToPILImage()
            img = transform(spec)
            img = img.resize((118,64), resample=0)