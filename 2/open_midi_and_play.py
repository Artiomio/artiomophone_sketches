#/usr/bin/python3
import random
import sys
import time
from instrument_draft_01_precalculated_sounds import play_precalculated_note

import pygame.midi
import mido

THRESHOLD = 0.1

if len(sys.argv) > 1:
    mid = mido.MidiFile(sys.argv[1])
else:    
    import glob
    file_name = random.choice(glob.glob("*.mid"))

    print("Midi file not specified, trying this file: ", file_name)
    mid = mido.MidiFile(file_name)


pygame.midi.init()
#player = pygame.midi.Output(4)
#player.set_instrument(0)

last_time_note_player = time.time()


midi_bytes_list = []
for msg in mid.play():
    midi_bytes = msg.bytes()

    if len(midi_bytes) > 1:
        print(msg, f"Время={msg.time}", midi_bytes); midi_bytes_list.append(midi_bytes)

        if time.time() - last_time_note_player > THRESHOLD and midi_bytes[2]:
            pass
        #player.write_short(*midi_bytes)
        play_precalculated_note(midi_bytes[1], 10)

        last_time_note_player = time.time()
#    time.sleep(msg.time)

import json
json.dump(midi_bytes_list, open("list_of_notes.txt", 'w'))
#del player
#pygame.midi.quit()