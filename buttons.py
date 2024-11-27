import math
import mido
import pygame

GREY = (127, 127, 127)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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

    def radial_distance(self, centre, pointer):
        return math.sqrt((pointer[0] - centre[0])**2 +
                         (pointer[1] - centre[1])**2)

    def is_push(self, event):
        return event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]

    def mouse_over(self, event):
        return self.radial_distance(self.coords, event.pos) < self.size

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


class StradellaPanel:
    def __init__(self, buttons, velocity, banks, shift, midi_chan, midi_out):
        self.buttons = buttons
        self.velocity = velocity
        self.banks = banks
        self.shift = shift
        self.midi_chan = midi_chan
        self.midi_out = midi_out

    def handle_event(self, event):
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if event.key in self.buttons:
                button = self.buttons[event.key]
                new_state = button.is_push(event)
                button.handle_switch(new_state,
                                     self.banks,
                                     self.shift,
                                     self.midi_chan,
                                     self.velocity,
                                     self.midi_out)
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            for key, button in self.buttons.items():
                if button.mouse_over(event):
                    new_state = button.is_push(event)
                    button.handle_switch(new_state,
                                         self.banks,
                                         self.shift,
                                         self.midi_chan,
                                         self.velocity,
                                         self.midi_out)

    def draw(self, screen, font):
        for key, button in self.buttons.items():
            button.draw(screen, font)


