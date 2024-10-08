import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

'''This works with the morse_code_wav.py file to decode the morse code from the sound.wav file generated by the morse_code_wav.py file.
Any other morse code sound file can not be used to decode the morse code. As it uses different logic to generate the morse code sound file.'''

'''First use morse_code_wav.py to generate the sound.wav file and then use this file to decode the morse code from the sound.wav file.'''

'''The morse_code_wav_decoder.py is created by me My LinkedIn: https://www.linkedin.com/in/tarun-kumar-s-676a74267/'''

'''The morse_code_wav.py is created by LinkedIn: https://www.linkedin.com/in/harish-jayaraj-p-60a189195/'''

# Define a dictionary to map Morse code to characters
morse_map_char = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', 
    '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', 
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', 
    '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', 
    '---..': '8', '----.': '9', '-----': '0', '/': ' '
}

# Read the WAV file
# wav_file = input("Enter the name of the wav file (with .wav): ")
wav_file = "sound.wav"
sample_rate, data = wavfile.read(wav_file)

# Select only the first channel if the data has multiple channels
if len(data.shape) > 1:
    data = data[:, 0]

# Normalize the data
data = data / np.max(np.abs(data))

# Subtract the minimum value for normalization
min_value = np.min(data)
normalized_data = data - min_value

# Scale data to [0, 1]
max_value = np.max(normalized_data)
normalized_data /= max_value

# Convert normalized data to a list of integers
normalized_integer_list = [int(num) for num in normalized_data]

#--------------------Plot the wav file------------------------

# time = np.arange(len(normalized_data)) / sample_rate
# plt.figure(figsize=(12, 6))
# plt.plot(time, normalized_data)
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.title('Normalized Waveform of the WAV File')
# plt.grid(True)
# plt.show()

#--------------------------------------------------------------

# Function to calculate intervals in the integer list
def calculate_intervals(lst):
    if not lst:
        return []
    
    intervals = []
    current_value = lst[0]
    current_count = 0

    for value in lst:
        if value == current_value:
            current_count += 1
        else:
            intervals.append((current_value, current_count))
            current_value = value
            current_count = 1

    intervals.append((current_value, current_count))
    return intervals

# Extract intervals
calculated_intervals = calculate_intervals(normalized_integer_list)

# Extract just the interval counts
extracted_intervals = [calculated_intervals[i][1] for i in range(len(calculated_intervals) - 1)]

# Remove the first interval if it's an anomaly (I dunno why there is 1 in first place)
if 1 in extracted_intervals:
    extracted_intervals.remove(1)

# Get unique, sorted intervals
unique_intervals = sorted(list(set(extracted_intervals)))

# Create a dictionary to map intervals to Morse code values
morse_code_map = {}
morse_values = ['.', '', '-', ',', '/']

for i in unique_intervals:
    morse_code_map[i] = morse_values[unique_intervals.index(i)]

# Decode Morse code from extracted intervals
decoded_data_lst = []
morse_data_str = ''

for j in extracted_intervals:
    if morse_code_map[j] == ',':
        decoded_data_lst.append(morse_data_str)
        morse_data_str = ''
    elif morse_code_map[j] == '/':
        decoded_data_lst.append(morse_data_str)
        decoded_data_lst.append("/")
        morse_data_str = ''
    else:
        morse_data_str += morse_code_map[j]
decoded_data_lst.append(morse_data_str)

# Decode Morse code into readable characters
decoded_message = ''
for k in decoded_data_lst:
    decoded_message += morse_map_char.get(k, k)

# Print the decoded Morse code and message
print("Decoded Message (Morse Code):", ' '.join(decoded_data_lst))
print("Decoded Message:", decoded_message.title())
