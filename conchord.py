from buttons import Button, NotePanel, RegisterPanel
from chromatic import chromatic_buttons
import mido
import os
import pygame
from stradella import stradella_buttons
from registers import stradella_register_buttons, chromatic_register_buttons

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1450, 450
TEAL = (0, 127, 127)
# TODO: centralise the coordinates/positioning configuration
x0 = 150
y0 = 100
x_space = 45
button_radius = 15

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

stradella_registers = RegisterPanel((150, 100), stradella_register_buttons)
chromatic_registers = RegisterPanel((950, 100), chromatic_register_buttons)
stradella_octave_shift = Button((x0 - x_space * 1.5, y0),
                                button_radius*2,
                                [pygame.image.load(os.path.join("button_images", "octave.png")),
                                 pygame.image.load(os.path.join("button_images", "octave_b.png"))],
                                None,
                                None,
                                True)

chromatic_octave_shift = Button((800 + x0 - x_space * 1.5, y0),
                                button_radius*2,
                                [pygame.image.load(os.path.join("button_images", "octave.png")),
                                 pygame.image.load(os.path.join("button_images", "octave_b.png"))],
                                None,
                                None,
                                True)
 
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

panel_switch = Button((740, 250),
                      button_radius*2,
                      [pygame.image.load(os.path.join("button_images", "left_arrow.png")),
                       pygame.image.load(os.path.join("button_images", "right_arrow_b.png"))],
                      None,
                      None,
                      True)


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
