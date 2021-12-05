from random import uniform, choice, random
import pygame as pg
from settings import *
from tilemap import *
import pytweening as tween
from itertools import chain

vec = pg.math.Vector2

def image(self, rot, fire):
		image = 0
		if rot == 0:
			image = 0
		if rot == 45:
			image = 2
		if rot == 90:
			image = 4
		if rot == 135:
			image = 6
		if rot == 180:
			image = 8
		if rot == 225:
			image = 10
		if rot == 270:
			image = 12
		if rot == 315:
			image = 14
		if fire:
			image += 1
		self.image = self.game.player_img[image].copy()
		return False

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

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = PLAYER_LAYER
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.player_img[0]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.hit_rect = PLAYER_HIT_RECT
		self.hit_rect.center = self.rect.center
		self.vel = vec(0, 0)
		self.pos = vec(x, y)
		self.rot = 0
		self.fire = False
		self.last_shot = 0
		self.last_time = 0
		self.boost_time = 0
		self.health = PLAYER_HEALTH
		self.speed = PLAYER_SPEED
		self.weapon = 'pistol'
		self.damage = False
		self.ammo = 0

	def	get_keys(self):
		self.vel = vec(0, 0)
		keys = pg.key.get_pressed()
		time = pg.time.get_ticks()
		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.vel.x = -self.speed
			if time - self.last_time > FPS:
				self.rot = 180
				self.last_time = time
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.vel.x = self.speed
			if time - self.last_time > FPS:
				self.rot = 0
				self.last_time = time
		if keys[pg.K_UP] or keys[pg.K_w]:
			self.vel.y = -self.speed
			if time - self.last_time > FPS:
				self.rot = 270
				self.last_time = time
		if keys[pg.K_DOWN] or keys[pg.K_s]:
			self.vel.y = self.speed
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
	#part for shooting
		if keys[pg.K_SPACE] or keys[pg.K_z]:
			self.shoot()

	def shoot(self):
		now = pg.time.get_ticks()
		if now - self.last_shot > WEAPONS[self.weapon]['rate']:
			self.fire = True
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
			self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(self.rot)
			for i in range(WEAPONS[self.weapon]['bullet_count']):
				spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
				Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'], WEAPONS[self.weapon]['bullet_lifetime'])
				snd = choice(self.game.weapon_sounds[self.weapon])
				if snd.get_num_channels() > 2:
					snd.stop()
				snd.play()
			if self.weapon == 'shotgun':
				self.ammo -= 1

	def hit(self):
		self.damage = True
		self.damage_alpha = chain(DAMAGE_ALPHA * 4)

	def update(self):
		self.get_keys()
		self.pos += self.vel * self.game.dt
		self.hit_rect.x = self.pos.x
		collide_with_walls(self, self.game.walls, 'x')
		self.hit_rect.y = self.pos.y
		collide_with_walls(self, self.game.walls, 'y')
		self.rect.center = self.hit_rect.center
		self.rect.move_ip(0, -20)
		self.fire = image(self, self.rot, self.fire)
		if self.damage :
			try:
				self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
			except:
				self.damage = False
		time = pg.time.get_ticks()
		if time - self.boost_time > BOOST_TIME * 1000:
			self.speed = PLAYER_SPEED
		if self.ammo == 0:
			self.weapon = 'pistol'

	def add_health(self):
		self.health += HEALTH_PACK_AMOUNT
		if self.health > PLAYER_HEALTH:
			self.health = PLAYER_HEALTH
	
	def speed_boost(self):
		self.speed = PLAYER_SPEED * 2
		self.boost_time = pg.time.get_ticks()
	
	def	shotgun(self):
		self.weapon = 'shotgun'
		self.ammo = 10


