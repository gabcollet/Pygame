#basic game loop structure

import pygame as pg
import sys
import random
from os import path
from settings import *
from sprites import *
from tilemap import *

#HUD functions
def draw_player_health(surf, x, y, pct):
	if pct < 0:
		pct = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 20
	fill = pct * BAR_LENGTH
	outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pg.Rect(x, y, int(fill), BAR_HEIGHT)
	if pct > 0.6:
		col = GREEN
	elif pct > 0.3:
		col = YELLOW
	else:
		col = RED
	pg.draw.rect(surf, col, fill_rect)
	pg.draw.rect(surf, WHITE, outline_rect, 2)
	
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
		map_folder = path.join(game_folder, 'maps')
		self.map = TiledMap(path.join(map_folder, 'home.tmx'))
		self.map_img = self.map.make_map()
		self.map_rect = self.map_img.get_rect()
		self.player_img = []
		for img in PLAYER_IMG:
			self.player_img.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
		self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG_FRONT)).convert_alpha()	
		self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
		self.tree_img = []
		for img in TREE_IMG:
			self.tree_img.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
		self.item_images = {}
		for item in ITEM_IMAGES:
			self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

	def	new(self):
		#sert a initié les variables pour un nouveau jeu
		self.all_sprites = pg.sprite.LayeredUpdates()
		self.walls = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.bullets = pg.sprite.Group()
		self.items = pg.sprite.Group()
		for tile_object in self.map.tmxdata.objects:
			obj_center = vec(tile_object.x + tile_object.width / 2,
							tile_object.y + tile_object.height / 2)
			if tile_object.name == 'player':
				self.player = Player(self, obj_center.x, obj_center.y)
			if tile_object.name == 'mob':
				Mob(self, obj_center.x, obj_center.y)
			if tile_object.name == 'wall':
				Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
			if tile_object.name == 'tree_green':
				Tree(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "green")
			if tile_object.name == 'tree_red':
				Tree(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "red")
			if tile_object.name in ['health']:
				Item(self, obj_center, tile_object.name)
		self.camera = Camera(self.map.width, self.map.height)
		self.draw_debug = False

	def run(self):
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.draw()
		self.quit()

	def	quit(self):
		pg.display.quit()
		pg.quit()
		sys.exit()

	def update(self):
		#update portion of the game loop
		self.all_sprites.update()
		self.camera.update(self.player)
		#player hit items
		hits = pg.sprite.spritecollide(self.player, self.items, False)
		for hit in hits:
			if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
				hit.kill()
				self.player.add_health(HEALTH_PACK_AMOUNT)
		#mobs hit player
		hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
		for hit in hits:
			self.player.health -= MOB_DAMAGE
			hit.vel = vec(0,0)
			if self.player.health <= 0:
				self.playing = False
		if hits:
			self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
		#bullet hit mobs
		hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True, collide_hit_rect)
		for hit in hits:
			hit.health -= BULLET_DAMAGE
			hit.vel = vec(0,0)
	
	def draw(self):
		pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
		for sprite in self.all_sprites:
			if isinstance(sprite, Mob):
				sprite.draw_health()
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		#part to debug with h key
			if self.draw_debug:
				pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
		#part so mob dont get over player and each other
		for sprite_mob in self.mobs:
			if self.player.hit_rect.y > sprite_mob.hit_rect.y:
				self.all_sprites.change_layer(self.player, 4)
			else:
				self.all_sprites.change_layer(self.player, 2)
		if self.draw_debug:
			for wall in self.walls:
				pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
		#HUD functions
		draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
		pg.display.flip()

	def events(self):
		#sert a maper les events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.playing = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_h:
					self.draw_debug = not self.draw_debug
		keys = pg.key.get_pressed()
		if keys[pg.K_ESCAPE]:
			self.playing = False
	
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
