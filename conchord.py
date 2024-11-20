import pygame
import mido
from math import floor

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1900, 850
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
CHORD_BUTTON_WIDTH = 100
CHORD_BUTTON_HEIGHT = 50

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the MIDI output port
output = mido.open_output()

# Reference chord intervals (from root)
#
#     "major": [0, 4, 7],
#     "minor": [0, 3, 7],
#     "dom7": [0, 4, 10],
#     "dim7": [-3, 0, 3],
#

top_left = 100
x_space = 150
y_space = 150

rows = 5
columns = 12
octave = -2  # From C3 bass (on 6th row)

# Db leftmost bass
root_notes_lower = [[61 + 2 * i + octave * 12] for i in range(int(columns/2))]

# Ab major fourth below
root_notes_higher = [[56 + 2 * i + octave * 12] for i in range(int(columns/2))]

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


coordinates = [(top_left + (n % columns)*x_space,
                top_left + floor(n / columns)*y_space)
               for n in range(rows * columns)]

notes = counter_bass + root_notes + major_notes + minor_notes + seventh_notes
names = cb_names + root_names + major_names + minor_names + seventh_names
keys = cb_keys + root_keys + major_keys + minor_keys + seventh_keys

chord_buttons = {}
for i in range(len(keys)):
    chord_buttons[keys[i]] = {"notes": notes[i],
                              "text": names[i],
                              "coords": coordinates[i],
                              "keyboard": keys[i],
                              "state": 'note_off'}

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if event.key in chord_buttons:
                button = chord_buttons[event.key]
                print(button)
                button["state"] = 'note_on' if event.type == pygame.KEYDOWN else 'note_off'
                # Play/stop the chord
                for note in button["notes"]:
                    msg = mido.Message(button["state"], note=note, velocity=64)
                    output.send(msg)
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            for key, button in chord_buttons.items():
                if (button["coords"][0] < event.pos[0] < button["coords"][0] + CHORD_BUTTON_WIDTH and
                        button["coords"][1] < event.pos[1] < button["coords"][1] + CHORD_BUTTON_HEIGHT):
                    print(button)
                    button["state"] = 'note_on' if event.type == pygame.MOUSEBUTTONDOWN else 'note_off'
                    # Play/stop the chord
                    for note in button["notes"]:
                        msg = mido.Message(button["state"], note=note, velocity=64)
                        output.send(msg)

    # Draw everything
    screen.fill(BLACK)
    for key, button in chord_buttons.items():
        colour = WHITE if button["state"] == 'note_off' else GREY
        pygame.draw.rect(screen, colour, (button["coords"][0], button["coords"][1], CHORD_BUTTON_WIDTH, CHORD_BUTTON_HEIGHT))
        text_surface = font.render(button["text"], True, BLACK)
        screen.blit(text_surface, (button["coords"][0] + 10, button["coords"][1] + 10))

    pygame.display.flip()

pygame.quit()
