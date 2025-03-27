import os
import pandas as pd
import mido
from mido import MidiFile

def midi_note_to_name(note):
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (note // 12) - 1
    name = note_names[note % 12] + str(octave)
    return name

def process_midi_file(midi_path, output_folder):
    midi = MidiFile(midi_path)
    note_events = []
    
    note_on_times = {}  # Store note-on times to calculate duration
    current_time = 0
    
    for track in midi.tracks:
        for msg in track:
            current_time += msg.time  # Accumulate time in ticks
            
            if msg.type == 'note_on' and msg.velocity > 0:
                note_on_times[msg.note] = current_time
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in note_on_times:
                    note_on_time = note_on_times.pop(msg.note)
                    duration = current_time - note_on_time
                    note_name = midi_note_to_name(msg.note)
                    note_events.append([msg.note, note_name, note_on_time, current_time, duration, msg.velocity])
    
    df = pd.DataFrame(note_events, columns=['Note', 'Note Name', 'Start Time', 'End Time', 'Duration', 'Velocity'])
    output_csv_path = os.path.join(output_folder, os.path.basename(midi_path).replace('.mid', '.csv').replace('.midi', '.csv'))
    df.to_csv(output_csv_path, index=False)
    print(f"Processed {midi_path} -> {output_csv_path}")

def process_midi_folder(folder_path):
    output_folder = os.path.join(folder_path, "csv_outputs")
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.mid') or filename.endswith('.midi'):
            midi_path = os.path.join(folder_path, filename)
            process_midi_file(midi_path, output_folder)
    
    print(f"All CSV files saved in: {output_folder}")

if __name__ == "__main__":
    folder_path = os.getcwd()  # Set the folder path to the current working directory
    process_midi_folder(folder_path)
