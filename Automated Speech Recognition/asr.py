from vosk import Model, KaldiRecognizer
import pyaudio


import time
start_time = time.time()
#model = Model("/home/szm/Documents/Uni_Stuff/FYP/ASR/vosk-model-en-us-0.22-lgraph")
model = Model("/home/szm/Documents/Uni_Stuff/FYP/ASR/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)
print("--- %s seconds for loading model ---" % (time.time() - start_time))

#REcognize from microphone
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    start_time2 = time.time()
    data = stream.read(4096)
    # if len(data) == 0:
    #     break
    if recognizer.AcceptWaveform(data):
        print(recognizer.Result())
        print("--- %s seconds for obtaining transcript ---" % (time.time() - start_time2))

