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

# shared constants and functions
import random
from colors import Colors

# frames per second
FPS = 15

# game window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 960

# cell size and game grid
CELL_SIZE = 10
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
GRID_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
GRID_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

# background color
BG_COLOR = Colors.BLACK

# game title
PYSNAFU = 'PySnafu'

# game font
SANS_FONT = 'freesansbold.ttf'

# coordinates
X = 'x'
Y = 'y'

# cardinal directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# syntactic sugar: index of the worm's head
HEAD = 0

# maximum number of simultaneous apples
APPLE_COUNT = 4


def get_random_location():
    return {X: random.randint(0, GRID_WIDTH - 1), Y: random.randint(0, GRID_HEIGHT - 1)}
