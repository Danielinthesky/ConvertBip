# analisar_audio.py
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import scipy.signal
import os
import pprint

def plot_waveform(audio_data, sr, output_path):
    plt.figure(figsize=(10, 4))
    plt.plot(np.arange(len(audio_data)) / sr, audio_data)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.savefig(output_path)
    plt.close()

def plot_spectrogram(audio_data, sr, output_path):
    X = librosa.stft(audio_data)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar()
    plt.title('Spectrogram')
    plt.savefig(output_path)
    plt.close()

def detect_beep_patterns(beep_durations):
    patterns = []
    diagnoses = []

    i = 0
    while i < len(beep_durations):
        if beep_durations[i] > 0.4:  # Bip longo
            if i + 2 < len(beep_durations) and all(beep_durations[i+1:i+3] < 0.3):
                patterns.append('1 bip longo seguido de 2 bips curtos')
                diagnoses.append('Problema na RAM')
                i += 3  # Pular os próximos 2 bips curtos
            elif i + 3 < len(beep_durations) and all(beep_durations[i+1:i+4] < 0.3):
                patterns.append('1 bip longo seguido de 3 bips curtos')
                diagnoses.append('Problema no vídeo')
                i += 4  # Pular os próximos 3 bips curtos
            else:
                i += 1
        else:
            i += 1

    return patterns, diagnoses

def analyze_beeps(audio_file):
    audio_data, sr = librosa.load(audio_file, sr=None)
    hop_length = 512
    frame_length = 1024
    energy = librosa.feature.rms(y=audio_data, frame_length=frame_length, hop_length=hop_length)[0]

    threshold_energy = np.median(energy) + np.std(energy)

    beep_indices = np.where(energy > threshold_energy)[0]

    beep_durations = []
    dominant_freqs = []
    energies = []
    beep_details = []

    for i in range(len(beep_indices)):
        start_sample = beep_indices[i] * hop_length
        end_sample = start_sample + frame_length

        if end_sample > len(audio_data):
            end_sample = len(audio_data)

        beep_data = audio_data[start_sample:end_sample]
        beep_duration = len(beep_data) / sr
        beep_durations.append(beep_duration)

        f, t, Sxx = scipy.signal.spectrogram(beep_data, sr)
        dominant_freq = f[np.argmax(Sxx, axis=0)]
        dominant_freqs.append(np.mean(dominant_freq))
        energies.append(np.sum(Sxx))

        beep_details.append({
            'duration': beep_duration,
            'dominant_freq': np.mean(dominant_freq),
            'energy': np.sum(Sxx),
            'peak_index': beep_indices[i]
        })

    patterns, diagnoses = detect_beep_patterns(np.array(beep_durations))

    waveform_path = f"{os.path.basename(audio_file).split('.')[0]}_waveform.png"
    spectrogram_path = f"{os.path.basename(audio_file).split('.')[0]}_spectrogram.png"
    plot_waveform(audio_data, sr, waveform_path)
    plot_spectrogram(audio_data, sr, spectrogram_path)

    return {
        'beep_durations': np.array(beep_durations),
        'dominant_freqs': np.array(dominant_freqs),
        'energy': np.array(energies),
        'num_beeps': len(beep_indices),
        'patterns': patterns,
        'diagnoses': diagnoses,
        'beep_details': beep_details,
        'waveform_path': waveform_path,
        'spectrogram_path': spectrogram_path
    }

def main():
    audio_files = [
        r'C:\Users\Danie\OneDrive\Documentos\Beep\amostras\1Curto_1Longo_3Curtos_3.wav',       
        r'C:\Users\Danie\OneDrive\Documentos\Beep\amostras\1Longo_2Curtos_1.wav',
        r'C:\Users\Danie\OneDrive\Documentos\Beep\amostras\1Longo_3Curtos_1.wav',
        r'C:\Users\Danie\OneDrive\Documentos\Beep\amostras\1Longo_3Curtos_2.wav',
        r'C:\Users\Danie\OneDrive\Documentos\Beep\amostras\1Longo_3Curtos_3.wav',
        r'C:\Users\Danie\OneDrive\Documentos\Beep\amostras\1longo-2curtos_3.wav',        
        r'C:\Users\Danie\OneDrive\Documentos\Beep\amostras\Bip_3bips_repetidos.wav'
    ]

    results = {}
    for audio_file in audio_files:
        results[audio_file] = analyze_beeps(audio_file)
    
    pprint.pprint(results)

if __name__ == "__main__":
    main()
