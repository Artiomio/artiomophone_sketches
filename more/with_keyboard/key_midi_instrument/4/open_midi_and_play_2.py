#/usr/bin/python3
import random
import sys
import time
random.seed(time.time())

from instrument_draft_01_precalculated_sounds import play_precalculated_note

import pygame.midi
import mido

THRESHOLD = 0.3

if len(sys.argv) > 1:
    mid = mido.MidiFile(sys.argv[1])
else:    
    import glob
    file_name = random.choice(glob.glob("../*.mid"))

    print("Midi file not specified, trying this file: ", file_name)
    mid = mido.MidiFile(file_name)


pygame.midi.init()
#player = pygame.midi.Output(4)
#player.set_instrument(0)

last_time_note_player = time.time()

for msg in mid.play():
    midi_bytes = msg.bytes()

    if len(midi_bytes) > 1:
        print(msg, f"Время={msg.time}", midi_bytes)

        if time.time() - last_time_note_player > THRESHOLD and midi_bytes[2]:
            input("Press Enter ")

        #player.write_short(*midi_bytes)
        play_precalculated_note(midi_bytes[1], 50)

        last_time_note_player = time.time()
#    time.sleep(msg.time)

#del player
#pygame.midi.quit()