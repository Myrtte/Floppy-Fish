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
NET_WIDTH, NET_HEIGHT = 55, 61
NET_VEL = -5

# Sound Bytes
FISH_FLOP_SOUND = pygame.mixer.Sound(os.path.join('Assets\\floppy_fish_assets', 'floppy_fish_peter.mp3'))

# Sprites
FISH_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'fish.png')), (FISH_WIDTH, FISH_HEIGHT))
NET_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'fish_net.png')), (NET_WIDTH, NET_HEIGHT))
ROD_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'fish_net_rod.png')), (NET_WIDTH, 200))
BOT_NET_SPRITE = pygame.transform.flip(pygame.transform.rotate(NET_SPRITE, 180), True, False)
BOT_ROD_SPRITE = pygame.transform.flip(pygame.transform.rotate(ROD_SPRITE, 180), True, False)


def handle_nets(top_nets_active, top_rods_active, bot_nets_active, bot_rods_active):
    for net in top_nets_active:
        net.x += NET_VEL
        if net.x + NET_WIDTH <= 0:
            net.x = 1100

    for rod in top_rods_active:
        rod.x += NET_VEL
        if rod.x + NET_WIDTH <= 0:
            rod.x = 1100

    for net in bot_nets_active:
        net.x += NET_VEL
        if net.x + NET_WIDTH <= 0:
            net.x = 1100

    for rod in bot_rods_active:
        rod.x += NET_VEL
        if rod.x + NET_WIDTH <= 0:
            rod.x = 1100


def draw_window(fish, top_nets_active, top_rods_active, bot_nets_active, bot_rods_active):
    WIN.fill(BLUE)
    WIN.blit(FISH_SPRITE, fish)
    for rod in top_rods_active:
        WIN.blit(ROD_SPRITE, rod)

    for rod in bot_rods_active:
        WIN.blit(BOT_ROD_SPRITE, rod)

    for net in top_nets_active:
        WIN.blit(NET_SPRITE, net)

    for net in bot_nets_active:
        WIN.blit(BOT_NET_SPRITE, net)

    pygame.display.update()


def main():
    # Game variables
    fish_momentum = 10
    playing = False
    
    # Hit Boxes
    fish = pygame.Rect(200, 100, 40, 40)

    top_nets_active = [pygame.Rect(700, 139, NET_WIDTH, NET_HEIGHT),
                       pygame.Rect(1100, 139, NET_WIDTH, NET_HEIGHT),
                       pygame.Rect(1500, 139, NET_WIDTH, NET_HEIGHT)]

    top_rods_active = [pygame.Rect(700, 0, 10, 139),
                       pygame.Rect(1100, 0, 10, 139),
                       pygame.Rect(1500, 0, 10, 139)]

    bot_nets_active = [pygame.Rect(700, 400, NET_WIDTH, NET_HEIGHT),
                       pygame.Rect(1100, 400, NET_WIDTH, NET_HEIGHT),
                       pygame.Rect(1500, 400, NET_WIDTH, NET_HEIGHT)]

    bot_rods_active = [pygame.Rect(700, 400, 10, 200),
                       pygame.Rect(1100, 400, 10, 200),
                       pygame.Rect(1500, 400, 10, 200)]

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

                if event.key == pygame.K_RIGHT:  # FIXME: make this start game.
                    playing = True

        # Fish Momentum
        fish_momentum += 1
        if fish_momentum > 12:
            fish_momentum = 12
        if fish_momentum < -18:
            fish_momentum = -18
        fish.y += fish_momentum

        # Fish Ceiling
        if fish.y <= 0:
            fish.y = 0
        if fish.y >= 600 - FISH_HEIGHT:
            fish.y = 600 - FISH_HEIGHT

        if playing:
            handle_nets(top_nets_active, top_rods_active, bot_nets_active, bot_rods_active)

        draw_window(fish, top_nets_active, top_rods_active, bot_nets_active, bot_rods_active)

    pygame.quit()


if __name__ == '__main__':
    main()
