import numpy as np
from scipy.io.wavfile import write

# Set parameters
freq = 2000
sampling = 32000

# Define time periods and generate waveforms
dot_time_period = 0.1
dot_samples = int(sampling * dot_time_period)
dot_wave = np.cos(2 * np.pi * freq * np.linspace(0, dot_time_period, dot_samples))

dash_time_period = 0.2
dash_samples = int(sampling * dash_time_period)
dash_wave = np.cos(2 * np.pi * freq * np.linspace(0, dash_time_period, dash_samples))

space_time_period = 0.3
space_samples = int(sampling * space_time_period)
space_wave = np.cos(2 * np.pi * 1e-6 * np.linspace(0, space_time_period, space_samples))

interval_time_period = 0.1
interval_samples = int(sampling * interval_time_period)
interval_wave = np.cos(2 * np.pi * 1e-6 * np.linspace(0, interval_time_period, interval_samples))

# Morse code lookup table
morse_code_map = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': '/'
}

# Get input sentence from the user
input_sentence = input('Enter a sentence: ').upper()

# Convert the input sentence to Morse code
word = ''  # Initialize the Morse code string
for char in input_sentence:
    if char in morse_code_map:
        word += morse_code_map[char] + ' '  # Append Morse code and a space

print(f'Morse Code: {word}')

# Encoder
wave = np.array([])

for char in word:
    if char == '.':
        wave = np.concatenate((wave, dot_wave, interval_wave))
    elif char == '-':
        wave = np.concatenate((wave, dash_wave, interval_wave))
    elif char == ' ':
        wave = np.concatenate((wave, interval_wave, interval_wave))
    elif char == '/':
        wave = np.concatenate((wave, space_wave))

# Save the Morse code sound to a WAV file
filename = 'sound.wav'
write(filename, sampling, wave.astype(np.float32))
