from buttons import StradellaPanel
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

# Default to soft bass. TODO: make this less clunky
current_register = reset_registers(register_buttons, pygame.K_F7)
current_vel = 90
midi_out_channel = 0
midi_in_channel = 0

stradella = StradellaPanel(stradella_buttons,
                           current_vel,
                           current_register,
                           octave_shift.state,
                           midi_out_channel,
                           midi_output)

# Game loop
running = True
while running:
    for message in midi_input.iter_pending():
        if message.is_cc(11) and message.channel == midi_in_channel:
            stradella.velocity = message.value
    for event in pygame.event.get():
        stradella.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            for key, button in register_buttons.items():
                if (button.mouse_over(event) and button.is_push(event)):
                    stradella.banks = reset_registers(register_buttons, key)
            if (octave_shift.mouse_over(event) and button.is_push(event)):
                octave_shift.handle_switch(not octave_shift.state)
                stradella.shift = octave_shift.state

    # Draw everything
    screen.fill(TEAL)
    stradella.draw(screen, font)
    for key, button in register_buttons.items():
        button.draw(screen, font)
    octave_shift.draw(screen, font)

    pygame.display.flip()


pygame.quit()
