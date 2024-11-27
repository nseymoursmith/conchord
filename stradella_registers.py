from buttons import RegisterButton, Button
import os
import pygame

button_radius = 30
x0 = 450
y0 = 100
x_space = 90

# registers
soprano = [2]
alto = [2, 1]
tenor = [2, 1, 0]
soft_tenor = [1, 0]
master = [2, 1, 0, 0, -1]
soft_bass = [0, 0, -1]
bass_alto = [2, 1, -1]

register_images = [[pygame.image.load(os.path.join("button_images", "soprano.png")),
                    pygame.image.load(os.path.join("button_images", "soprano_b.png"))],
                   [pygame.image.load(os.path.join("button_images", "alto.png")),
                    pygame.image.load(os.path.join("button_images", "alto_b.png"))],
                   [pygame.image.load(os.path.join("button_images", "tenor.png")),
                    pygame.image.load(os.path.join("button_images", "tenor_b.png"))],
                   [pygame.image.load(os.path.join("button_images", "soft_tenor.png")),
                    pygame.image.load(os.path.join("button_images", "soft_tenor_b.png"))],
                   [pygame.image.load(os.path.join("button_images", "master.png")),
                    pygame.image.load(os.path.join("button_images", "master_b.png"))],
                   [pygame.image.load(os.path.join("button_images", "soft_bass.png")),
                    pygame.image.load(os.path.join("button_images", "soft_bass_b.png"))],
                   [pygame.image.load(os.path.join("button_images", "bass-alto.png")),
                    pygame.image.load(os.path.join("button_images", "bass-alto_b.png"))]]

register_banks = [soprano, alto, tenor, soft_tenor, master, soft_bass, bass_alto]
register_keys = [pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5,
                 pygame.K_F6, pygame.K_F7, pygame.K_F8]

register_buttons = {}
for i in range(len(register_keys)):
    register_buttons[register_keys[i]] = RegisterButton((x0 + i * x_space, y0),
                                                        button_radius*2,
                                                        register_images[i],
                                                        None,
                                                        register_banks[i],
                                                        False)

octave_shift = Button((x0 - x_space * 1.5, y0),
                      button_radius*2,
                      [pygame.image.load(os.path.join("button_images", "octave.png")),
                       pygame.image.load(os.path.join("button_images", "octave_b.png"))],
                      None,
                      True)
