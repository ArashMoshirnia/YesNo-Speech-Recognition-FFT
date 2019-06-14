from scipy.io import wavfile as wav
from scipy.fftpack import fft
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt


# audio config params
FORMAT = pyaudio.paInt16  # format of sampling 16 bit int
CHANNELS = 1  # number of channels it means number of sample in every sampling
RATE = 44100  # number of  sample in 1 second sampling
CHUNK = 1024  # length of every chunk
RECORD_SECONDS = 1.5  # time of recording in seconds
WAVE_OUTPUT_FILENAME = "file.wav"  # file name


audio = pyaudio.PyAudio()

print("recording...")
while True:
    # start Recording
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    # print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # reading voice
    rate, data = wav.read('file.wav')

    vc = np.fft.fft(data)
    abs_vc = np.absolute(vc)
    abs_vc = abs_vc[0:int(len(abs_vc)/2)]

    upper7000 = 0
    below7000 = 0
    below5000 = 0
    below3000 = 0
    total_energy = np.sum(abs_vc)

    for i in range(len(abs_vc)) :
        if i<3000 :
            below3000 += abs_vc[i]

        elif i<5000 and i>3000 :
            below5000 += abs_vc[i]

        elif i<7000 and i>5000:
            below7000 += abs_vc[i]

        elif i>7000:
            upper7000 += abs_vc[i]

    upper7000Rate = upper7000 / total_energy
    below7000Rate = below7000 / total_energy
    below5000Rate = below5000 / total_energy
    below3000Rate = below3000 / total_energy

    print(below3000Rate)
    print(below5000Rate)
    print(below7000Rate)
    print(upper7000Rate)

    print(upper7000)
    print(below7000)

    if below3000Rate + below5000Rate > 0.85 :
        print("NO")
    elif upper7000<100000000 and below7000<100000000 :
        print("MUTE")
    elif upper7000Rate + below7000Rate + below5000Rate > 0.50 :
        print("YES")



    print('-----------')

    # plt.plot(abs_vc)
    # plt.show()


audio.close()
