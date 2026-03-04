"""
AUREON Microphone (System Audio Capture)
==========================================
100% ASCII -- will NOT crash on Windows cp1252.

Captures SYSTEM AUDIO OUTPUT (what is playing on your speakers).
NOT the physical microphone. Uses WASAPI loopback (pyaudiowpatch).

This is what lets AUREON hear podcasts from Spotify/YouTube.

Usage:
    from aureon_microphone import AureonMicrophone
    mic = AureonMicrophone()
    mic.start()
    # ... audio is being captured ...
    mic.stop()
    mic.save_to_wav("captured.wav")
"""
from __future__ import annotations
import wave
import time
import os
from typing import Optional, Callable, List
from pathlib import Path

# Try WASAPI loopback first (best), then standard pyaudio
_audio_lib = None
_WASAPI = False

try:
    import pyaudiowpatch as pyaudio
    _audio_lib = "pyaudiowpatch"
    _WASAPI = True
except ImportError:
    try:
        import pyaudio
        _audio_lib = "pyaudio"
    except ImportError:
        pyaudio = None
        _audio_lib = None


class AureonMicrophone:
    """
    Captures SYSTEM AUDIO (not physical mic).
    Uses WASAPI loopback to hear what the computer is playing.
    """

    def __init__(self, chunk_size: int = 1024):
        if pyaudio is None:
            raise ImportError(
                "No audio library found. Install: pip install pyaudiowpatch"
            )

        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_data: List[bytes] = []
        self.callback: Optional[Callable] = None

        # Find the right device
        self._device_index = None
        self._device_info = None
        self._sample_rate = 44100
        self._channels = 2
        self._format = pyaudio.paInt16
        self._sample_width = 2

        self._find_loopback_device()

    def _find_loopback_device(self):
        """Find WASAPI loopback or Stereo Mix device."""
        info = self.audio.get_host_api_info_by_index(0)

        # Method 1: WASAPI loopback (pyaudiowpatch only)
        if _WASAPI:
            try:
                wasapi_info = self.audio.get_host_api_info_by_type(
                    pyaudio.paWASAPI)
                for i in range(wasapi_info.get("deviceCount", 0)):
                    dev = self.audio.get_device_info_by_host_api_device_index(
                        wasapi_info["index"], i)
                    if dev.get("isLoopbackDevice", False):
                        self._device_index = dev["index"]
                        self._device_info = dev
                        self._sample_rate = int(dev.get("defaultSampleRate", 44100))
                        self._channels = max(int(dev.get("maxInputChannels", 2)), 1)
                        print("  [MIC] WASAPI loopback: " + dev.get("name", "?"))
                        return
            except Exception:
                pass

        # Method 2: Stereo Mix (standard pyaudio)
        device_count = self.audio.get_device_count()
        for i in range(device_count):
            try:
                dev = self.audio.get_device_info_by_index(i)
                name = dev.get("name", "").lower()
                if dev.get("maxInputChannels", 0) > 0:
                    if "stereo mix" in name or "what u hear" in name or "loopback" in name:
                        self._device_index = i
                        self._device_info = dev
                        self._sample_rate = int(dev.get("defaultSampleRate", 44100))
                        self._channels = max(int(dev.get("maxInputChannels", 2)), 1)
                        print("  [MIC] Stereo Mix: " + dev.get("name", "?"))
                        return
            except Exception:
                continue

        # Method 3: Fall back to default input (physical mic)
        try:
            default = self.audio.get_default_input_device_info()
            self._device_index = default["index"]
            self._device_info = default
            self._sample_rate = int(default.get("defaultSampleRate", 44100))
            self._channels = max(int(default.get("maxInputChannels", 1)), 1)
            print("  [MIC] WARNING: Using physical mic (no loopback found)")
            print("  [MIC] To capture system audio, enable Stereo Mix:")
            print("         Right-click speaker icon > Sounds > Recording")
            print("         Right-click > Show Disabled Devices")
            print("         Enable 'Stereo Mix'")
        except Exception:
            print("  [MIC] ERROR: No audio input device found")

    def start(self, callback: Optional[Callable] = None):
        """Start capturing system audio."""
        if self._device_index is None:
            print("  [MIC] No audio device available")
            return

        self.callback = callback
        self.is_recording = True
        self.audio_data = []

        def audio_callback(in_data, frame_count, time_info, status):
            if self.is_recording:
                if self.callback:
                    self.callback(in_data)
                self.audio_data.append(in_data)
            return (in_data, pyaudio.paContinue)

        try:
            self.stream = self.audio.open(
                format=self._format,
                channels=self._channels,
                rate=self._sample_rate,
                input=True,
                input_device_index=self._device_index,
                frames_per_buffer=self.chunk_size,
                stream_callback=audio_callback,
            )
            dev_name = self._device_info.get("name", "?") if self._device_info else "?"
            print("  [MIC] Capturing from: " + dev_name)
            print("  [MIC] Rate: " + str(self._sample_rate) + " Hz, "
                  + str(self._channels) + " channels")
        except Exception as e:
            print("  [MIC] Failed to start: " + str(e))
            self.is_recording = False

    def stop(self):
        """Stop capturing."""
        self.is_recording = False
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception:
                pass
        print("  [MIC] Stopped. " + str(len(self.audio_data)) + " chunks captured.")

    def save_to_wav(self, filename: str):
        """Save captured audio to WAV file."""
        if not self.audio_data:
            print("  [MIC] No audio data to save.")
            return

        try:
            wf = wave.open(filename, "wb")
            wf.setnchannels(self._channels)
            wf.setsampwidth(self._sample_width)
            wf.setframerate(self._sample_rate)
            wf.writeframes(b"".join(self.audio_data))
            wf.close()
            size_kb = os.path.getsize(filename) // 1024
            print("  [MIC] Saved: " + filename + " (" + str(size_kb) + " KB)")
        except Exception as e:
            print("  [MIC] Save failed: " + str(e))

    def terminate(self):
        """Clean up audio resources."""
        self.stop()
        try:
            self.audio.terminate()
        except Exception:
            pass

    def get_info(self):
        """Get device info."""
        return {
            "library": _audio_lib,
            "wasapi": _WASAPI,
            "device_index": self._device_index,
            "device_name": self._device_info.get("name", "?") if self._device_info else None,
            "sample_rate": self._sample_rate,
            "channels": self._channels,
            "is_loopback": _WASAPI and self._device_info and self._device_info.get("isLoopbackDevice", False),
        }


