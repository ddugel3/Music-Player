import scipy.io.wavfile

# 초당 샘플링 데이터 수
sampling_rate = 44100
sp.io.wavfile.write(".wav", sampling_rate, octave)

sr, y_read = sp.io.wavfile.read("octave.wav")
# sr == sampling_rate

plt.plot(y_read[40000:50000])
plt.show()


