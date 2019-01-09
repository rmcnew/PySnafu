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

import sys

import pygame
from pygame.locals import *

from shared import *
from worm import Worm
from bolt import Bolt


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


def init_worm1():
    # Set a random start point on the left side.
    start_x = random.randint(5, (GRID_WIDTH/2) - 6)
    start_y = random.randint(5, GRID_HEIGHT - 6)
    worm_coordinates = [{X: start_x, Y: start_y},
                        {X: start_x - 1, Y: start_y},
                        {X: start_x - 2, Y: start_y}]
    direction = RIGHT
    return Worm(Colors.DARK_BLUE, Colors.BLUE, direction, worm_coordinates)


def init_worm2():
    # Set a random start point on the right side.
    start_x = random.randint((GRID_WIDTH/2) + 5, GRID_WIDTH - 6)
    start_y = random.randint(5, GRID_HEIGHT - 6)
    worm_coordinates = [{X: start_x, Y: start_y},
                        {X: start_x - 1, Y: start_y},
                        {X: start_x - 2, Y: start_y}]
    direction = RIGHT
    return Worm(Colors.DARK_GREEN, Colors.GREEN, direction, worm_coordinates)


def init_apples():
    apples = []
    # Start the apples in random places.
    for i in range(APPLE_COUNT):
        apples.append(get_random_location())
    return apples


def fire_bolt(worm, bolts):
    if worm.direction == UP:
        bolts.append(Bolt(UP, {X: worm.coordinates[HEAD][X], Y: worm.coordinates[HEAD][Y] - 1}))
    elif worm.direction == DOWN:
        bolts.append(Bolt(DOWN, {X: worm.coordinates[HEAD][X], Y: worm.coordinates[HEAD][Y] + 1}))
    elif worm.direction == LEFT:
        bolts.append(Bolt(LEFT, {X: worm.coordinates[HEAD][X] - 1, Y: worm.coordinates[HEAD][Y]}))
    elif worm.direction == RIGHT:
        bolts.append(Bolt(RIGHT, {X: worm.coordinates[HEAD][X] + 1, Y: worm.coordinates[HEAD][Y]}))


def handle_input_events(worm1, worm2, bolts):
    # handle input events
    for event in pygame.event.get():  # event handling loop
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            # worm 1 controls
            if (event.key == K_a) and worm1.direction != RIGHT:
                worm1.direction = LEFT
            elif (event.key == K_d) and worm1.direction != LEFT:
                worm1.direction = RIGHT
            elif (event.key == K_w) and worm1.direction != DOWN:
                worm1.direction = UP
            elif (event.key == K_s) and worm1.direction != UP:
                worm1.direction = DOWN
            elif event.key == K_LCTRL:
                fire_bolt(worm1, bolts)
            # worm 2 controls
            elif (event.key == K_LEFT) and worm2.direction != RIGHT:
                worm2.direction = LEFT
            elif (event.key == K_RIGHT) and worm2.direction != LEFT:
                worm2.direction = RIGHT
            elif (event.key == K_UP) and worm2.direction != DOWN:
                worm2.direction = UP
            elif (event.key == K_DOWN) and worm2.direction != UP:
                worm2.direction = DOWN
            elif event.key == K_RCTRL:
                fire_bolt(worm2, bolts)
            # both worm controls
            elif (event.key == K_KP4) and worm2.direction != RIGHT and worm1.direction != RIGHT:
                worm2.direction = LEFT
                worm1.direction = LEFT
            elif (event.key == K_KP6) and worm2.direction != LEFT and worm1.direction != LEFT:
                worm2.direction = RIGHT
                worm1.direction = RIGHT
            elif (event.key == K_KP8) and worm2.direction != DOWN and worm1.direction != DOWN:
                worm2.direction = UP
                worm1.direction = UP
            elif (event.key == K_KP2) and worm2.direction != UP and worm1.direction != UP:
                worm2.direction = DOWN
                worm1.direction = DOWN
            # quit
            elif event.key == K_ESCAPE:
                terminate()


