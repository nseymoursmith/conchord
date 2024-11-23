from buttons import NoteButton
import math
import pygame

button_radius = 40
x0 = 100
y0 = 250
x_space = 100
y_space = 100
rows = 5
columns = 12

# Reference chord intervals (from root)
#
#     "major": [0, 4, 7],
#     "minor": [0, 3, 7],
#     "dom7": [0, 4, 10],
#     "dim7": [-3, 0, 3],

# Db leftmost bass
root_notes_lower = [[61 + 2 * i] for i in range(int(columns/2))]

# Ab major fourth below
root_notes_higher = [[56 + 2 * i] for i in range(int(columns/2))]

root_notes = root_notes_lower + root_notes_higher
# Interleave to get major fourth major fifth alternating
root_notes[::2] = root_notes_lower
root_notes[1::2] = root_notes_higher
root_names = ["Db", "Ab", "Eb", "Bb", "F", "C", "G", "D", "A", "E", "B", "F#"]
root_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
             pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
             pygame.K_9, pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS]

counter_bass = [[n[0] + 4] for n in root_notes]
cb_names = ["F", "C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
cb_keys = [pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4,
           pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8,
           pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12]

major_notes = [list(map(lambda x: x + n[0] + 12, (0, 4, 7)))
               for n in root_notes]
major_names = [f"{root_name}M" for root_name in root_names]
major_keys = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
              pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i,
              pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET,
              pygame.K_RIGHTBRACKET]

minor_notes = [list(map(lambda x: x + n[0] + 12, (0, 3, 7)))
               for n in root_notes]
minor_names = [f"{root_name}m" for root_name in root_names]
minor_keys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
              pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k,
              pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_HASH]

seventh_notes = [list(map(lambda x: x + n[0] + 12, (0, 4, 10)))
                 for n in root_notes]
seventh_names = [f"{root_name}7" for root_name in root_names]
seventh_keys = [pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v,
                pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_COMMA,
                pygame.K_PERIOD, pygame.K_SLASH, pygame.K_F14, pygame.K_F15]


coordinates = [(x0 + (n % columns)*x_space + math.floor(n / columns)*x_space/3,
                y0 + math.floor(n / columns)*y_space)
               for n in range(rows * columns)]

notes = counter_bass + root_notes + major_notes + minor_notes + seventh_notes
names = cb_names + root_names + major_names + minor_names + seventh_names
keys = cb_keys + root_keys + major_keys + minor_keys + seventh_keys

stradella_buttons = {}
for i in range(len(keys)):
    stradella_buttons[keys[i]] = NoteButton(coordinates[i],
                                            button_radius,
                                            None,
                                            names[i],
                                            notes[i],
                                            False)

