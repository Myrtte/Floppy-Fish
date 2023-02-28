"""Flappy Bird clone; first game made without tutorial"""
import pygame
import random
from sys import exit
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Game Window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Floppy Fish!')

# Global Constants
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
LIGHT_BLUE = (84, 250, 240)
FISH_WIDTH, FISH_HEIGHT = 43, 42
NET_WIDTH, NET_HEIGHT = 55, 61
NET_VEL = -5
NET_GAP = 260

# Game Events
COLLISION_NET = pygame.USEREVENT + 1
COLLISION_ROD = pygame.USEREVENT + 2
ONE_POINT = pygame.USEREVENT + 3

# Fonts
TITLE_FONT = pygame.font.SysFont('segoescript', 40)
TITLE_FONT_SMALL = pygame.font.SysFont('segoescript', 20)
HIGH_SCORE_FONT = pygame.font.SysFont('segoescript', 70)

# Sound Bytes
FISH_FLOP_SOUND = pygame.mixer.Sound('Assets\\floppy_fish\\sounds\\floppy_fish_peter.mp3')
INTRO_SOUND = pygame.mixer.Sound('Assets\\floppy_fish\\sounds\\intro_sound.mp3')
SOUNDTRACK = pygame.mixer.Sound('Assets\\floppy_fish\\sounds\\soundtrack.mp3')
NET_HIT = pygame.mixer.Sound('Assets\\floppy_fish\\sounds\\net_hit.mp3')
ROD_HIT = pygame.mixer.Sound('Assets\\floppy_fish\\sounds\\rod_hit.mp3')
MENU_SELECT = pygame.mixer.Sound('Assets\\floppy_fish\\sounds\\fish_flop.mp3')

# Sprites
TITLE = pygame.transform.scale(
    pygame.image.load('Assets\\floppy_fish\\graphics\\floppy_fish_text.png').convert_alpha(), (600, 500))
BACKGROUND = pygame.transform.scale(
    pygame.image.load('Assets\\floppy_fish\\graphics\\background.png').convert_alpha(), (WIDTH * 3, HEIGHT))
FISH_SPRITE = pygame.transform.scale(
    pygame.image.load('Assets\\floppy_fish\\graphics\\fish.png').convert_alpha(), (FISH_WIDTH, FISH_HEIGHT))
FLIPPED_FISH = pygame.transform.rotate(
    pygame.transform.scale(FISH_SPRITE, (30, 30)), 10)
NET_SPRITE = pygame.transform.scale(
    pygame.image.load('Assets\\floppy_fish\\graphics\\fish_net.png').convert_alpha(), (NET_WIDTH, NET_HEIGHT))
ROD_SPRITE = pygame.transform.scale(
    pygame.image.load('Assets\\floppy_fish\\graphics\\fish_net_rod.png').convert_alpha(), (NET_WIDTH, 400))
BOT_NET_SPRITE = pygame.transform.flip(pygame.transform.rotate(NET_SPRITE, 180), True, False)
BOT_ROD_SPRITE = pygame.transform.flip(pygame.transform.rotate(ROD_SPRITE, 180), True, False)

pygame.display.set_icon(FISH_SPRITE)


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

        if fish.x == net.x:
            pygame.event.post(pygame.event.Event(ONE_POINT))

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


