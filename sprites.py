from random import uniform
import pygame as pg
from settings import *
from tilemap import *
from os import path

vec = pg.math.Vector2

def image(self, game, rot):
		self.image = game.player_img
		game_folder = path.dirname(__file__)
		img_folder = path.join(game_folder, 'img')
		if rot == 0:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_RIGHT)).convert_alpha()
		if rot == 45:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_DOWN_R)).convert_alpha()
		if rot == 90:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_DOWN)).convert_alpha()
		if rot == 135:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_DOWN_L)).convert_alpha()
		if rot == 180:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_LEFT)).convert_alpha()
		if rot == 225:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_UP_L)).convert_alpha()
		if rot == 270:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_UP)).convert_alpha()
		if rot == 315:
			self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_UP_R)).convert_alpha()

def collide_with_walls(sprite, group, dir):
	if dir == 'x':
		hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			if hits[0].rect.centerx > sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width
			if hits[0].rect.centerx < sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.right
			sprite.vel.x = 0
			sprite.hit_rect.x = sprite.pos.x
	if dir == 'y':
		hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			if hits[0].rect.centery > sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height
			if hits[0].rect.centery < sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.bottom
			sprite.vel.y = 0
			sprite.hit_rect.y = sprite.pos.y

def collide_with_mobs(sprite, group, dir):
	if dir == 'x':
		hits = pg.sprite.spritecollide(sprite, group, False, collide_rect_not_self)
		if hits:
			if hits[0].rect.centerx > sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.left + 2
			if hits[0].rect.centerx < sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.right - sprite.hit_rect.width
			sprite.vel.x = 0
			sprite.hit_rect.x = sprite.pos.x
	if dir == 'y':
		hits = pg.sprite.spritecollide(sprite, group, False, collide_rect_not_self)
		if hits:
			if hits[0].rect.centery > sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.top
			if hits[0].rect.centery < sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.bottom - 18
			sprite.vel.y = 0
			sprite.hit_rect.y = sprite.pos.y

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
		self.pos = vec(x, y)
		self.rot = 0
		self.last_shot = 0
		self.last_time = 0
		self.health = PLAYER_HEALTH

	def	get_keys(self):
		self.vel = vec(0, 0)
		dir = 0
		keys = pg.key.get_pressed()
		time = pg.time.get_ticks()
		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.vel.x = -PLAYER_SPEED
			if time - self.last_time > FPS:
				self.rot = 180
				self.last_time = time
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.vel.x = PLAYER_SPEED
			if time - self.last_time > FPS:
				self.rot = 0
				self.last_time = time
		if keys[pg.K_UP] or keys[pg.K_w]:
			self.vel.y = -PLAYER_SPEED
			if time - self.last_time > FPS:
				self.rot = 270
				self.last_time = time
		if keys[pg.K_DOWN] or keys[pg.K_s]:
			self.vel.y = PLAYER_SPEED
			if time - self.last_time > FPS:
				self.rot = 90
				self.last_time = time
		if keys[pg.K_DOWN] and keys[pg.K_LEFT] or keys[pg.K_a] and keys[pg.K_s]:
			self.rot = 135
		if keys[pg.K_DOWN] and keys[pg.K_RIGHT] or keys[pg.K_d] and keys[pg.K_s]:
			self.rot = 45		
		if keys[pg.K_UP] and keys[pg.K_RIGHT] or keys[pg.K_d] and keys[pg.K_w]:
			self.rot = 315
		if keys[pg.K_UP] and keys[pg.K_LEFT] or keys[pg.K_a] and keys[pg.K_w]:
			self.rot = 225
		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= 0.7071
		if keys[pg.K_SPACE] or keys[pg.K_z]:
			now = pg.time.get_ticks()
			if now - self.last_shot > BULLET_RATE:
				self.last_shot = now
				dir = vec(1, 0).rotate(self.rot)
				pos = self.rect.center + BARREL_OFFSET.rotate(self.rot)
				if self.rot == 180:
					pos = pos + vec(0, 12)
				if self.rot == 0:
					pos = pos + vec(0, -2)
				if self.rot == 135:
					pos = pos + vec(12, 6)
				if self.rot == 225:
					pos = pos + vec(-9, 14)
				Bullet(self.game, pos, dir)
				self.vel = vec(-KICKBACK, 0).rotate(self.rot)

	def update(self):
		self.get_keys()
		self.pos += self.vel * self.game.dt
		self.hit_rect.x = self.pos.x
		collide_with_walls(self, self.game.walls, 'x')
		self.hit_rect.y = self.pos.y
		collide_with_walls(self, self.game.walls, 'y')
		self.rect.center = self.hit_rect.center
		self.rect.move_ip(0, -20)
		image(self, self.game, self.rot)

class Mob(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.mobs
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.mob_img
		self.rect = self.image.get_rect()
		self.hit_rect = MOB_HIT_RECT.copy()
		self.hit_rect.center = self.rect.center
		self.pos = vec(x, y)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.rot = 0
		self.health = MOB_HEALTH
	
	def update(self):
		game_folder = path.dirname(__file__)
		img_folder = path.join(game_folder, 'img')
		self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
		if self.rot > -135 and self.rot < -45:
			self.image = pg.image.load(path.join(img_folder, MOB_IMG_FRONT)).convert_alpha()
		if self.rot < 135 and self.rot > 45:
			self.image = pg.image.load(path.join(img_folder, MOB_IMG_BACK)).convert_alpha()
		if self.rot > 135 or self.rot < -135:
			self.image = pg.image.load(path.join(img_folder, MOB_IMG_LEFT)).convert_alpha()
		if self.rot < 45 and self.rot > -45:
			self.image = pg.image.load(path.join(img_folder, MOB_IMG_RIGHT)).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
		self.acc += self.vel * -1
		self.vel += self.acc * self.game.dt
		self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt **2
		self.hit_rect.x = self.pos.x
		collide_with_walls(self, self.game.walls, 'x')
		collide_with_mobs(self, self.game.mobs, 'x')
		self.hit_rect.y = self.pos.y
		collide_with_walls(self, self.game.walls, 'y')
		collide_with_mobs(self, self.game.mobs, 'y')
		self.rect.move_ip(10, -14)
		if self.health <= 0:
			self.kill()

	def draw_health(self):
		if self.health > 60:
			col = GREEN
		elif self.health > 30:
			col = YELLOW
		else:
			col = RED
		width = int(self.rect.width * self.health / MOB_HEALTH)
		self.health_bar = pg.Rect(0, 0, width, 7)
		if self.health < MOB_HEALTH:
			pg.draw.rect(self.image, col, self.health_bar)

class Bullet(pg.sprite.Sprite):
	def __init__(self, game, pos, dir):
		self.groups = game.all_sprites, game.bullets
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.bullet_img
		self.rect = self.image.get_rect()
		self.hit_rect = self.rect
		self.pos = vec(pos)
		self.rect.center = pos
		spread = uniform(-GUN_SPREAD, GUN_SPREAD)
		self.vel = dir.rotate(spread) * BULLET_SPEED
		self.spawn_time = pg.time.get_ticks()

	def update(self):
		self.pos += self.vel * self.game.dt
		self.rect.center = self.pos
		if pg.sprite.spritecollideany(self, self.game.walls):
			self.kill()
		if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
			self.kill()

""" class Wall(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.wall_img
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE """

class Obstacle(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		self.groups = game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.rect = pg.Rect(x, y, w, h)
		self.hit_rect = self.rect
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y


		
