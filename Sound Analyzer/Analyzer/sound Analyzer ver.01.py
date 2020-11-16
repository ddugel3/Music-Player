import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

wav = '../../music/Piano-melody_1.wav'
(file_dir, file_id) = os.path.split(wav)
print("file_dir:", file_dir)
print("file_id:", file_id)
y, sr = librosa.load(wav, sr=10000)
time = np.linspace(0, len(y)/sr, len(y)) # time axis

fig, ax = plt.subplots() # plot
ax.plot(time, y, color = 'b', label='speech waveform')

ax.set_ylabel("Amplitude") # y 축
ax.set_xlabel("Time [s]") # x 축

plt.savefig("../Analyzed/ver.01/"+file_id+'_Waveform'+'.png')

plt.show()