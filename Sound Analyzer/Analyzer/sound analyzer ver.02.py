import os
import numpy as np
import librosa, librosa.display
import matplotlib.pyplot as plt
FIG_SIZE = (15,10)

file = "../../music/Piano-melody_1.wav"
(file_dir, file_id) = os.path.split(file)

sig, sr = librosa.load(file, sr=22050)
print(sig,sig.shape)

#Waveform 시각화
plt.figure(figsize=FIG_SIZE)
librosa.display.waveplot(sig, sr, alpha=0.5)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Waveform")
fft = np.fft.fft(sig)
plt.savefig("../Analyzed/ver.02/"+file_id+'_Waveform'+'.png')

#-------------------------------------------------------------------#

# 단순 푸리에 변환 → Spectrum
# 복소공간 값 절댓갑 취해서, magnitude 구하기
magnitude = np.abs(fft)
# Frequency 값 만들기
f = np.linspace(0,sr,len(magnitude))
# 푸리에 변환을 통과한 specturm은 대칭구조로 나와서 high frequency 부분 절반을 날려고 앞쪽 절반만 사용한다.
left_spectrum = magnitude[:int(len(magnitude)/2)]
left_f = f[:int(len(magnitude)/2)]
plt.figure(figsize=FIG_SIZE)
plt.plot(left_f, left_spectrum)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.title("Power spectrum")
plt.savefig("../Analyzed/ver.02/"+file_id+'_Frequency-Spectrum'+'.png')

#-------------------------------------------------------------------#

# STFT -> spectrogram
hop_length = 512  # 전체 frame 수
n_fft = 2048  # frame 하나당 sample 수
# calculate duration hop length and window in seconds
hop_length_duration = float(hop_length)/sr
n_fft_duration = float(n_fft)/sr
# STFT
stft = librosa.stft(sig, n_fft=n_fft, hop_length=hop_length)
# 복소공간 값 절댓값 취하기
magnitude = np.abs(stft)
# magnitude > Decibels
log_spectrogram = librosa.amplitude_to_db(magnitude)
# display spectrogram
plt.figure(figsize=FIG_SIZE)
librosa.display.specshow(log_spectrogram, sr=sr, hop_length=hop_length)
plt.xlabel("Time")
plt.ylabel("Frequency")
plt.colorbar(format="%+2.0f dB")
plt.title("Spectrogram (dB)")
plt.savefig("../Analyzed/ver.02/"+file_id+'_Spectrogram'+'.png')


plt.show()