import os, platform, sys
import math, pygame, time, threading, random
from multiprocessing import Process, Array, Value
import multiprocessing, array

import pyaudio, sys, aubio
import numpy as np

# Modified from demo_pyaudio.py from aubio-0.4.4 demos

curFreq = Value('f', 0)

def startRecord():
    p = pyaudio.PyAudio()

    # open stream
    buffer_size = 1024*4
    pyaudio_format = pyaudio.paFloat32
    n_channels = 1
    samplerate = 44100
    stream = p.open(format=pyaudio_format,
                    channels=n_channels,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=buffer_size)

    if len(sys.argv) > 1:
        # record 5 seconds
        output_filename = sys.argv[1]
        record_duration = 5 # exit 1
        outputsink = aubio.sink(sys.argv[1], samplerate)
        total_frames = 0
    else:
        # run forever
        outputsink = None
        record_duration = None

    # setup pitch
    tolerance = 0.8
    win_s = 4096 # fft size
    hop_s = buffer_size # hop size
    pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    print("*** starting recording")
    while True:
        try:
            audiobuffer = stream.read(buffer_size)
            signal = np.fromstring(audiobuffer, dtype=np.float32)

            pitch = pitch_o(signal)[0]
            confidence = pitch_o.get_confidence()

            curFreq.value = pitch

            if outputsink:
                outputsink(signal, len(signal))

            if record_duration:
                total_frames += len(signal)
                if record_duration * samplerate < total_frames:
                    break
        except KeyboardInterrupt:
            print("*** Ctrl+C pressed, exiting")
            break

    print("*** done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()

if platform.system() == "Windows":
    t = threading.Thread(target=startRecord, args=())
else:
    t = multiprocessing.Process(target=startRecord)

def runThread():
    t.start()

def terminate():
    t.terminate()
