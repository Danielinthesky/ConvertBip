
import numpy as np
import librosa
import scipy.signal
import os

def apply_bandpass_filter(data, sr, lowcut=1000, highcut=2000):
    nyquist = 0.5 * sr
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = scipy.signal.butter(2, [low, high], btype="band")
    return scipy.signal.filtfilt(b, a, data)

def detect_beep_patterns(beep_durations):
    patterns = []
    diagnoses = []

    i = 0
    while i < len(beep_durations):
        if beep_durations[i] > 0.4:  # Bip longo
            if i + 3 < len(beep_durations) and all(d < 0.3 for d in beep_durations[i+1:i+4]):
                patterns.append('1 bip longo seguido de 3 bips curtos')
                diagnoses.append('Problema no vídeo')
                i += 4  # Pular os próximos 3 bips curtos
            else:
                i += 1
        elif beep_durations[i] <= 0.2:
            if len(beep_durations) == 1:
                patterns.append('PC Energizado')
                diagnoses.append('Bip curto isolado')
            i += 1
        else:
            i += 1
            
    return patterns, diagnoses

def analyze_beeps(audio_file):
    audio_data, sr = librosa.load(audio_file, sr=None)
    filtered_audio = apply_bandpass_filter(audio_data, sr)

    hop_length = 512
    frame_length = 1024
    energy = librosa.feature.rms(y=filtered_audio, frame_length=frame_length, hop_length=hop_length)[0]
    threshold_energy = np.median(energy) + np.std(energy)

    beep_indices = np.where(energy > threshold_energy)[0]

    beep_durations = []
    for i in range(len(beep_indices)):
        start_sample = beep_indices[i] * hop_length
        end_sample = start_sample + frame_length
        if end_sample > len(filtered_audio):
            end_sample = len(filtered_audio)
        beep_data = filtered_audio[start_sample:end_sample]
        beep_durations.append(len(beep_data) / sr)

    patterns, diagnoses = detect_beep_patterns(np.array(beep_durations))
    
    return {
        'beep_durations': np.array(beep_durations),
        'num_beeps': len(beep_indices),
        'patterns': patterns,
        'diagnoses': diagnoses,
    }
