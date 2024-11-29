from buttons import NotePanel, RegisterPanel
import mido
import pygame
from chromatic import chromatic_buttons
from stradella import stradella_buttons
from registers import stradella_register_buttons, stradella_octave_shift, chromatic_octave_shift, chromatic_register_buttons, panel_switch

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1450, 450
TEAL = (0, 127, 127)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 24)

# Set up the MIDI ports
midi_output = mido.open_output()
midi_input = mido.open_input()

current_vel = 90
midi_out_channel = 0
midi_in_channel = 0

# TODO: centralise the coordinates/positioning configuration
stradella_registers = RegisterPanel((150, 100), stradella_register_buttons)
chromatic_registers = RegisterPanel((950, 100), chromatic_register_buttons)

stradella = NotePanel((50, 150),
                      stradella_buttons,
                      current_vel,
                      stradella_registers.active_banks,
                      stradella_octave_shift.state,
                      midi_out_channel,
                      midi_output)

chromatic = NotePanel((800, 150),
                      chromatic_buttons,
                      current_vel,
                      chromatic_registers.active_banks,
                      chromatic_octave_shift.state,
                      midi_out_channel,
                      midi_output)

# Game loop
running = True
while running:
    for message in midi_input.iter_pending():
        if message.is_cc(11) and message.channel == midi_in_channel:
            stradella.velocity = message.value
            chromatic.velocity = message.value
    for event in pygame.event.get():
        stradella_registers.handle_event(event)
        chromatic_registers.handle_event(event)
        stradella.banks = stradella_registers.active_banks
        chromatic.banks = chromatic_registers.active_banks
        if panel_switch.state:
            chromatic.handle_event(event)
        else:
            stradella.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            if (stradella_octave_shift.mouse_over(event) and stradella_octave_shift.is_push(event)):
                stradella_octave_shift.handle_switch(not stradella_octave_shift.state)
                stradella.shift = stradella_octave_shift.state
            if (chromatic_octave_shift.mouse_over(event) and chromatic_octave_shift.is_push(event)):
                chromatic_octave_shift.handle_switch(not chromatic_octave_shift.state)
                chromatic.shift = chromatic_octave_shift.state
            if (panel_switch.mouse_over(event) and panel_switch.is_push(event)):
                panel_switch.handle_switch(not panel_switch.state)

    # Draw everything
    screen.fill(TEAL)
    chromatic.draw(screen, font)
    stradella.draw(screen, font)
    stradella_registers.draw(screen, font)
    chromatic_registers.draw(screen, font)
    stradella_octave_shift.draw(screen, font)
    chromatic_octave_shift.draw(screen, font)
    panel_switch.draw(screen, font)

    pygame.display.flip()


pygame.quit()
