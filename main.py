#basic game loop structure

import pygame as pg
import sys
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
		pg.mixer.pre_init(44100, -16, 1, 2048)
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		pg.key.set_repeat(20, 70)
		self.load_data()

	def draw_text(self, text, font_name, size, color, x, y, align="nw"):
		font = pg.font.Font(font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		if align == "nw":
			text_rect.topleft = (x, y)
		if align == "ne":
			text_rect.topright = (x, y)
		if align == "sw":
			text_rect.bottomleft = (x, y)
		if align == "se":
			text_rect.bottomright = (x, y)
		if align == "n":
			text_rect.midtop = (x, y)
		if align == "s":
			text_rect.midbottom = (x, y)
		if align == "e":
			text_rect.midright = (x, y)
		if align == "w":
			text_rect.midleft = (x, y)
		if align == "center":
			text_rect.center = (int(x), int(y))
		self.screen.blit(text_surface, text_rect)

	def	load_data(self):
		game_folder = path.dirname(__file__)
		img_folder = path.join(game_folder, 'img')
		snd_folder = path.join(game_folder, 'snd')
		music_folder = path.join(game_folder, 'music')
		self.map_folder = path.join(game_folder, 'maps')
		self.title_font = path.join(img_folder, 'Font/RioGrande.ttf')
		self.hud_font = path.join(img_folder, 'Font/Cowboys.ttf')
		self.text_font = path.join(img_folder, 'Font/OldTownRegular.ttf')
		self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
		self.dim_screen.fill((0, 0, 0, 180))
		self.player_img = []
		self.mob_img = []
		for img in PLAYER_IMG:
			self.player_img.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
		for img in MOB_IMG:
			self.mob_img.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
		self.bullet_images = {}
		self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
		self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (5, 5))
		self.tree_img = []
		for img in TREE_IMG:
			self.tree_img.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
		self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
		self.splat = pg.transform.scale(self.splat, (64, 64))
		self.item_images = {}
		for item in ITEM_IMAGES:
			self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
		#Sound loading
		pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
		pg.mixer.music.set_volume(0.2)
		self.effects_sounds = {}
		for type in EFFECTS_SOUNDS :
			s = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
			s.set_volume(0.2)
			self.effects_sounds[type] = s
		self.weapon_sounds = {}
		for weapon in WEAPON_SOUNDS:
			self.weapon_sounds[weapon] = []
			for snd in WEAPON_SOUNDS[weapon]:
				s = pg.mixer.Sound(path.join(snd_folder, snd))
				s.set_volume(0.05)
				self.weapon_sounds[weapon].append(s)
		self.zombie_moan_sounds = []
		for snd in ZOMBIE_MOAN_SOUNDS:
			s = pg.mixer.Sound(path.join(snd_folder, snd))
			s.set_volume(0.15)
			self.zombie_moan_sounds.append(s)
		self.player_hit_sounds = []
		for snd in PLAYER_HIT_SOUNDS:
			self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
		self.zombie_hit_sounds = []
		for snd in ZOMBIE_HIT_SOUNDS:
			s = pg.mixer.Sound(path.join(snd_folder, snd))
			s.set_volume(0.3)
			self.zombie_hit_sounds.append(s)

	def	new(self):
		#sert a initié les variables pour un nouveau jeu
		self.all_sprites = pg.sprite.LayeredUpdates()
		self.walls = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.bullets = pg.sprite.Group()
		self.items = pg.sprite.Group()
		self.map = TiledMap(path.join(self.map_folder, 'home.tmx'))
		self.map_img = self.map.make_map()
		self.map_rect = self.map_img.get_rect()
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
			if tile_object.name in ['health', 'speed', 'shotgun']:
				Item(self, obj_center, tile_object.name)
		self.camera = Camera(self.map.width, self.map.height)
		self.draw_debug = False
		self.paused = False
		self.effects_sounds['level_start'].play()

	def run(self):
		self.playing = True
		pg.mixer.music.play(loops=-1)
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			if not self.paused:
				self.update()
			self.draw()

	def	quit(self):
		pg.display.quit()
		pg.quit()
		sys.exit()

	def update(self):
		#update portion of the game loop
		self.all_sprites.update()
		self.camera.update(self.player)
		#game over condition
		if len(self.mobs) == 0:
			self.show_win_screen()
			self.playing = False
		#player hit items
		hits = pg.sprite.spritecollide(self.player, self.items, False, collide_hit_rect)
		for hit in hits:
			if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
				hit.kill()
				self.effects_sounds['health_up'].play()
				self.player.add_health()
			if hit.type == 'speed':
				hit.kill()
				self.effects_sounds['eating'].play()
				self.player.speed_boost()
			if hit.type == 'shotgun':
				hit.kill()
				self.effects_sounds['shotgun'].play()
				self.player.weapon = 'shotgun'
		#mobs hit player
		hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
		for hit in hits:
			snd = choice(self.player_hit_sounds)
			if snd.get_num_channels() > 2:
				snd.stop()
			snd.play()
			self.player.health -= MOB_DAMAGE
			hit.vel = vec(0,0)
			if self.player.health <= 0:
				self.show_go_screen()
				self.playing = False
		if hits:
			self.player.hit()
			self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
		#bullet hit mobs
		hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True, collide_hit_rect)
		for mob in hits:
			for bullet in hits[mob]:
				mob.health -= bullet.damage
			mob.vel = vec(0,0)
	
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
			if self.player.hit_rect.y < sprite_mob.hit_rect.y:
				self.all_sprites.change_layer(sprite_mob, 4)
			else:
				self.all_sprites.change_layer(sprite_mob, 2)
		if self.draw_debug:
			for wall in self.walls:
				pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
		#HUD functions
		draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
		self.draw_text('Los Cactus: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE, WIDTH - 10, 10, align="ne")
		if self.paused:
			self.screen.blit(self.dim_screen, (0, 0))
			self.draw_text("(Paused)", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
		pg.display.flip()

	def events(self):
		#sert a maper les events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_h:
					self.draw_debug = not self.draw_debug
				if event.key == pg.K_p:
					self.paused = not self.paused
		keys = pg.key.get_pressed()
		if keys[pg.K_ESCAPE]:
			self.quit()
	
	def show_start_screen(self):
		self.screen.fill(WHITE)
		self.draw_text("(El cazador de cactus)", self.title_font, 100, RED, WIDTH / 2, HEIGHT * 4 / 10, align="center")
		self.draw_text("Made by GabCollet", self.title_font, 20, BLACK, WIDTH / 2, HEIGHT * 4 / 10 + 50, align="center")
		self.draw_text("Press ENTER to start", self.title_font, 50, BLACK, WIDTH / 2, HEIGHT * 6 / 10, align="center")
		instruction_rect = pg.Rect(10, HEIGHT - 260, 250, 250)
		pg.draw.rect(self.screen, (230, 230, 230), instruction_rect)
		self.draw_text("Instructions :", self.text_font, 40, BLACK, 65, HEIGHT -250, align="nw")
		self.draw_text("Move ------------------------ Arrows Keys", self.text_font, 25, BLACK, 20, HEIGHT -200, align="nw")
		self.draw_text("or", self.text_font, 25, BLACK, 200, HEIGHT -180, align="nw")
		self.draw_text("WASD", self.text_font, 25, BLACK, 190, HEIGHT -160, align="nw")
		self.draw_text("Shoot ---------------------- Spacebar or Z", self.text_font, 25, BLACK, 20, HEIGHT -130, align="nw")
		self.draw_text("Pause ------------------------------------------ P", self.text_font, 25, BLACK, 20, HEIGHT -110, align="nw")
		self.draw_text("Show Hit-Box ------------------------------ H", self.text_font, 25, BLACK, 20, HEIGHT -90, align="nw")
		self.draw_text("Quit ------------------------------------------ esc", self.text_font, 25, BLACK, 20, HEIGHT -70, align="nw")
		pg.display.flip()
		self.wait_for_key()

	def show_go_screen(self):
		self.screen.fill(BLACK)
		pg.mixer.music.stop()
		self.draw_text("(GAME OVER)", self.title_font, 200, RED, WIDTH / 2, HEIGHT / 2, align="center")
		self.draw_text("Press ENTER to restart", self.title_font, 50, WHITE, WIDTH / 2, HEIGHT * 6 / 10, align="center")
		pg.display.flip()
		self.wait_for_key()
	
	def show_win_screen(self):
		self.screen.fill(BLACK)
		pg.mixer.music.stop()
		self.draw_text("(Felicidades!)", self.title_font, 200, RED, WIDTH / 2, HEIGHT / 2, align="center")
		self.draw_text("Press ENTER to restart", self.title_font, 50, WHITE, WIDTH / 2, HEIGHT * 6 / 10, align="center")
		pg.display.flip()
		self.wait_for_key()

	def wait_for_key(self):
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.quit()
				if event.type == pg.KEYDOWN :
					if event.key == pg.K_ESCAPE:
						self.quit()
					if event.key == pg.K_RETURN:
						pg.event.clear()
						waiting = False

g = Game()
g.show_start_screen()
while True:
	g.new()
	g.run()
