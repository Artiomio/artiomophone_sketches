import numpy as np
import pygame
from time import sleep


def midi2freq(midi_number):
  return 440 * 2 ** ((midi_number - 69) * (1./12.))



DISCR_FREQ = 44100
STEREO = 0

def play_freq(freq, duration, volume=127):
    DURATION = duration
    NOTE_FREQ = freq

    ARRAY_SIZE = int(DISCR_FREQ * DURATION * (STEREO + 1))

    t = np.linspace(0, DURATION, num=ARRAY_SIZE, dtype="float64")

    x =    np.exp(-2 * t ** 1.1 + 1) * (
              np.sin(t*10)) *(   np.sin(NOTE_FREQ * 2 * np.pi * t)
          #+ 0.2 * np.sin(1/12 * NOTE_FREQ * 2 * np.pi * t) 
          + 0.1 * np.sin(2 * NOTE_FREQ * 2 * np.pi * t) 
        + 0.01  * np.sin(4 * NOTE_FREQ * 2 * np.pi * t)
        + 0.001 * np.sin(8 * NOTE_FREQ * 2 * np.pi * t)  )
    


    scaled = np.int16(x / np.max(np.abs(x)) * (32767 * volume / 127))



    sound = pygame.sndarray.make_sound(scaled)
    sound.play()




def note_freq(latin_note, octave_number=0, w0=261.626):
    """ Возвращает частоты ноты, заданную латинским названием (C, D, E, F, G, A или B)
        w0 - "опорная" частота, по умолчанию частота ноты до первой (в центре клавиатура пианино) октавы
        octave_number: 0 соответствует первой октаве, -1 - малой октаве, etc
    """
    notes = {"c": 1, "d": 3, "e": 5, "f":6, "g": 8, "a": 10, "b": 12}
    latin_note = latin_note.lower()
    assert latin_note in notes
    n = notes[latin_note]
    return w0 * 2 ** ((n - 1) / 12.0 ) * 2 ** (octave_number)


    
"""
for ch in "cdefgab":
    play_freq(note_freq(ch), duration=1), sleep(0.62)

play_freq(note_freq("c", octave_number=1), duration=1), sleep(0.62)
play_freq(note_freq("c", octave_number=1), duration=1), sleep(0.62)

for ch in "cdefgab"[::-1]:
    play_freq(note_freq(ch, octave_number=0), duration=1), sleep(0.62)
"""



def note_on(midi_number, volume=127):
    play_freq(midi2freq(midi_number), duration=3, volume=volume) 




pygame.mixer.pre_init(DISCR_FREQ, size=-16, channels=1)
pygame.mixer.init()
 
pygame.mixer.set_num_channels(100)
