import librosa as li
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

from PIL import Image
import os


def draw_pic(path):
    plt.figure(figsize=(60,600))
    y, sr = li.load(path, mono=True)
    mel_sp = li.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=64)

    log_mel_spec = li.power_to_db(mel_sp, ref=np.max)
    t = log_mel_spec.shape[1]
    log_mel_spec = log_mel_spec[:, :t // 2]
    min_level_db=-100
    n = 2
    normalize = (log_mel_spec - min_level_db) / (-min_level_db)
    normalize = np.stack([normalize]*n, 1)
    normalize = np.reshape(normalize, [-1, t//2])

    mel_sp = np.flip(normalize, 0)
    mel_sp = (mel_sp - np.min(mel_sp)) / (np.max(mel_sp) - np.min(mel_sp))
    alphas = mel_sp + 0.
    alphas[alphas > 0.05] = 1
    print(np.min(mel_sp), np.max(mel_sp))
    #mel_sp = mel_sp[:, 96:]
    print(mel_sp.shape)
    plt.matshow(mel_sp, cmap="Greys")
    plt.axis('off')
    plt.savefig(path + ".png", bbox_inches='tight', pad_inches=0, dpi=1024)
    plt.close()


def test(folder):
    for sample in os.listdir(folder):
        sample_folder = os.path.join(folder, sample)
        path = os.path.join(sample_folder, "000.wav")
        draw_pic(path)


if __name__=="__main__":
    test("public/audios/001")

