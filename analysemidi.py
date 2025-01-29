import os
import csv
from mido import MidiFile

# Directory containing MIDI files
midi_folder = "./midi"  # Replace with your folder path
output_csv = "midi_keypress_counts.csv"

# Function to count key presses (note-on events) in a MIDI file
def count_keypresses(midi_file_path):
    keypress_count = 0
    midi = MidiFile(midi_file_path)
    for track in midi.tracks:
        for msg in track:
            if msg.type == "note_on" and msg.velocity > 0:  # Note-on events with non-zero velocity
                keypress_count += 1
    return keypress_count

# Collect data from each MIDI file
midi_data = []
for filename in os.listdir(midi_folder):
    if filename.lower().endswith(".mid"):
        file_path = os.path.join(midi_folder, filename)
        keypress_count = count_keypresses(file_path)
        midi_data.append([filename, keypress_count])

# Write results to CSV
with open(output_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Keypress Count"])
    writer.writerows(midi_data)

print(f"Keypress counts saved to '{output_csv}'.")
