import pygame
import sys
import random
import math


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 425))
    screen.blit(floor_surface, (floor_x_pos + 576, 425))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 150))
    return bottom, top


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def getScore(pipes):
    global score
    global high_score
    new_score = 0
    for pipe in pipes:
        if pipe.centerx <= 100:
            new_score += 0.5

    if new_score > score:
        score_sound.play()

    score = int(new_score)
    high_score = max(high_score, score)

    return score


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 425:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def checkCollision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 425:
        death_sound.play()
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 5, 1)
    return new_bird


def bird_animimation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display():
    score_surface = game_font.render(
        "Score: " + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(100, 75))
    screen.blit(score_surface, score_rect)

    if game_active == False:
        high_score_surface = game_font.render(
            "High Score: " + str(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(425, 75))
        screen.blit(high_score_surface, high_score_rect)


# Define variables
gravity = 0.125  # Positive means you are going down
bird_movement = 0
game_active = True
score = 0
high_score = 0

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=812)
pygame.init()
pygame.display.set_caption("Flappy Birds")
# Tells you the size of the screen
screen = pygame.display.set_mode((576, 512))
# Initializes a class that allows you to control the frames per second
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)  # Initializes a FONT

# importing the background image
bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (576, 512))

# importing the floor background
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (576, 112))
floor_x_pos = 0

# importing the bird animation
bird_downflap = pygame.image.load(
    'assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]

bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512/2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 2000)

# importing the pipes
pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_list = []
pipe_height = [190, 200,  224, 254, 300,  325, 360, 380]
SPAWNPIPE = pygame.USEREVENT  # Even listener but triggered by timer
pygame.time.set_timer(SPAWNPIPE, 1200)  # Event will trigger afte 1.2 seconds

# Messages
play_game = pygame.image.load('assets/message.png').convert_alpha()
play_game_rect = play_game.get_rect(center=(288, 256))

# Audio
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

while True:
    for event in pygame.event.get():  # Checks for event selectors
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # Checks if any keys are pressed down
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4.5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512 / 2)
                bird_movement = -4
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % 3

        bird_surface, bird_rect = bird_animimation()

    screen.blit(bg_surface, (0, 0))
    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = checkCollision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
    else:
        screen.blit(play_game, play_game_rect)

    # Score
    score = getScore(pipe_list)
    score_display()

    # Floor
    draw_floor()
    floor_x_pos -= 1

    if floor_x_pos == -576:
        floor_x_pos = 0

    pygame.display.update()
    # Will not allow the game to over 120 frames per second but can be less than
    clock.tick(100)
