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

#Game settings (1024, 768)
WIDTH = 1920 #grid 32x24
HEIGHT = 970
FPS = 60
TITLE = "Jeu Demo"
BGCOLOR = BROWN

TILESIZE = 64 #use power of 2 ex : 16, 32, 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300 #pixel per sec
PLAYER_HIT_RECT = pg.Rect(0 , 0, 20, 20)
BARREL_OFFSET = vec(20, 8)

#Player sprites
PLAYER_IMG = ['Player/player_side/tile029.png', 'Player/player_side/tile030.png',
				'Player/player_angle_1/tile029.png', 'Player/player_angle_1/tile030.png',
				'Player/player_front/tile029.png', 'Player/player_front/tile030.png',
				'Player/player_angle_1/rev29.png', 'Player/player_angle_1/rev30.png',
				'Player/player_side/rev29.png', 'Player/player_side/rev30.png',
				'Player/player_angle_2/rev29.png', 'Player/player_angle_2/rev30.png',
				'Player/player_back/tile029.png', 'Player/player_back/tile030.png',
				'Player/player_angle_2/tile029.png', 'Player/player_angle_2/tile030.png']

#Gun settings
BULLET_IMG = 'Player/bullet1.png'
BULLET_SPEED = 1000
BULLET_LIFETIME = 1500
BULLET_RATE = 200
KICKBACK = 200
GUN_SPREAD = 2
BULLET_DAMAGE = 10

#Mob settings
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 20, 20)
AVOID_RADIUS = 50
DETECT_RADIUS = 750

#mob sprites only have 4 directions :3
MOB_IMG = ['Mobs/Cactus/mob_front/tile000.png', 'Mobs/Cactus/mob_back/tile000.png',
			'Mobs/Cactus/mob_side/tile000.png', 'Mobs/Cactus/mob_side/rev00.png']

TREE_IMG = ['tree_green.png', 'tree_red.png']

#Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 3
SPACE_LAYER = 4
BULLET_LAYER = 5
TREE_LAYER = 6
EFFECTS_LAYER = 6
ITEM_LAYER = 1

#Items
ITEM_IMAGES = {'health' : 'Items/HeartMoving1.png',
				'speed' : 'Items/ChickenThighMoving1.png'}
HEALTH_PACK_AMOUNT = 50
BOOST_TIME = 6 #in sec
BOB_RANGE = 15 #in pixel
BOB_SPEED = 0.4

#Sounds

BG_MUSIC = 'Western_Adventures.mp3'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
						'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['man-dying.wav']
WEAPON_SOUNDS_GUN = ['gunshot/gunshot-high-1.wav', 'gunshot/gunshot-high-2.wav', 'gunshot/gunshot-high-3.wav',
					 'gunshot/gunshot-high-4.wav', 'gunshot/gunshot-high-5.wav', 'gunshot/gunshot-high-6.wav']
EFFECTS_SOUNDS = {'level_start' : 'level_start.wav',
					'health_up' : 'health_pack.wav'}						