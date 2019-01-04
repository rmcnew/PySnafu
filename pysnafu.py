# PySnafu
# Pygame-based Snafu based on Al Sweigart's wormy.py
# 
# BSD 2-Clause License
# 
# PySnafu, Copyright (c) 2019, Richard Scott McNew.
# All rights reserved.
# 
# PySnafu is derived from:
# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import random
import pygame
import sys
from pygame.locals import *

FPS = 15
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960
CELL_SIZE = 10
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)
PYSNAFU = 'PySnafu'
SANS_FONT = 'freesansbold.ttf'

# R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 155, 0)
DARK_GRAY = (40, 40, 40)
BG_COLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the worm's head


def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font(SANS_FONT, 18)
    pygame.display.set_caption(PYSNAFU)

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()


def run_game():
    # Set a random start point.
    start_x = random.randint(5, CELL_WIDTH - 6)
    start_y = random.randint(5, CELL_HEIGHT - 6)
    worm_coordinates = [{'x': start_x,     'y': start_y},
                  {'x': start_x - 1, 'y': start_y},
                  {'x': start_x - 2, 'y': start_y}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = get_random_location()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if worm_coordinates[HEAD]['x'] == -1 or worm_coordinates[HEAD]['x'] == CELL_WIDTH or worm_coordinates[HEAD]['y'] == -1 or worm_coordinates[HEAD]['y'] == CELL_HEIGHT:
            return # game over
        for wormBody in worm_coordinates[1:]:
            if wormBody['x'] == worm_coordinates[HEAD]['x'] and wormBody['y'] == worm_coordinates[HEAD]['y']:
                return # game over

        # check if worm has eaten an apple
        if worm_coordinates[HEAD]['x'] == apple['x'] and worm_coordinates[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = get_random_location() # set a new apple somewhere
        else:
            del worm_coordinates[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            new_head = {'x': worm_coordinates[HEAD]['x'], 'y': worm_coordinates[HEAD]['y'] - 1}
        elif direction == DOWN:
            new_head = {'x': worm_coordinates[HEAD]['x'], 'y': worm_coordinates[HEAD]['y'] + 1}
        elif direction == LEFT:
            new_head = {'x': worm_coordinates[HEAD]['x'] - 1, 'y': worm_coordinates[HEAD]['y']}
        elif direction == RIGHT:
            new_head = {'x': worm_coordinates[HEAD]['x'] + 1, 'y': worm_coordinates[HEAD]['y']}
        worm_coordinates.insert(0, new_head)
        DISPLAY_SURF.fill(BG_COLOR)
        draw_grid()
        draw_worm(worm_coordinates)
        draw_apple(apple)
        draw_score(len(worm_coordinates) - 3)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def draw_press_key_message():
    press_key_surf = BASIC_FONT.render('Press a key to play.', True, DARK_GRAY)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 30)
    DISPLAY_SURF.blit(press_key_surf, press_key_rect)


def check_for_key_press():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key


def show_start_screen():
    title_font = pygame.font.Font(SANS_FONT, 100)
    title_surf1 = title_font.render(PYSNAFU, True, WHITE, BLUE)
    title_surf2 = title_font.render(PYSNAFU, True, RED)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAY_SURF.fill(BG_COLOR)
        rotated_surf1 = pygame.transform.rotate(title_surf1, degrees1)
        rotated_rect1 = rotated_surf1.get_rect()
        rotated_rect1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAY_SURF.blit(rotated_surf1, rotated_rect1)

        rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
        rotated_rect2 = rotated_surf2.get_rect()
        rotated_rect2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        DISPLAY_SURF.blit(rotated_surf2, rotated_rect2)

        draw_press_key_message()

        if check_for_key_press():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def get_random_location():
    return {'x': random.randint(0, CELL_WIDTH - 1), 'y': random.randint(0, CELL_HEIGHT - 1)}


def show_game_over_screen():
    game_over_font = pygame.font.Font(SANS_FONT, 150)
    game_surf = game_over_font.render('Game', True, WHITE)
    over_surf = game_over_font.render('Over', True, WHITE)
    game_rect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    game_rect.midtop = (WINDOW_WIDTH / 2, 10)
    over_rect.midtop = (WINDOW_WIDTH / 2, game_rect.height + 10 + 25)

    DISPLAY_SURF.blit(game_surf, game_rect)
    DISPLAY_SURF.blit(over_surf, over_rect)
    draw_press_key_message()
    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press() # clear out any key presses in the event queue

    while True:
        if check_for_key_press():
            pygame.event.get() # clear event queue
            return


def draw_score(score):
    score_surf = BASIC_FONT.render('Score: %s' % score, True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 120, 10)
    DISPLAY_SURF.blit(score_surf, score_rect)


def draw_worm(worm_coordinates):
    for coord in worm_coordinates:
        x = coord['x'] * CELL_SIZE
        y = coord['y'] * CELL_SIZE
        worm_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, DARK_GREEN, worm_segment_rect)
        worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(DISPLAY_SURF, GREEN, worm_inner_segment_rect)


def draw_apple(coord):
    x = coord['x'] * CELL_SIZE
    y = coord['y'] * CELL_SIZE
    apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY_SURF, RED, apple_rect)


def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):  # draw vertical lines
        pygame.draw.line(DISPLAY_SURF, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAY_SURF, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))


if __name__ == '__main__':
    main()
