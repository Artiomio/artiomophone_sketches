import numpy as np
import pygame
from time import sleep


def midi2freq(midi_number):
  return 440 * 2 ** ((midi_number - 69) * (1./12.))



DISCR_FREQ = 44100
STEREO = 0

PRECALCULATED_SOUND_DURATION = 3


"""
def play_freq(freq, duration):
    DURATION = duration
    NOTE_FREQ = freq

    ARRAY_SIZE = int(DISCR_FREQ * DURATION * (STEREO + 1))

    t = np.linspace(0, DURATION, num=ARRAY_SIZE)
    x = np.exp(-t*2) * (np.sin(NOTE_FREQ * 2*np.pi * t) + 0.1*np.sin( 2 * NOTE_FREQ * 2*np.pi * t) 
            + 0.001*np.sin( 3 * NOTE_FREQ * 2*np.pi * t))

    scaled = np.int16(x / np.max(np.abs(x)) * 32767)



    sound = pygame.sndarray.make_sound(scaled)
    sound.play()
"""



def note_freq(latin_note, octave_number=0, w0=261.626):
    """ Возвращает частоты ноты, заданную латинским названием (C, D, E, F, G, A или B)
        w0 - "опорная" частота, по умолчанию частота ноты до первой (в центре клавиатура пианино) октавы
        octave_number: 0 соответствует первой октаве, -1 - малой октаве, etc
    """
    notes = {"c": 1, "d": 3, "e": 5, "f":6, "g": 8, "a": 10, "b": 12}
    latin_note = latin_note.lower()
    assert latin_note in notes
    n = notes[latin_note]
    return w0 * 2 ** ((n - 1) / 12 ) * 2 ** (octave_number)


    
"""
for ch in "cdefgab":
    play_freq(note_freq(ch), duration=1), sleep(0.62)

play_freq(note_freq("c", octave_number=1), duration=1), sleep(0.62)
play_freq(note_freq("c", octave_number=1), duration=1), sleep(0.62)

for ch in "cdefgab"[::-1]:
    play_freq(note_freq(ch, octave_number=0), duration=1), sleep(0.62)
"""



def note_on(midi_number):
    play_freq(midi2freq(midi_number), duration=1)    
    print(midi2freq(midi_number))



def play_precalculated_note(midi_number, volume=127):
    if len(precalculated_sound[midi_number]) > 0:
        if volume == 127:
            sound = pygame.sndarray.make_sound(precalculated_sound[midi_number])
            sound.play(maxtime=7000) # CONSTANT TO REMOVE!
        elif volume < 127:
            sound = pygame.sndarray.make_sound( ((volume / 127 ) * precalculated_sound[midi_number]).astype("uint16"))
            sound.play(maxtime=7000)  # CONSTANT TO REMOVE!






def precalculate_sounds(duration):
    print("Calculating sounds")
    DURATION = duration


    ARRAY_SIZE = int(DISCR_FREQ * DURATION * (STEREO + 1))

    t = np.linspace(0, DURATION, num=ARRAY_SIZE)

    precalculated_sounds = np.zeros(shape=[128, ARRAY_SIZE], dtype="int16")

    total_number_of_notes = precalculated_sounds.shape[0]

    max_amp = 0
    
    for note_number in range(total_number_of_notes):
        print("%d%%" %  round(100.0 * note_number / total_number_of_notes), end="", flush=True)
        NOTE_FREQ = midi2freq(note_number)

        x =  np.exp(-3*t) * (np.sin( (NOTE_FREQ) * 2 * np.pi * t)
         + np.sin( (NOTE_FREQ) * 2 * np.pi * (t + 2/3))**3
         + 0.1 * np.sin(0.25 * NOTE_FREQ * 2*np.pi * t)
         + 0.01  * np.sin( 2 * NOTE_FREQ * 2*np.pi * t)
         + 0.05 * np.sin( 3 * NOTE_FREQ * 2*np.pi * t))


#       x = np.exp(-4 * t ** 1.1 + 1) * (np.sin(NOTE_FREQ * 2 * np.pi * t)
#           + 0.1 * np.sin(0.333 * NOTE_FREQ * 2*np.pi * t) 
#            + 0.1  * np.sin( 2 * NOTE_FREQ * 2*np.pi * t)
#            + 0.01 * np.sin( 3 * NOTE_FREQ * 2*np.pi * t))



        max_amp = np.max(np.abs(x))

        scaled = np.int16(x / max_amp * 30000.0)
        precalculated_sounds[note_number] = scaled
        print("\r", end="", flush=True)

    print("Ready!")
    return precalculated_sounds



# As an alternative, instead of generating sounds, here I read them from wav-files I recorded
def load_from_wavs(path="", *_):
    from scipy.io import wavfile

    notes_array = [[]] * 128
    for i in range(1, 60):
        wav_file = r"C:\Programming\Piano\Notes try\notes\%03d.wav" % i
        fs, data = wavfile.read(wav_file)
        notes_array[i + 35] = data

    return notes_array

pygame.mixer.pre_init(DISCR_FREQ, size=-16, channels=1)
pygame.mixer.init()
pygame.mixer.set_num_channels(100)



precalculated_sound = precalculate_sounds(duration=7)
#precalculated_sound = load_from_wavs()




