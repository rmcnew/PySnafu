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

# bolt class
from shared import *


class Bolt:
    def __init__(self, direction, start_coordinates):
        self.direction = direction
        self.coordinates = start_coordinates

    def move(self):
        # move the bolt
        if self.direction == UP:
            self.coordinates = {X: self.coordinates[X], Y: self.coordinates[Y] - BOLT_SPEED}
        elif self.direction == DOWN:
            self.coordinates = {X: self.coordinates[X], Y: self.coordinates[Y] + BOLT_SPEED}
        elif self.direction == LEFT:
            self.coordinates = {X: self.coordinates[X] - BOLT_SPEED, Y: self.coordinates[Y]}
        elif self.direction == RIGHT:
            self.coordinates = {X: self.coordinates[X] + BOLT_SPEED, Y: self.coordinates[Y]}

    def get_moved_coords(self):
        # calculate the grid squares that the bolt just passed through
        bolt_coords = []
        bolt_coords.append(self.coordinates)
        if self.direction == UP:
            for y in range(self.coordinates[Y], self.coordinates[Y] + BOLT_SPEED):
                bolt_coords.append({X: self.coordinates[X], Y: y})
        elif self.direction == DOWN:
            for y in range(self.coordinates[Y], self.coordinates[Y] - BOLT_SPEED):
                bolt_coords.append({X: self.coordinates[X], Y: y})
        elif self.direction == LEFT:
            for x in range(self.coordinates[X], self.coordinates[X] + BOLT_SPEED):
                bolt_coords.append({X: x, Y: self.coordinates[Y]})
        elif self.direction == RIGHT:
            for x in range(self.coordinates[X], self.coordinates[X] - BOLT_SPEED):
                bolt_coords.append({X: x, Y: self.coordinates[Y]})
        return bolt_coords
