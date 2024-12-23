from pydub import AudioSegment
import librosa
import numpy as np
import matplotlib.pyplot as plt

# Convert video file to .wav audio
#audio = AudioSegment.from_file("linea_bajo.mov", format="mov")
#audio.export("audio.wav", format="wav")

# Load the audio file
audio_path = "audio.wav"
y, sr = librosa.load(audio_path, sr=None)  # y = audio data, sr = sample rate

# Perform a Short-Time Fourier Transform (STFT) to extract frequencies
stft = np.abs(librosa.stft(y))
frequencies = librosa.fft_frequencies(sr=sr)

# Identify contrabass frequency range (41 Hz to 220 Hz)
contrabass_freqs = frequencies[(frequencies >= 41) & (frequencies <= 220)]
print("Contrabass freqs are: ", contrabass_freqs)

# Get the time-varying energy in this range
contrabass_energy = stft[(frequencies >= 41) & (frequencies <= 220), :]


# Convert Frequencies to Notes
notes = [librosa.hz_to_note(freq) for freq in contrabass_freqs]
print("Notes are: ", notes)

# Create a Note Chart
# Calculate time for each frame
times = librosa.frames_to_time(np.arange(contrabass_energy.shape[1]), sr=sr)

# Plot the energy of the contrabass frequencies over time
plt.figure(figsize=(10, 6))
plt.plot(times, np.sum(contrabass_energy, axis=0))
plt.xlabel("Time (s)")
plt.ylabel("Energy")
plt.title("Contrabass Energy Over Time")
plt.show()

# Save the Chart
plt.savefig("contrabass_chart.png")