def draw_window_home_screen():
    title = pygame.Rect(100, 0, 600, 500)
    small_fish = pygame.Rect(350, 300, 30, 30)
    WIN.blit(BACKGROUND, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)
    WIN.blit(TITLE, title)
    pygame.display.update()
    FISH_FLOP_SOUND.play()
    pygame.time.delay(1000)
    WIN.blit(FLIPPED_FISH, small_fish)
    pygame.display.update()
    FISH_FLOP_SOUND.play()
    pygame.time.delay(1000)
    while True:
        title.x -= 3
        small_fish.x -= 3
        WIN.blit(BACKGROUND, (0, 0))
        WIN.blit(FLIPPED_FISH, small_fish)
        WIN.blit(TITLE, title)
        pygame.display.update()
        if title.x <= 0:
            break
    high_score_txt = TITLE_FONT_SMALL.render('Current High Score:', True, LIGHT_BLUE)
    hs_high_score = HIGH_SCORE_FONT.render('69', True, LIGHT_BLUE)
    WIN.blit(high_score_txt, (550, 230))
    WIN.blit(hs_high_score, (
        450 + high_score_txt.get_width() // 2 + hs_high_score.get_width() // 2, 220 + high_score_txt.get_height()))
    INTRO_SOUND.play()
    pygame.display.update()


def draw_window_game(fish, top_nets_active, top_rods_active, bot_nets_active,
                     bot_rods_active, background_x, background_x2, final_score, high_score):
    final_score_text = TITLE_FONT.render(f"Score: {str(final_score)}", True, WHITE)
    high_score_text = TITLE_FONT.render(f"High Score: {str(high_score)}", True, WHITE)

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

    WIN.blit(final_score_text, (10, 50))
    WIN.blit(high_score_text, (10, 0))

    pygame.display.update()


def main(restart=0, high_score=0):
    if restart == 0:
        SOUNDTRACK.play()
    # Game variables
    playing = False
    idle = False
    home_screen = True
    if restart == 1:
        idle = True
        home_screen = False
    fish_momentum = 10
    background_x = 0
    background_x2 = 2400
    final_score = 0

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
                   pygame.Rect(700, pos_1 + NET_GAP + NET_HEIGHT, 10, 400),
                   pygame.Rect(1100, pos_2 + NET_GAP + NET_HEIGHT, 10, 400),
                   pygame.Rect(1500, pos_3 + NET_GAP + NET_HEIGHT, 10, 400)]
    top_nets_active, top_rods_active = (nets_active[0:3]), (nets_active[3:6])
    bot_nets_active, bot_rods_active = (nets_active[6:9]), (nets_active[9:12])

    clock = pygame.time.Clock()  # fps limiter

    # Home Screen
    if restart == 0:
        draw_window_home_screen()

    run = True
    while run:  # game loop
        clock.tick(60)  # fps limiter
        for event in pygame.event.get():  # game events
            if event.type == pygame.QUIT:  # stop program when game window closed
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not home_screen:
                    fish_momentum -= 27
                    FISH_FLOP_SOUND.play()
                    idle = False
                    playing = True

                if event.key == pygame.K_RETURN:
                    MENU_SELECT.play()
                    home_screen = False
                    idle = True

            if event.type == COLLISION_ROD:
                ROD_HIT.play()
                run = False
                if final_score > high_score:
                    high_score = final_score

            if event.type == COLLISION_NET:
                NET_HIT.play()
                run = False
                if final_score > high_score:
                    high_score = final_score

            if event.type == ONE_POINT:
                final_score += 1

        if home_screen:
            if not home_screen:
                break
            title = pygame.Rect(-2, 0, 600, 500)
            small_fish = pygame.Rect(248, 300, 30, 30)
            high_score_txt = TITLE_FONT_SMALL.render('Current High Score:', True, LIGHT_BLUE)
            hs_high_score = HIGH_SCORE_FONT.render('69', True, LIGHT_BLUE)
            cont_txt = TITLE_FONT.render('Press Enter To Continue', True, LIGHT_BLUE)
            pygame.time.delay(800)
            if not home_screen:
                break
            WIN.blit(cont_txt, (400 - cont_txt.get_width() // 2, 10))
            pygame.display.update()
            pygame.time.delay(800)
            if not home_screen:
                break
            WIN.blit(BACKGROUND, (0, 0))
            WIN.blit(FLIPPED_FISH, small_fish)
            WIN.blit(TITLE, title)
            WIN.blit(high_score_txt, (550, 230))
            WIN.blit(hs_high_score, (450 + high_score_txt.get_width() // 2 + hs_high_score.get_width() // 2,
                                     220 + high_score_txt.get_height()))
            pygame.display.update()

        if idle:
            final_score_text = TITLE_FONT.render(f"Score: {str(final_score)}", True, WHITE)
            high_score_text = TITLE_FONT.render(f"High Score: {high_score}", True, WHITE)
            begin_txt = TITLE_FONT_SMALL.render('Press Space To Jump', True, LIGHT_BLUE)
            WIN.blit(BACKGROUND, (background_x, 0))
            WIN.blit(BACKGROUND, (background_x2, 0))
            WIN.blit(final_score_text, (10, 50))
            WIN.blit(high_score_text, (10, 0))
            WIN.blit(FISH_SPRITE, fish)
            WIN.blit(begin_txt, (fish.x - 80, fish.y - 50))
            for rod in top_rods_active:
                WIN.blit(ROD_SPRITE, rod)

            for rod in bot_rods_active:
                WIN.blit(BOT_ROD_SPRITE, rod)

            for net in top_nets_active:
                WIN.blit(NET_SPRITE, net)

            for net in bot_nets_active:
                WIN.blit(BOT_NET_SPRITE, net)

            pygame.display.update()

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

            draw_window_game(fish, top_nets_active, top_rods_active, bot_nets_active,
                             bot_rods_active, background_x, background_x2, final_score, high_score)

    main(1, high_score)


if __name__ == '__main__':
    main()
