"""Flappy Bird clone; first game made without tutorial"""

import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Game Window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Floppy Fish!')

# Global Constants
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
FISH_WIDTH, FISH_HEIGHT = 43, 42
NET_WIDTH = 55

# Sound Bytes
FISH_FLOP_SOUND = pygame.mixer.Sound(os.path.join('Assets\\floppy_fish_assets', 'floppy_fish_peter.mp3'))

# Sprites
FISH_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'fish.png')), (FISH_WIDTH, FISH_HEIGHT))
NET_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'fish_net.png')), (NET_WIDTH, 61))
NET_ROD_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'fish_net_rod.png')), (NET_WIDTH, 78))


def draw_window(fish):
    WIN.fill(BLUE)
    WIN.blit(FISH_SPRITE, fish)
    WIN.blit(NET_ROD_SPRITE, (500, 78))  # FIXME: placeholder net
    WIN.blit(NET_ROD_SPRITE, (500, 0))
    WIN.blit(NET_SPRITE, (500, 139))
    pygame.display.update()


def main():
    fish = pygame.Rect(200, 100, 40, 40)
    fish_momentum = 10

    clock = pygame.time.Clock()  # fps limiter
    run = True
    while run:  # game loop
        clock.tick(60)  # fps limiter
        for event in pygame.event.get():  # game events
            if event.type == pygame.QUIT:  # stop program when game window closed
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fish_momentum -= 27
                    FISH_FLOP_SOUND.play()

        fish_momentum += 1
        if fish_momentum > 12:
            fish_momentum = 12
        if fish_momentum < -18:
            fish_momentum = -18
        fish.y += fish_momentum

        draw_window(fish)

    pygame.quit()


if __name__ == '__main__':
    main()
