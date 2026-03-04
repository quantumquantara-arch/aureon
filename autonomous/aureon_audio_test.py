import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import pycaw
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Audio loopback test - capture system audio and play it back
print("Starting audio loopback test...")

# Get default audio device
devices = AudioUtilities.GetSpeakers()
device = devices.GetAudioEndpointVolume()

# Set up audio parameters
sample_rate = 44100
duration = 5  # seconds

# Capture audio from system
print(f"Recording {duration} seconds of system audio...")
recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype='int16')
time.sleep(duration)

# Stop recording
sd.stop()
print("Recording complete.")

# Playback the captured audio
print("Playing back captured audio...")
sd.play(recording, sample_rate)
time.sleep(duration)

print("Audio loopback test complete.")
print("If you heard your own audio played back, the loopback is working!")