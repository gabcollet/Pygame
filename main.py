#basic game loop structure

import pygame as pg
import sys
from settings import *
from sprites import *

class Game:
	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		pg.key.set_repeat(100, 100)
		self.load_data()

	def	load_data(self):
		pass

	def	new(self):
		#sert a initié les variables pour un nouveau jeu
		self.all_sprites = pg.sprite.Group()
		self.walls = pg.sprite.Group()
		self.player = Player(self, 10, 10)
		for x in range(10, 20):
			Wall(self, x, 5)
	
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
	
	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
	
	def draw(self):
		self.screen.fill(BGCOLOR)
		self.draw_grid()
		self.all_sprites.draw(self.screen)
		pg.display.flip()

	def events(self):
		#sert a maper les events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
				if event.key == pg.K_LEFT:
					self.player.move(dx=-1)
				if event.key == pg.K_RIGHT:
					self.player.move(dx=1)
				if event.key == pg.K_UP:
					self.player.move(dy=-1)
				if event.key == pg.K_DOWN:
					self.player.move(dy=1)
	
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
