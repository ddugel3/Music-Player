import librosa.display
import numpy as np
import matplotlib.pyplot as plt

audio_path = 'music/Piano-melody_1.wav'
y, sr = librosa.load(audio_path)

D = librosa.amplitude_to_db(librosa.stft(y[:1024]), ref=np.max)
plt.plot(D.flatten())
plt.show()