def run_game():
    worm1 = init_worm1()  # WASD controls
    worm2 = init_worm2()  # arrow controls
    apples = init_apples()
    stones = []
    bolts = []

    while True:  # main game loop
        handle_input_events(worm1, worm2, bolts)

        # check for collisions
        if worm1.died(worm2):
            return "Worm 2 wins!"
        if worm2.died(worm1):
            return "Worm 1 wins!"

        # check if worm has eaten an apple
        apples = worm1.ate_apple(apples)
        apples = worm2.ate_apple(apples)

        # move bolts
        for bolt in bolts:
            bolt.move()
        # move worms
        worm1.move()
        worm2.move()

        # update display
        DISPLAY_SURF.fill(BG_COLOR.value)
        draw_grid()
        draw_worm(worm1)
        draw_worm(worm2)
        draw_bolts(bolts)
        draw_apples(apples)
        draw_scores(worm1, worm2)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def draw_press_key_message():
    press_key_surf = BASIC_FONT.render('Press a key to play.', True, Colors.DARK_GRAY.value)
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
    title_surf1 = title_font.render(PYSNAFU, True, Colors.WHITE.value, Colors.BLUE.value)
    title_surf2 = title_font.render(PYSNAFU, True, Colors.RED.value)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAY_SURF.fill(BG_COLOR.value)
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
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def show_game_over_screen():
    game_over_font = pygame.font.Font(SANS_FONT, 150)
    game_surf = game_over_font.render('Game', True, Colors.WHITE.value)
    over_surf = game_over_font.render('Over', True, Colors.WHITE.value)
    game_rect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    game_rect.midtop = (WINDOW_WIDTH / 2, 10)
    over_rect.midtop = (WINDOW_WIDTH / 2, game_rect.height + 10 + 25)

    DISPLAY_SURF.blit(game_surf, game_rect)
    DISPLAY_SURF.blit(over_surf, over_rect)
    draw_press_key_message()
    pygame.display.update()
    pygame.time.wait(500)
    check_for_key_press()  # clear out any key presses in the event queue

    while True:
        if check_for_key_press():
            pygame.event.get()  # clear event queue
            return


def draw_scores(worm1, worm2):
    # worm 1 score
    worm1_score_surf = BASIC_FONT.render('Score: %s' % worm1.score(), True, Colors.WHITE.value)
    worm1_score_rect = worm1_score_surf.get_rect()
    worm1_score_rect.topleft = (120, 10)
    DISPLAY_SURF.blit(worm1_score_surf, worm1_score_rect)
    # worm 2 score
    worm2_score_surf = BASIC_FONT.render('Score: %s' % worm2.score(), True, Colors.WHITE.value)
    worm2_score_rect = worm2_score_surf.get_rect()
    worm2_score_rect.topleft = (WINDOW_WIDTH - 120, 10)
    DISPLAY_SURF.blit(worm2_score_surf, worm2_score_rect)


def draw_worm(worm):
    for coord in worm.coordinates:
        x = coord[X] * CELL_SIZE
        y = coord[Y] * CELL_SIZE
        worm_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, worm.lineColor.value, worm_segment_rect)
        worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(DISPLAY_SURF, worm.fillColor.value, worm_inner_segment_rect)


def draw_apples(apples):
    for apple in apples:
        x = apple[X] * CELL_SIZE
        y = apple[Y] * CELL_SIZE
        apple_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, Colors.RED.value, apple_rect)

def draw_bolts(bolts):
    for bolt in bolts:
        x = bolt.coordinates[X] * CELL_SIZE
        y = bolt.coordinates[Y] * CELL_SIZE
        bolt_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, Colors.YELLOW.value, bolt_rect)

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):  # draw vertical lines
        pygame.draw.line(DISPLAY_SURF, Colors.DARK_GRAY.value, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAY_SURF, Colors.DARK_GRAY.value, (0, y), (WINDOW_WIDTH, y))


if __name__ == '__main__':
    main()
