from buttons import NoteButton
import math
import pygame

GREY = (127, 127, 127)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

button_radius = 20
x0 = 800
y0 = 250
x_space = 50
y_space = 50
rows = 5
columns = 12

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)


def number_to_note(number):
    octave = number // NOTES_IN_OCTAVE
    note = NOTES[number % NOTES_IN_OCTAVE]
    return note, octave


top_row = [[55 + 3 * i] for i in range(int(columns))]
top_keys = [pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4,
            pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8,
            pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12]

second_row = [[57 + 3 * i] for i in range(int(columns))]
second_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
               pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
               pygame.K_9, pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS]

third_row = [[59 + 3 * i] for i in range(int(columns))]
third_keys = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
              pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i,
              pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET,
              pygame.K_RIGHTBRACKET]

fourth_row = [[61 + 3 * i] for i in range(int(columns))]
fourth_keys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
               pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k,
               pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_HASH]

fifth_row = [[60 + 3 * i] for i in range(int(columns))]
fifth_keys = [pygame.K_BACKSLASH, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v,
              pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_COMMA,
              pygame.K_PERIOD, pygame.K_SLASH, pygame.K_RSHIFT]

coordinates = [(x0 + (n % columns)*x_space + math.floor(n / columns)*x_space/3,
                y0 + math.floor(n / columns)*y_space)
               for n in range(rows * columns)]
coordinates[-12:] = [(coordinate[0] - x_space, coordinate[1]) for coordinate in coordinates[-12:]]

notes = top_row + second_row + third_row + fourth_row + fifth_row
keys = top_keys + second_keys + third_keys + fourth_keys + fifth_keys
names = [number_to_note(note_number[0])[0] for note_number in notes]


chromatic_buttons = {}
for i in range(len(keys)):
    chromatic_buttons[keys[i]] = NoteButton(coordinates[i],
                                            button_radius,
                                            None,
                                            names[i],
                                            BLACK if "#" in names[i] else WHITE,
                                            notes[i],
                                            False)
