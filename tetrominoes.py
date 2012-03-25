# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: tetrominoes.py
# @Date: 2011年02月26日 星期六 15时57分20秒

# Constant variables
FPS          = 25
WINDOWWIDTH  = 640
WINDOWHEIGHT = 480
BLOCKSIZE    = 20
BOARDWIDTH   = 10
BOARDHEIGHT  = 20
BLANK        = -1


# Key repeat frequency
MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ     = 0.15


# Board position
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BLOCKSIZE) / 2)
BOARDTOP = WINDOWHEIGHT - (BOARDHEIGHT * BLOCKSIZE) - 5


# Palette
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
RED      = (239,  52,  52)
GREEN    = (  0, 191,   0)
BLUE     = (  0,  85, 255)
YELLOW   = (255, 246,   0)
GRAY     = (191, 189, 189)
DARKGRAY = (219, 219, 219)

BORDERCOLOR = BLACK
BGCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)


# Shape (5 * 5)
S_SHAPE = [
  ['.....',
   '.....',
   '..OO.',
   '.OO..',
   '.....'],
  ['.....',
   '..O..',
   '..OO.',
   '...O.',
   '.....']
]

Z_SHAPE = [
  ['.....',
   '.....',
   '.OO..',
   '..OO.',
   '.....'],
  ['.....',
   '..O..',
   '.OO..',
   '.O...',
   '.....']
]

I_SHAPE = [
  ['..O..',
   '..O..',
   '..O..',
   '..O..',
   '.....'],
  ['.....',
   '.....',
   'OOOO.',
   '.....',
   '.....']
]

O_SHAPE = [
  ['.....',
   '.....',
   '.OO..',
   '.OO..',
   '.....']
]

J_SHAPE = [
  ['.....',
   '.O...',
   '.OOO.',
   '.....',
   '.....'],
  ['.....',
   '..OO.',
   '..O..',
   '..O..',
   '.....'],
  ['.....',
   '.....',
   '.OOO.',
   '...O.',
   '.....'],
  ['.....',
   '..O..',
   '..O..',
   '.OO..',
   '.....']
]

L_SHAPE = [
  ['.....',
   '...O.',
   '.OOO.',
   '.....',
   '.....'],
  ['.....',
   '..O..',
   '..O..',
   '..OO.',
   '.....'],
  ['.....',
   '.....',
   '.OOO.',
   '.O...',
   '.....'],
  ['.....',
   '.OO..',
   '..O..',
   '..O..',
   '.....']
]

T_SHAPE = [
  ['.....',
   '..O..',
   '.OOO.',
   '.....',
   '.....'],
  ['.....',
   '..O..',
   '..OO.',
   '..O..',
   '.....'],
  ['.....',
   '.....',
   '.OOO.',
   '..O..',
   '.....'],
  ['.....',
   '..O..',
   '.OO..',
   '..O..',
   '.....']
]

SHAPES = {
  'S': S_SHAPE,
  'Z': Z_SHAPE,
  'J': J_SHAPE,
  'L': L_SHAPE,
  'I': I_SHAPE,
  'O': O_SHAPE,
  'T': T_SHAPE
}

# loop through each shape
for p in SHAPES:
  # loop through each rotation of the shape
  for i in range(len(SHAPES[p])):
    shapeData = []
    # loop through each column of the rotation
    for x in range(5):
      column = []
      # loop through each character of the column
      for y in range(5):
        if SHAPES[p][i][x][y] == '.':
          column.append(BLANK)
        else:
          column.append(1)
      shapeData.append(column)
    SHAPES[p][i] = shapeData
