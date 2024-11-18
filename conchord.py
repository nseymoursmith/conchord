import pygame
import mido
from math import floor

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1900, 850
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHORD_BUTTON_WIDTH = 100
CHORD_BUTTON_HEIGHT = 50

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the MIDI output port
output = mido.open_output()

# Define chord intervals
intervals = {
    "major": [0, 4, 3],
    "minor": [0, 3, 4],
    "dom7": [0, 4, 6],
    "dim7": [-3, 0, 3],
}

top_left = 100
x_space = 150
y_space = 150

rows = 5
columns = 12

root_notes = [[25 + 7*i] for i in range(12)]
root_names = ["Db", "Ab", "Eb", "Bb", "F", "C", "G", "D", "A", "E", "B", "F#"]
counter_bass = [[i[0] + 4] for i in root_notes]
cb_names = ["F", "C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
major_notes = [list(map(lambda x: x + n[0] + 12, (0, 4, 7))) for n in root_notes]
major_names = [f"{root_name}M" for root_name in root_names]
minor_notes = [list(map(lambda x: x + n[0] + 12, (0, 3, 7))) for n in root_notes]
minor_names = [f"{root_name}m" for root_name in root_names]
seventh_notes = [list(map(lambda x: x + n[0] + 12, (-3, 0, 3))) for n in root_notes]
seventh_names = [f"{root_name}7" for root_name in root_names]
coordinates = [(top_left + (n % columns)*x_space,
                top_left + floor(n / columns)*y_space)
               for n in range(rows * columns)]

notes = counter_bass + root_notes + major_notes + minor_notes + seventh_notes
names = cb_names + root_names + major_names + minor_names + seventh_names

chord_buttons = []
for i in range(len(names)):
    chord_buttons.append({"notes": notes[i],
                          "text": names[i],
                          "coords": coordinates[i]})

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in chord_buttons:
                if (button["coords"][0] < event.pos[0] < button["coords"][0] + CHORD_BUTTON_WIDTH and
                        button["coords"][1] < event.pos[1] < button["coords"][1] + CHORD_BUTTON_HEIGHT):
                    print(button)
                    # Play the chord
                    for note in button["notes"]:
                        msg = mido.Message('note_on', note=note, velocity=64)
                        output.send(msg)
                    pygame.time.wait(500)  # Wait for 0.5 seconds
                    for note in button["notes"]:
                        msg = mido.Message('note_off', note=note, velocity=64)
                        output.send(msg)

    # Draw everything
    screen.fill(BLACK)
    for button in chord_buttons:
        pygame.draw.rect(screen, WHITE, (button["coords"][0], button["coords"][1], CHORD_BUTTON_WIDTH, CHORD_BUTTON_HEIGHT))
        text_surface = font.render(button["text"], True, BLACK)
        screen.blit(text_surface, (button["coords"][0] + 10, button["coords"][1] + 10))

    pygame.display.flip()

pygame.quit()
