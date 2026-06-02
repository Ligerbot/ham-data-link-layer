#This "library" was made completely by claude. There are no good tone generator libraries out there.
import numpy as np
import sounddevice as sd

FS = 44100

def play(frequency, duration_ms):
    t = np.linspace(0, duration_ms / 1000, int(FS * duration_ms / 1000))
    wave = np.sin(2 * np.pi * frequency * t).astype(np.float32)
    sd.play(wave, FS)
    sd.wait()

def listen(target_freq, duration_ms=100, tolerance=50):
    samples = sd.rec(int(FS * duration_ms / 1000), samplerate=FS, channels=1, dtype='float32')
    sd.wait()
    fft = np.abs(np.fft.rfft(samples[:, 0]))
    freqs = np.fft.rfftfreq(len(samples[:, 0]), 1 / FS)
    peak = freqs[np.argmax(fft)]
    return abs(peak - target_freq) < tolerance