class Mob(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = MOB_LAYER
		self.groups = game.all_sprites, game.mobs
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.mob_img[0].copy()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.rect.move_ip(10, -14)
		self.hit_rect = MOB_HIT_RECT.copy()
		self.hit_rect.center = self.rect.center
		self.hit_rect.move_ip(0, 24)
		self.pos = vec(x, y)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.rot = 0
		self.health = MOB_HEALTH
		self.target = game.player
		self.saved_image = self.image
	
	def avoid_mobs(self):
		for mob in self.game.mobs:
			if mob != self:
				dist = self.pos - mob.pos
				if 0 < dist.length() < AVOID_RADIUS:
					self.acc += dist.normalize()

	def update(self):
		target_dist = self.target.pos - self.pos
		self.image = self.saved_image.copy()
		if target_dist.length_squared() < DETECT_RADIUS**2 or self.health < MOB_HEALTH:
			if random() < 0.005:
				choice(self.game.zombie_moan_sounds).play()
			self.rot = target_dist.angle_to(vec(1, 0))
			if self.rot > -135 and self.rot < -45:
				self.image = self.game.mob_img[0].copy()
			if self.rot < 135 and self.rot > 45:
				self.image = self.game.mob_img[1].copy()
			if self.rot > 135 or self.rot < -135:
				self.image = self.game.mob_img[3].copy()
			if self.rot < 45 and self.rot > -45:
				self.image = self.game.mob_img[2].copy()
			self.rect = self.image.get_rect()
			self.rect.center = self.pos
			self.acc = vec(1, 0).rotate(-self.rot)
			self.avoid_mobs()
			if self.acc != 0:
				self.acc.scale_to_length(MOB_SPEED)
			self.acc += self.vel * -1
			self.vel += self.acc * self.game.dt
			self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt **2
			self.hit_rect.x = self.pos.x
			collide_with_walls(self, self.game.walls, 'x')
			self.hit_rect.y = self.pos.y
			collide_with_walls(self, self.game.walls, 'y')
			self.rect.move_ip(10, -14)
			self.saved_image = self.image.copy()
		if self.health <= 0:
			choice(self.game.zombie_hit_sounds).play()
			self.kill()
			self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))

	def draw_health(self):
		for mob in self.game.mobs:
			if mob.health > 60:
				col = GREEN
			elif mob.health > 30:
				col = YELLOW
			else:
				col = RED
			width = int(mob.rect.width * mob.health / MOB_HEALTH)
			mob.health_bar = pg.Rect(0, 0, width, 7)
			if mob.health < MOB_HEALTH:
				pg.draw.rect(mob.image, col, mob.health_bar)

class Bullet(pg.sprite.Sprite):
	def __init__(self, game, pos, dir, damage, lifetime):
		self._layer = BULLET_LAYER
		self.groups = game.all_sprites, game.bullets
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
		self.rect = self.image.get_rect()
		self.hit_rect = self.rect.copy()
		self.pos = vec(pos)
		self.rect.center = pos
		self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
		self.spawn_time = pg.time.get_ticks()
		self.damage = damage
		self.bullet_lifetime = lifetime

	def update(self):
		self.pos += self.vel * self.game.dt
		self.hit_rect.x = self.pos.x
		self.hit_rect.y = self.pos.y
		self.rect.center = self.hit_rect.center
		self.hit_rect.move_ip(0, 15)
		if pg.sprite.spritecollideany(self, self.game.walls):
			self.kill()
		if pg.time.get_ticks() - self.spawn_time > self.bullet_lifetime :
			self.kill()

class Obstacle(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		self._layer = WALL_LAYER
		self.groups = game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.rect = pg.Rect(x, y, w, h)
		self.hit_rect = self.rect
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y

class Tree(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, type):
		self._layer = TREE_LAYER
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.rect = pg.Rect(x, y, w, h)
		self.x = x
		self.y = y
		self.rect.x = x - 15
		self.rect.y = y - 15
		if type == "green":
			self.image = game.tree_img[0]
		elif type == "red":
			self.rect.y = y - 18
			self.image = game.tree_img[1]
		self.hit_rect = self.rect.copy()
		self.hit_rect.move_ip(15, 20)

class Item(pg.sprite.Sprite):
	def __init__(self, game, pos, type):
		self._layer = ITEM_LAYER
		self.groups = game.all_sprites, game.items
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.item_images[type]
		self.rect = self.image.get_rect()
		self.type = type
		self.hit_rect = self.rect
		self.pos = pos
		self.rect.center = pos
		self.tween = tween.easeInOutSine
		self.step = 0
		self.dir = 1

	def update(self):
		#bobbing motion
		offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
		self.rect.centery = self.pos.y + offset * self.dir
		self.step += BOB_SPEED
		if self.step > BOB_RANGE:
			self.step = 0
			self.dir *= -1