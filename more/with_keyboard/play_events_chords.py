import sys
import time

if len(sys.argv) < 2:
    print("Need a file name!")
    sys.argv.append(r"C:\Dropbox\Programming\python\midi\Sun Jul  1 07;48;11 2018")


# Считываем трек из файла
track = eval(open(sys.argv[1], "r").read())

import pygame.midi


pygame.midi.init()
MIDI_OUTPUT_ID = 6
player = pygame.midi.Output(MIDI_OUTPUT_ID)

# player.set_instrument(0) # Выбор инструмента


time_aspect = 0.3   # Коэффициент "замедления"

track = [x for x in track if x[1][0] == 144 and x[1][2] != 0]


last_time = track[0][0]
simple_track = []
while True:
    print("Начинаем играть")
    last_time = 0
    for time_stamp, event_bytes in track:

        pause = (time_stamp - last_time) / time_aspect

        if pause > 0.05:
            pause = 0.05
        elif pause > 0.025 and pause < 0.05:
            pause = 0.025
        else:
            pause = 0

        if pause > 0.02:
            print("____________________________________", pause)
            simple_track.append([])

        if pause > 0:
            input("press enter")
            # time.sleep(pause / time_aspect)

        last_time = time_stamp
        player.write_short(*event_bytes)
        print("events:", event_bytes)

        simple_track[-1].append(event_bytes[1])
        print("simple track:", simple_track)

    print("Ждем 10 сек перед повторением песенки")
    time.sleep(10)

    with open("note_numbers_850", "w") as f:
        f.write(str(simple_track))


del player
pygame.midi.quit()

