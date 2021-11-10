#basic game loop structure

import pygame as pg
import sys
import random
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		pg.key.set_repeat(20, 70)
		self.load_data()

	def	load_data(self):
		game_folder = path.dirname(__file__)
		img_folder = path.join(game_folder, 'img')
		self.map = Map(path.join(game_folder, 'map2.txt'))
		self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG_DOWN)).convert_alpha()
		self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG_FRONT)).convert_alpha()
		self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
		self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))

	def	new(self):
		#sert a initié les variables pour un nouveau jeu
		self.all_sprites = pg.sprite.Group()
		self.walls = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		#sert a faire apparaitre les murs
		for row, tiles in enumerate(self.map.data):
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row)
				if tile == 'M':
					Mob(self, col, row)
				if tile == 'P':
					self.player = Player(self, col, row)
		self.camera = Camera(self.map.width, self.map.height)

	def run(self):
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.draw()

	def	quit(self):
		pg.quit()
		sys.exit()

	def update(self):
		self.all_sprites.update()
		self.camera.update(self.player)
	
	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
	
	def draw(self):
		pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		self.screen.fill(BGCOLOR)
		""" self.draw_grid() """
		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		pg.display.flip()

	def events(self):
		#sert a maper les events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
	
	def show_start_screen(self):
		pass

	def show_go_screen(self):
		pass

g = Game()
g.show_start_screen()
while True:
	g.new()
	g.run()
	g.show_go_screen()
