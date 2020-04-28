# Standard library imports
from types import SimpleNamespace

OS = SimpleNamespace(**{
    'LINUX': 'linux',
    'WINDOWS': 'windows'
})

AMOUNT = SimpleNamespace(**{
    'PLAYFIELD_ROWS': 12,
    'PLAYFIELD_COLUMNS': 6,
    'TILE_TYPES': 9,
    'CURSOR_ROWS': 11,
    'CURSOR_COLUMNS': 4
})

PIXELSIZE = SimpleNamespace(**{
    'TILE_WIDTH': 16,
    'TILE_HEIGHT': 16,
    'GAMEWINDOW_WIDTH': 256,
    'GAMEWINDOW_HEIGHT': 224,
    'GAMEWINDOW_OFFSET_X': 8,
    'GAMEWINDOW_OFFSET_Y': 70,
    'PLAYFIELD_WIDTH': 16 * 6,
    'PLAYFIELD_HEIGHT': 16 * 12,
    'PLAYFIELD_OFFSET_X_P1': 8,
    'PLAYFIELD_OFFSET_X_P2': 145 + 8,
    'PLAYFIELD_OFFSET_Y': 23,
    'CURSOR_WIDTH': 35,
    'CURSOR_HEIGHT': 20
})

DIRECTION = SimpleNamespace(**{
    'LEFT': -1,
    'RIGHT': 1
})

ACTION = SimpleNamespace(**{
    'MOVE_UP' : 1,
    'MOVE_DOWN' : 2,
    'MOVE_LEFT' : 3,
    'MOVE_RIGHT' : 4,
    'SWITCH_PANELS' : 5,
    'STACK_UP' : 6,
    'DO_NOTHING' : 7
})
MOVES = [ACTION.MOVE_UP, ACTION.MOVE_DOWN, ACTION.MOVE_LEFT, ACTION.MOVE_RIGHT]

TILE = SimpleNamespace(**{
    'PURPLE': 0,
    'YELLOW': 1,
    'GREEN': 2,
    'AQUAMARINE': 3,
    'RED': 4,
    'GREY': 5,
    'BLUE': 6,
    'CONCRETE': 7,
    'STEEL': 8
})
PANELS = [TILE.PURPLE, TILE.YELLOW, TILE.GREEN, TILE.AQUAMARINE, TILE.RED, TILE.GREY, TILE.BLUE]
GARBAGE = [TILE.CONCRETE, TILE.STEEL]

GAMEMODE = SimpleNamespace(**{
    'SINGLE_PLAYER': 'single_player',
    'VS': 'vs'
})

PLAYER = SimpleNamespace(**{
    'ONE': 0,
    'TWO': 1
})
PLAYERS = [PLAYER.ONE, PLAYER.TWO]

BOT = SimpleNamespace(**{
    'LAURENS': 'laurens',
    'DANIEL': 'daniel'
})

EMULATOR = SimpleNamespace(**{
    'PATH_LINUX': 'zsnes',
    'PATH_WINDOWS': 'nintendo/windows/snes9x-x64.exe',
    'ROM_FILENAME': 'tetris_attack.smc',
    'ROM_PATH': 'nintendo/tetris_attack.smc'
})

ACTION_KEY_MAPPING_P1 = {
    ACTION.MOVE_UP: 'w',
    ACTION.MOVE_DOWN: 's',
    ACTION.MOVE_LEFT: 'a',
    ACTION.MOVE_RIGHT: 'd',
    ACTION.SWITCH_PANELS: 'f',
    ACTION.STACK_UP: 'm'
}

ACTION_KEY_MAPPING_P2 = {
    ACTION.MOVE_UP: 'UP',
    ACTION.MOVE_DOWN: 'DOWN',
    ACTION.MOVE_LEFT: 'LEFT',
    ACTION.MOVE_RIGHT: 'RIGHT',
    ACTION.SWITCH_PANELS: 'SPACE',
    ACTION.STACK_UP: 'R_CTRL'
}

COLOR_TILE_MAPPING = {
    " ".join(map(str, [255,  24, 255])): TILE.PURPLE,
    " ".join(map(str, [255, 255,   0])): TILE.YELLOW,
    " ".join(map(str, [  0, 255,   0])): TILE.GREEN,
    " ".join(map(str, [  0, 255, 255])): TILE.AQUAMARINE,
    " ".join(map(str, [255,  16,  16])): TILE.RED,
    " ".join(map(str, [132, 134, 132])): TILE.GREY,
    " ".join(map(str, [ 66, 113, 255])): TILE.BLUE,
    " ".join(map(str, [  8,  81, 214])): TILE.CONCRETE,
    " ".join(map(str, [148,  24,  24])): TILE.CONCRETE,
    " ".join(map(str, [ 99, 105, 107])): TILE.STEEL,
    " ".join(map(str, [ 57,  56,  57])): TILE.STEEL
}