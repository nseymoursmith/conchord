from buttons import StradellaPanel, RegisterPanel
import mido
import pygame
from stradella import stradella_buttons
from stradella_registers import register_buttons, octave_shift

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

current_vel = 90
midi_out_channel = 0
midi_in_channel = 0

registers = RegisterPanel(register_buttons)

stradella = StradellaPanel(stradella_buttons,
                           current_vel,
                           registers.active_banks,
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
        registers.handle_event(event)
        stradella.banks = registers.active_banks
        stradella.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            if (octave_shift.mouse_over(event) and octave_shift.is_push(event)):
                octave_shift.handle_switch(not octave_shift.state)
                stradella.shift = octave_shift.state

    # Draw everything
    screen.fill(TEAL)
    stradella.draw(screen, font)
    registers.draw(screen, font)
    octave_shift.draw(screen, font)

    pygame.display.flip()


pygame.quit()
