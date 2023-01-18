import win32api
import sys
import time


from ctypes import windll, Structure, c_long, byref


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]



def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}



    pos = queryMousePosition()
    print(pos)



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

        if pause > 0:

            mouse_pos = queryMousePosition()
            while abs(mouse_pos["x"] - queryMousePosition()["x"]) < 500:
                pass
            
            
            mouse_x, mouse_y = queryMousePosition()["x"], queryMousePosition()["y"]


            if mouse_x < 500:
                win32api.SetCursorPos((100, mouse_y))
            elif mouse_x > 500:
                win32api.SetCursorPos((800, mouse_y))
    
            volume = round(128 * mouse_pos["y"] / 1000)
            if volume > 127: volume = 127

            
            # time.sleep(pause / time_aspect)

        last_time = time_stamp
        event_bytes[2] = volume
        player.write_short(*event_bytes)
        print(event_bytes, volume)

    print("Ждем 10 сек перед повторением песенки")
    time.sleep(10)

del player
pygame.midi.quit()

