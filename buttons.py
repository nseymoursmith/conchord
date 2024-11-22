import math
import mido
import pygame

GREY = (127, 127, 127)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def radial_distance(centre, pointer):
    return math.sqrt((pointer[0] - centre[0])**2 + (pointer[1] - centre[1])**2)


class Button:
    def __init__(self, coords, size, images, text, state):
        self.coords = coords
        self.size = size
        self.images = images
        self.text = text
        self.state = state

    def draw(self, screen, font):
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

    def mouse_over(self, event):
        return radial_distance(self.coords, event.pos) < self.size

    def handle_switch(self, new_state):
        if self.state is not new_state:
            self.state = new_state


class NoteButton(Button):
    def __init__(self, coords, size, images, text, notes, state):
        super().__init__(coords, size, images, text, state)
        self.notes = notes

    def handle_switch(self, new_state, banks, shift, midi_chan, vel, output):
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
