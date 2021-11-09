from io import SEEK_CUR
import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from os import path

from tilemap import collide_hit_rect
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.player_img
		self.rect = self.image.get_rect()
		self.hit_rect = PLAYER_HIT_RECT
		self.hit_rect.center = self.rect.center
		self.vel = vec(0, 0)
		self.pos = vec(x, y) * TILESIZE
		""" self.rot = 0 """

	def	get_keys(self):
		""" self.rot_speed = 0 """
		self.vel = vec(0, 0)
		game_folder = path.dirname(__file__)
		img_folder = path.join(game_folder, 'img')
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.vel.x = -PLAYER_SPEED
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_LEFT)).convert_alpha()
			""" self.rot_speed = PLAYER_ROT_SPEED """
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.vel.x = PLAYER_SPEED
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_RIGHT)).convert_alpha()
			""" self.rot_speed = -PLAYER_ROT_SPEED """
		if keys[pg.K_UP] or keys[pg.K_w]:
			self.vel.y = -PLAYER_SPEED
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_UP)).convert_alpha()
			""" self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot) """
		if keys[pg.K_DOWN] or keys[pg.K_s]:
			self.vel.y = PLAYER_SPEED
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_DOWN)).convert_alpha()
		if self.vel.x < 0 and self.vel.y > 0:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_DOWN_L)).convert_alpha()
		if self.vel.x > 0 and self.vel.y > 0:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_DOWN_R)).convert_alpha()
		if self.vel.x > 0 and self.vel.y < 0:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_UP_R)).convert_alpha()
		if self.vel.x < 0 and self.vel.y < 0:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_UP_L)).convert_alpha()
		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= 0.7071
		""" self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot) """

	def collide_with_walls(self, dir):
		if dir == 'x':
			hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
			if hits:
				if self.vel.x > 0:
					self.pos.x = hits[0].rect.left - self.hit_rect.width
				if self.vel.x < 0:
					self.pos.x = hits[0].rect.right
				self.vel.x = 0
				self.hit_rect.x = self.pos.x
		if dir == 'y':
			hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
			if hits:
				if self.vel.y > 0:
					self.pos.y = hits[0].rect.top - self.hit_rect.height
				if self.vel.y < 0:
					self.pos.y = hits[0].rect.bottom
				self.vel.y = 0
				self.hit_rect.y = self.pos.y
	
	def update(self):
		self.get_keys()
		""" self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
		self.image = pg.transform.rotate(self.game.player_img, self.rot)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos """
		self.pos += self.vel * self.game.dt
		self.hit_rect.x = self.pos.x
		""" self.rect.centerx = self.pos.x """
		self.collide_with_walls('x')
		self.hit_rect.y = self.pos.y
		""" self.rect.centery = self.pos.y """
		self.collide_with_walls('y')
		self.rect.center = self.hit_rect.center
		self.rect.move_ip(0, -5)

class Wall(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE