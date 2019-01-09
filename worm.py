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

# worm class
from shared import *


class Worm:
    def __init__(self, line_color, fill_color, start_direction, start_coordinates):
        self.lineColor = line_color
        self.fillColor = fill_color
        self.direction = start_direction
        self.coordinates = start_coordinates
        self.apple_points = 0

    def died(self, other_worm, stones):
        # did the worm hit the wall?
        if self.coordinates[HEAD][X] == -1 or self.coordinates[HEAD][X] == GRID_WIDTH or \
                self.coordinates[HEAD][Y] == -1 or self.coordinates[HEAD][Y] == GRID_HEIGHT:
            return True
        # did the worm hit itself?
        for worm_body in self.coordinates[1:]:
            if worm_body[X] == self.coordinates[HEAD][X] and worm_body[Y] == self.coordinates[HEAD][Y]:
                return True
        # did the worm hit the other worm?
        for worm_body in other_worm.coordinates[1:]:
            if worm_body[X] == self.coordinates[HEAD][X] and worm_body[Y] == self.coordinates[HEAD][Y]:
                return True
        # did the worm hit a stone?
        for stone in stones:
            if self.coordinates[HEAD][X] == stone[X] and self.coordinates[HEAD][Y] == stone[Y]:
                return True
        return False

    def ate_apple(self, apples):
        new_apples = []
        eaten = False
        for apple in apples:
            if self.coordinates[HEAD][X] == apple[X] and self.coordinates[HEAD][Y] == apple[Y]:
                # don't remove worm's tail segment
                eaten = True
                self.apple_points += APPLE_POINT_VALUE
                new_apples.append(get_random_location())  # set a new apple somewhere
            else:
                new_apples.append(apple)
        if not eaten:
            del self.coordinates[-1]  # remove worm's tail segment
        return new_apples
    
    def move(self):
        # move the worm by adding a segment in the direction it is moving
        if self.direction == UP:
            self.coordinates.insert(0, {X: self.coordinates[HEAD][X], Y: self.coordinates[HEAD][Y] - 1})
        elif self.direction == DOWN:
            self.coordinates.insert(0, {X: self.coordinates[HEAD][X], Y: self.coordinates[HEAD][Y] + 1})
        elif self.direction == LEFT:
            self.coordinates.insert(0, {X: self.coordinates[HEAD][X] - 1, Y: self.coordinates[HEAD][Y]})
        elif self.direction == RIGHT:
            self.coordinates.insert(0, {X: self.coordinates[HEAD][X] + 1, Y: self.coordinates[HEAD][Y]})

    def length(self):
        # get the length of the worm for scoring purposes
        return len(self.coordinates)

    def score(self):
        return self.apple_points * int(self.length() / 3)

    def was_hit_by_bolt(self, bolts, stones):
        for bolt in bolts:
            bolt_coords = bolt.get_moved_coords()
            for bolt_segment in bolt_coords:
                for worm_index in range(HEAD + 1, len(self.coordinates) - 1):
                    if bolt_segment[X] == self.coordinates[worm_index][X] and bolt_segment[Y] == self.coordinates[worm_index][Y]:
                        # bolt hit worm, the rest of the worm body turns to stone
                        for hit_index in range(worm_index, len(self.coordinates) - 1):
                            stones.append(self.coordinates[hit_index])
                        del self.coordinates[worm_index:len(self.coordinates)]
                        return