if __name__ == "__main__":
    print("=" * 60)
    print("  AUREON MICROPHONE -- SYSTEM AUDIO TEST")
    print("=" * 60)
    print("  Audio library: " + str(_audio_lib))
    print("  WASAPI loopback: " + str(_WASAPI))
    print("")

    if _audio_lib is None:
        print("  [FAIL] No audio library. Run: pip install pyaudiowpatch")
    else:
        mic = AureonMicrophone()
        info = mic.get_info()
        print("  Device: " + str(info.get("device_name", "?")))
        print("  Loopback: " + str(info.get("is_loopback", False)))
        print("")

        if info["device_index"] is not None:
            print("  Recording 10 seconds of system audio...")
            print("  Play something on Spotify/YouTube NOW!")
            print("")

            byte_count = [0]
            def on_audio(data):
                byte_count[0] += len(data)

            mic.start(callback=on_audio)
            try:
                for i in range(10):
                    time.sleep(1)
                    kb = byte_count[0] // 1024
                    print("  " + str(i + 1) + "s: " + str(kb) + " KB captured")
            except KeyboardInterrupt:
                pass

            mic.stop()
            if byte_count[0] > 1000:
                mic.save_to_wav("aureon_mic_test.wav")
                print("  [OK] Test complete. Check aureon_mic_test.wav")
            else:
                print("  [WARN] Very little audio captured.")
                print("  Make sure something is playing!")
            mic.terminate()
        else:
            print("  [FAIL] No suitable device found.")

    print("")
    print("=" * 60)
