import pygame as pg
vec = pg.math.Vector2

#define colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
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
PLAYER_HEALTH = 100
PLAYER_SPEED = 300 #pixel per sec
""" PLAYER_ROT_SPEED = 250 """
PLAYER_IMG_RIGHT = 'Player/player_side/tile029.png'
PLAYER_IMG_LEFT = 'Player/player_side/rev29.png'
PLAYER_IMG_DOWN = 'Player/player_front/tile029.png'
PLAYER_IMG_UP = 'Player/player_back/tile029.png'
PLAYER_IMG_DOWN_R = 'Player/player_angle_1/tile029.png'
PLAYER_IMG_DOWN_L = 'Player/player_angle_1/rev29.png'
PLAYER_IMG_UP_R = 'Player/player_angle_2/tile029.png'
PLAYER_IMG_UP_L = 'Player/player_angle_2/rev29.png'
PLAYER_HIT_RECT = pg.Rect(0 , 0, 20, 20) #25,48
BARREL_OFFSET = vec(20, 8)

#Gun settings
BULLET_IMG = 'Player/bullet1.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1500
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 10

WALL_IMG = 'Buildings/wall.png'

#Mob settings
#mob sprites only have 4 directions :3
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_IMG_FRONT = 'Mobs/Cactus/mob_front/tile000.png'
MOB_IMG_BACK = 'Mobs/Cactus/mob_back/tile000.png'
MOB_IMG_RIGHT = 'Mobs/Cactus/mob_side/tile000.png'
MOB_IMG_LEFT = 'Mobs/Cactus/mob_side/rev00.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 20, 20)