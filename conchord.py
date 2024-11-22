import pygame
import mido
import math

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1450, 850
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
CHORD_BUTTON_RADIUS = 40

bass_x = 100
bass_y = 250
x_space = 100
y_space = 100
register_x = 350
register_y = 100


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

rows = 5
columns = 12
root_shift = True
shift_off = pygame.image.load("octave.png")
shift_on = pygame.image.load("octave_b.png")


# registers
soprano = [2]
alto = [2, 1]
tenor = [2, 1, 0]
soft_tenor = [1, 0]
master = [2, 1, 0, 0, -1]
soft_bass = [0, 0, -1]
bass_alto = [2, 1, -1]

registers = [{"image": pygame.image.load("soprano.png"),
              "image_b": pygame.image.load("soprano_b.png"),
              "banks": soprano},
             {"image": pygame.image.load("alto.png"),
              "image_b": pygame.image.load("alto_b.png"),
              "banks": alto},
             {"image": pygame.image.load("tenor.png"),
              "image_b": pygame.image.load("tenor_b.png"),
              "banks": tenor},
             {"image": pygame.image.load("soft_tenor.png"),
              "image_b": pygame.image.load("soft_tenor_b.png"),
              "banks": soft_tenor},
             {"image": pygame.image.load("master.png"),
              "image_b": pygame.image.load("master_b.png"),
              "banks": master},
             {"image": pygame.image.load("soft_bass.png"),
              "image_b": pygame.image.load("soft_bass_b.png"),
              "banks": soft_bass},
             {"image": pygame.image.load("bass-alto.png"),
              "image_b": pygame.image.load("bass-alto_b.png"),
              "banks": bass_alto}]

current_register = soft_bass

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


coordinates = [(bass_x + (n % columns)*x_space + math.floor(n / columns)*x_space/3,
                bass_y + math.floor(n / columns)*y_space)
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

def radial_distance(centre, pointer):
    return math.sqrt((pointer[0] - centre[0])**2 + (pointer[1] - centre[1])**2)

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
                    for octave in current_register:
                        active_note = note + 12 * octave + 12 * (-1 if root_shift else 0)
                        msg = mido.Message(button["state"], note=active_note, velocity=64)
                        output.send(msg)
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            for key, button in chord_buttons.items():
                if (radial_distance(button["coords"], event.pos) < CHORD_BUTTON_RADIUS):
                    print(button)
                    button["state"] = 'note_on' if event.type == pygame.MOUSEBUTTONDOWN else 'note_off'
                    # Play/stop the chord
                    for note in button["notes"]:
                        for octave in current_register:
                            active_note = note + 12 * octave + 12 * (-1 if root_shift else 0)
                            msg = mido.Message(button["state"], note=active_note, velocity=64)
                            output.send(msg)
            for n in range(len(registers)):
                coords = (register_x + n * x_space, register_y)
                if (radial_distance(coords, event.pos) < CHORD_BUTTON_RADIUS*3/4):
                    banks = registers[n]["banks"]
                    print(banks)
                    current_register = banks
            if (event.type == pygame.MOUSEBUTTONDOWN and
                radial_distance((register_x - x_space * 1.5, register_y), event.pos)
                < CHORD_BUTTON_RADIUS*3/4):
                root_shift = not root_shift

    # Draw everything
    screen.fill(BLACK)
    for key, button in chord_buttons.items():
        colour = WHITE if button["state"] == 'note_off' else GREY
        pygame.draw.circle(screen, colour, (button["coords"][0], button["coords"][1]), CHORD_BUTTON_RADIUS)
        text_surface = font.render(button["text"], True, BLACK)
        text_rect = text_surface.get_rect(center=(button["coords"][0], button["coords"][1]))
        screen.blit(text_surface, text_rect)
    for n in range(len(registers)):
        coords = (register_x + n * x_space, register_y)
        image = registers[n]["image_b"] if current_register == registers[n]["banks"] else registers[n]["image"]
        image_scaled = pygame.transform.smoothscale(image, (CHORD_BUTTON_RADIUS*3/2, CHORD_BUTTON_RADIUS*3/2))
        image_rect = image.get_rect(center=coords)
        screen.blit(image_scaled, image_rect)
    image = shift_on if root_shift else shift_off
    image_scaled = pygame.transform.smoothscale(image, (CHORD_BUTTON_RADIUS*3/2, CHORD_BUTTON_RADIUS*3/2))
    image_rect = image.get_rect(center=(register_x - x_space * 1.5, register_y))
    screen.blit(image_scaled, image_rect)

    pygame.display.flip()


pygame.quit()
