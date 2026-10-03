# import pygame

# from game.game import Game


# pygame.init()

# screen = pygame.display.set_mode(
#     (1100, 700),
#     pygame.RESIZABLE
# )

# pygame.display.set_caption(
#     "Mepple & Mipple - Magical Friendship Adventure"
# )

# clock = pygame.time.Clock()

# game = Game(screen)


# while game.running:

#     dt = clock.tick(60)

#     for event in pygame.event.get():

#         game.handle_event(event)

#     game.update(dt)

#     game.draw()

#     pygame.display.flip()


# pygame.quit()


import os
import pygame

import game.game

print("=" * 60)
print("PYTHON IS LOADING:")
print(os.path.abspath(game.game.__file__))
print("=" * 60)

from game.game import Game


pygame.init()

screen = pygame.display.set_mode(
    (1100, 700),
    pygame.RESIZABLE
)

pygame.display.set_caption(
    "Mepple & Mipple - Magical Friendship Adventure"
)

clock = pygame.time.Clock()

game = Game(screen)

while game.running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        game.handle_event(event)

    game.update(dt)
    game.draw()

    pygame.display.flip()

pygame.quit()