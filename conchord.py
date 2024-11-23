import mido
import pygame
from stradella import stradella_buttons
from stradella_registers import register_buttons, reset_registers, octave_shift

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1450, 850
TEAL = (0, 127, 127)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the MIDI ports
midi_output = mido.open_output()
midi_input = mido.open_input()


def is_push(event):
    return event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]


# Default to soft bass. TODO: make this less clunky
current_register = reset_registers(register_buttons, pygame.K_F7)
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
            if event.key in stradella_buttons:
                button = stradella_buttons[event.key]
                new_state = is_push(event)
                button.handle_switch(new_state,
                                     current_register,
                                     octave_shift.state,
                                     midi_out_channel,
                                     current_vel,
                                     midi_output)
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            for key, button in stradella_buttons.items():
                if button.mouse_over(event):
                    new_state = is_push(event)
                    button.handle_switch(new_state,
                                         current_register,
                                         octave_shift.state,
                                         midi_out_channel,
                                         current_vel,
                                         midi_output)
            for key, button in register_buttons.items():
                if (button.mouse_over(event) and is_push(event)):
                    current_register = reset_registers(register_buttons, key)
            if (octave_shift.mouse_over(event) and is_push(event)):
                octave_shift.handle_switch(not octave_shift.state)

    # Draw everything
    screen.fill(TEAL)
    for key, button in stradella_buttons.items():
        button.draw(screen, font)
    for key, button in register_buttons.items():
        button.draw(screen, font)
    octave_shift.draw(screen, font)

    pygame.display.flip()


pygame.quit()
