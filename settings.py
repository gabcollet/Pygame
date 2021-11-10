import pygame as pg

#define colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (255, 222, 142)

#Game settings
WIDTH = 1024 #grid 32x24
HEIGHT = 768
FPS = 60
TITLE = "Jeu Demo"
BGCOLOR = BROWN

TILESIZE = 64 #use power of 2 ex : 16, 32, 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Player settings
PLAYER_SPEED = 300 #pixel per sec
""" PLAYER_ROT_SPEED = 250 """
PLAYER_IMG_RIGHT = 'Player/player_side/tile000.png'
PLAYER_IMG_LEFT = 'Player/player_side/left00.png'
PLAYER_IMG_DOWN = 'Player/player_front/tile000.png'
PLAYER_IMG_UP = 'Player/player_back/tile000.png'
PLAYER_IMG_DOWN_R = 'Player/player_angle_1/tile000.png'
PLAYER_IMG_DOWN_L = 'Player/player_angle_1/rev00.png'
PLAYER_IMG_UP_R = 'Player/player_angle_2/tile000.png'
PLAYER_IMG_UP_L = 'Player/player_angle_2/rev00.png'
PLAYER_HIT_RECT = pg.Rect(0 , 0, 25, 48)

WALL_IMG = 'Buildings/wall.png'

#Mob settings
#mob sprites only have 4 directions :3
MOB_IMG_FRONT = 'Mobs/Cactus/mob_front/tile000.png'
MOB_IMG_BACK = 'Mobs/Cactus/mob_back/tile000.png'
MOB_IMG_RIGHT = 'Mobs/Cactus/mob_side/tile000.png'
MOB_IMG_LEFT = 'Mobs/Cactus/mob_side/rev00.png'