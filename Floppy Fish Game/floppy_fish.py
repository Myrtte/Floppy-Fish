"""Flappy Bird clone; first game made without tutorial"""

import pygame
import os
import random
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
NET_GAP = 260

# Game Events
COLLISION_NET = pygame.USEREVENT + 1
COLLISION_ROD = pygame.USEREVENT + 2

# Sound Bytes
FISH_FLOP_SOUND = pygame.mixer.Sound(os.path.join('Assets\\floppy_fish_assets', 'floppy_fish_peter.mp3'))

# Sprites
BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'background.png')), (WIDTH * 3, HEIGHT))
FISH_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'fish.png')), (FISH_WIDTH, FISH_HEIGHT))
NET_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'fish_net.png')), (NET_WIDTH, NET_HEIGHT))
ROD_SPRITE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets\\floppy_fish_assets', 'fish_net_rod.png')), (NET_WIDTH, 400))
BOT_NET_SPRITE = pygame.transform.flip(pygame.transform.rotate(NET_SPRITE, 180), True, False)
BOT_ROD_SPRITE = pygame.transform.flip(pygame.transform.rotate(ROD_SPRITE, 180), True, False)


def handle_nets(top_nets_active, top_rods_active, bot_nets_active, bot_rods_active, fish):
    num_net = 0
    new_pos = None
    if num_net % 4 == 0:
        new_pos = random.randint(50, 229)

    for net in top_nets_active:
        net.x += NET_VEL
        if net.x + NET_WIDTH <= 0:
            net.x = 1100
            net.y = new_pos
            num_net += 1
        
        if fish.colliderect(net):
            pygame.event.post(pygame.event.Event(COLLISION_NET))

    for rod in top_rods_active:
        rod.x += NET_VEL
        if rod.x + NET_WIDTH <= 0:
            rod.x = 1100
            rod.y = -400 + new_pos
            num_net += 1

        if fish.colliderect(rod):
            pygame.event.post(pygame.event.Event(COLLISION_ROD))

    for net in bot_nets_active:
        net.x += NET_VEL
        if net.x + NET_WIDTH <= 0:
            net.x = 1100
            net.y = new_pos + NET_GAP
            num_net += 1

        if fish.colliderect(net):
            pygame.event.post(pygame.event.Event(COLLISION_NET))

    for rod in bot_rods_active:
        rod.x += NET_VEL
        if rod.x + NET_WIDTH <= 0:
            rod.x = 1100
            rod.y = new_pos + NET_GAP
            num_net += 1

        if fish.colliderect(rod):
            pygame.event.post(pygame.event.Event(COLLISION_ROD))


def draw_window(fish, top_nets_active, top_rods_active, bot_nets_active, bot_rods_active, background_x, background_x2):
    WIN.blit(BACKGROUND, (background_x, 0))
    WIN.blit(BACKGROUND, (background_x2, 0))
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
    background_x = 0
    background_x2 = 2400
    collision = 0

    # Hit Boxes
    fish = pygame.Rect(200, 300, 40, 40)
    pos_1, pos_2, pos_3 = 140, random.randint(50, 229), random.randint(50, 229)
    nets_active = [pygame.Rect(700, pos_1, NET_WIDTH, NET_HEIGHT),
                   pygame.Rect(1100, pos_2, NET_WIDTH, NET_HEIGHT),
                   pygame.Rect(1500, pos_3, NET_WIDTH, NET_HEIGHT),
                   pygame.Rect(700, -400 + pos_1, 10, 400),
                   pygame.Rect(1100, -400 + pos_2, 10, 400),
                   pygame.Rect(1500, -400 + pos_3, 10, 400),
                   pygame.Rect(700, pos_1 + NET_GAP, NET_WIDTH, NET_HEIGHT),
                   pygame.Rect(1100, pos_2 + NET_GAP, NET_WIDTH, NET_HEIGHT),
                   pygame.Rect(1500, pos_3 + NET_GAP, NET_WIDTH, NET_HEIGHT),
                   pygame.Rect(700, pos_1 + NET_GAP, 10, 400),
                   pygame.Rect(1100, pos_2 + NET_GAP, 10, 400),
                   pygame.Rect(1500, pos_3 + NET_GAP, 10, 400)]
    top_nets_active, top_rods_active = (nets_active[0:3]), (nets_active[3:6])
    bot_nets_active, bot_rods_active = (nets_active[6:9]), (nets_active[9:12])

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
                    playing = True

            if event.type == COLLISION_ROD:
                run = False

            if event.type == COLLISION_NET:
                 run = False

        if playing:
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

            # Background
            background_x2 -= 1
            if background_x2 == -2400:
                background_x2 = background_x + 2400

            background_x -= 1
            if background_x == -2400:
                background_x = background_x2 + 2400
            
            handle_nets(top_nets_active, top_rods_active, bot_nets_active, bot_rods_active, fish)
            


        draw_window(fish, top_nets_active, top_rods_active, bot_nets_active, bot_rods_active, background_x, background_x2)

    pygame.quit()


if __name__ == '__main__':
    main()
