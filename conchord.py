import pygame
import mido

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHORD_BUTTON_WIDTH = 100
CHORD_BUTTON_HEIGHT = 50
CHORD_BUTTON_SPACING = 10

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
    "dim7": [-3, 0, 3],  # start from -3
}

root_notes = [25 + 7*i for i in range(12)]
counter_bass = [i + 4 for i in root_notes]

# Define the chords
chords = {
    "C": [60, 64, 67],  # C major
    "G": [67, 71, 74],  # G major
    "Am": [57, 60, 64],  # A minor
    "F": [65, 69, 72],  # F major
}

# Define the chord buttons
chord_buttons = [
    {"text": "C", "x": 100, "y": 100},
    {"text": "G", "x": 250, "y": 100},
    {"text": "Am", "x": 400, "y": 100},
    {"text": "F", "x": 100, "y": 250},
]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in chord_buttons:
                if (button["x"] < event.pos[0] < button["x"] + CHORD_BUTTON_WIDTH and
                        button["y"] < event.pos[1] < button["y"] + CHORD_BUTTON_HEIGHT):
                    # Play the chord
                    for note in chords[button["text"]]:
                        msg = mido.Message('note_on', note=note, velocity=64)
                        output.send(msg)
                    pygame.time.wait(500)  # Wait for 0.5 seconds
                    for note in chords[button["text"]]:
                        msg = mido.Message('note_off', note=note, velocity=64)
                        output.send(msg)

    # Draw everything
    screen.fill(BLACK)
    for button in chord_buttons:
        pygame.draw.rect(screen, WHITE, (button["x"], button["y"], CHORD_BUTTON_WIDTH, CHORD_BUTTON_HEIGHT))
        text_surface = font.render(button["text"], True, BLACK)
        screen.blit(text_surface, (button["x"] + 10, button["y"] + 10))

    pygame.display.flip()

pygame.quit()
