from instrument_draft_0 import note_on as play_note

l = [5, 6, 5, 0, 3, 5, 9, 0, 3, 5, 6, 5, 6, 5, 3, 0, 3, 6, 5, 4, 3, 2, 1, -3, -2]



for note in l:
    play_note(note+ 90, 50)

    input("press enter")
 

