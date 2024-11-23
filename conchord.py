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
TEAL = (0, 127, 127)
CHORD_BUTTON_RADIUS = 40

bass_x = 100
bass_y = 250
x_space = 100
y_space = 100
register_x = 350
register_y = 100
rows = 5
columns = 12

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the MIDI ports
output = mido.open_output()
midi_input = mido.open_input()

# Reference chord intervals (from root)
#
#     "major": [0, 4, 7],
#     "minor": [0, 3, 7],
#     "dom7": [0, 4, 10],
#     "dim7": [-3, 0, 3],
#


class Button:
    def __init__(self, coords, size, images, text, state):
        self.coords = coords
        self.size = size
        self.images = images
        self.text = text
        self.state = state

    def draw(self):
        if self.images:
            image = self.images[1] if self.state else self.images[0]
            image_scaled = pygame.transform.smoothscale(image,
                                                        (self.size, self.size))
            image_rect = image.get_rect(center=self.coords)
            screen.blit(image_scaled, image_rect)
        else:
            colour = WHITE if (self.state is False) else GREY
            pygame.draw.circle(screen, colour, self.coords, self.size)
        if self.text:
            text_surface = font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.coords)
            screen.blit(text_surface, text_rect)

    def handle_switch(self, new_state):
        if self.state is not new_state:
            self.state = new_state


class NoteButton(Button):
    def __init__(self, coords, size, images, text, notes, state):
        super().__init__(coords, size, images, text, state)
        self.notes = notes

    def handle_switch(self, new_state, banks, shift, midi_chan, vel):
        if self.state is not new_state:
            self.state = new_state
            message = 'note_on' if self.state else 'note_off'
            for note in self.notes:
                for octave in banks:
                    active_note = note + 12 * (octave - (1 if shift else 0))
                    msg = mido.Message(message,
                                       channel=midi_chan,
                                       note=active_note,
                                       velocity=vel)
                    output.send(msg)


class RegisterButton(Button):
    def __init__(self, coords, size, images, text, banks, state):
        super().__init__(coords, size, images, text, state)
        self.banks = banks

    def handle_switch(self, new_state):
        if self.state is not new_state:
            self.state = new_state
            return self.banks if self.state else None


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
    chord_buttons[keys[i]] = NoteButton(coordinates[i],
                                        CHORD_BUTTON_RADIUS,
                                        None,
                                        names[i],
                                        notes[i],
                                        False)
# registers
soprano = [2]
alto = [2, 1]
tenor = [2, 1, 0]
soft_tenor = [1, 0]
master = [2, 1, 0, 0, -1]
soft_bass = [0, 0, -1]
bass_alto = [2, 1, -1]

current_register = soft_bass

register_images = [[pygame.image.load("soprano.png"),
                    pygame.image.load("soprano_b.png")],
                   [pygame.image.load("alto.png"),
                    pygame.image.load("alto_b.png")],
                   [pygame.image.load("tenor.png"),
                    pygame.image.load("tenor_b.png")],
                   [pygame.image.load("soft_tenor.png"),
                    pygame.image.load("soft_tenor_b.png")],
                   [pygame.image.load("master.png"),
                    pygame.image.load("master_b.png")],
                   [pygame.image.load("soft_bass.png"),
                    pygame.image.load("soft_bass_b.png")],
                   [pygame.image.load("bass-alto.png"),
                    pygame.image.load("bass-alto_b.png")]]

register_banks = [soprano, alto, tenor, soft_tenor, master, soft_bass, bass_alto]
register_keys = [pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5,
                 pygame.K_F6, pygame.K_F7, pygame.K_F8]

register_buttons = {}
for i in range(len(register_keys)):
    register_buttons[register_keys[i]] = RegisterButton((register_x + i * x_space, register_y),
                                                        CHORD_BUTTON_RADIUS*3/2,
                                                        register_images[i],
                                                        None,
                                                        register_banks[i],
                                                        True if i == 5 else False)  # soft bass default

octave_shift = Button((register_x - x_space * 1.5, register_y),
                      CHORD_BUTTON_RADIUS*3/2,
                      [pygame.image.load("octave.png"),
                       pygame.image.load("octave_b.png")],
                      None,
                      True)


def radial_distance(centre, pointer):
    return math.sqrt((pointer[0] - centre[0])**2 + (pointer[1] - centre[1])**2)


def mouse_over(button, event):
    return radial_distance(button.coords, event.pos) < button.size


def is_push(event):
    return event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]


def reset_registers(registers, active):
    print(active)
    active_banks = None
    for key, button in registers.items():
        state = True if key == active else False
        bank_change = button.handle_switch(state)
        active_banks = active_banks or bank_change
    return active_banks


current_vel = 90
midi_out_channel = 0
midi_in_channel = 0

# Game loop
running = True
while running:
    for message in midi_input.iter_pending():
        if message.is_cc(11) and message.channel == midi_in_channel:
            current_vel = message.value
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if event.key in chord_buttons:
                button = chord_buttons[event.key]
                new_state = is_push(event)
                button.handle_switch(new_state,
                                     current_register,
                                     octave_shift.state,
                                     midi_out_channel,
                                     current_vel)
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            for key, button in chord_buttons.items():
                if mouse_over(button, event):
                    new_state = is_push(event)
                    button.handle_switch(new_state,
                                         current_register,
                                         octave_shift.state,
                                         midi_out_channel,
                                         current_vel)
            for key, button in register_buttons.items():
                if (mouse_over(button, event) and is_push(event)):
                    current_register = reset_registers(register_buttons, key)
            if (mouse_over(octave_shift, event) and is_push(event)):
                octave_shift.handle_switch(not octave_shift.state)

    # Draw everything
    screen.fill(TEAL)
    for key, button in chord_buttons.items():
        button.draw()
    for key, button in register_buttons.items():
        button.draw()
    octave_shift.draw()

    pygame.display.flip()


pygame.quit()
