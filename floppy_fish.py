"""Flappy Bird clone; first game made without tutorial"""

import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600  # creates game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Floppy Fish!')

FISH_FLOP_SOUND = pygame.mixer.Sound(os.path.join('Assets\\floppy_fish', 'floppy_fish_peter.mp3'))

FISH_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join('Assets\\floppy_fish', 'fish.png')), (43, 42))
FISHING_NET_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish', 'fish_net.png')), (55, 61))

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
FISH_WIDTH, FISH_HEIGHT = 43, 42


def draw_window(fish):
    WIN.fill(BLUE)
    WIN.blit(FISH_SPRITE, fish)
    pygame.draw.rect(WIN, WHITE, (pygame.Rect(500, 0, 55, 200)))
    WIN.blit(FISHING_NET_SPRITE, (500, 139))
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
