#! /usr/bin/python

#Import Modules
import os, pygame, random
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Define colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize pygame engine
pygame.init()

class spritesheet(object):
	def __init__(self, filename):
		try:
			self.sheet = pygame.image.load(filename).convert()
		except pygame.error, message:
			print 'Unable to load spritesheet image:', filename
			raise SystemExit, message
			
	# Load a specific image from a specific rectangle
	def image_at(self, rectangle, colorkey = None):
		"Loads image from x,y,x+offset,y+offset"
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size).convert()
		image.blit(self.sheet, (0, 0), rect)
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
				image.set_colorkey(colorkey, pygame.RLEACCEL)
				return image
	# Load a whole bunch of images and return them as a list
	def images_at(self, rects, colorkey = None):
		"Loads multiple images, supply a list of coordinates" 
		return [self.image_at(rect, colorkey) for rect in rects]
	# Load a whole strip of images
	def load_strip(self, rect, image_count, colorkey = None):
		"Loads a strip of images and returns them as a list"
		tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
		for x in range(image_count)]
		return self.images_at(tups, colorkey)

        
class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		ss = spritesheet('data/ship.png')
		self.image = ss.image_at((0, 132, 12, 16), -1)
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.y -= 9
		# check to see if it is off screen
		if self.rect.y <= 0:
			return 1

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite intializer
		ss = spritesheet('data/ship.png')
		self.image = ss.image_at((0, 132, 12, 16), -1)
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.y += 9
		# check to see if it is off screen
		if self.rect.y >= 800:
			return 1


class Ship(pygame.sprite.Sprite):
	"""moves a ship on the screen, following the mouse"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		ss = spritesheet('data/ship.png')
		self.image = ss.image_at((42, 0, 42, 42), -1)
		self.image = pygame.transform.scale(self.image, (52, 52))
		self.rect = self.image.get_rect()
		self.shooting = 0
		self.level = 0

	def update(self):
		pos = pygame.mouse.get_pos()
		self.rect.midtop = pos

	def shoot(self):
		self.shooting = 1
		newspawn = Bulletspawn(self.level, self)
		return newspawn

class Powerup(pygame.sprite.Sprite):
	"""Spawns a powerup sprite"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		ss = spritesheet('data/star.png')
		self.image = ss.image_at((0, 0, 14, 12), -1)
		self.image = pygame.transform.scale(self.image, (22, 20))
		self.rect = self.image.get_rect()
		self.sound = pygame.mixer.Sound('data/powup.wav')
		self.sound.set_volume(.1)

	def update(self):
		self.rect.y += 4
		if self.rect.y > 800:
			return 1

class Enemy(pygame.sprite.Sprite):
	"""moves a ship on the screen from top to bottom """
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		ss = spritesheet('data/enemies.png')
		randship = random.randint(0, 10)
		self.image = ss.image_at((0, (randship * 256), 256, 256), -1)
		self.image = pygame.transform.flip(self.image, 0, 1)
		self.image = pygame.transform.scale(self.image, (64, 64))
		self.rect = self.image.get_rect()
		self.count = 0

	def update(self):
		if self.count == 5:
			self.rect.y += random.randint(1, 5)
			self.rect.x += random.randint(-1, 1)
			self.count = 0
		else:
			self.rect.y += random.randint(1, 5)
		self.count += 1
		if self.rect.y > 800:
			return 1
		if self.rect.x > 1024 or self.rect.x < 0:
			return 1

def Bulletspawn(level, ship):
	newbullet = []
	for i in range(0, level+1):
		newbullet.append(Bullet())
	if level == 0:
		newbullet[0].rect.x = ship.rect.x + 10
		newbullet[0].rect.y = ship.rect.y + 8
	if level == 1:
		newbullet[0].rect.x = ship.rect.x
		newbullet[0].rect.y = ship.rect.y + 8
		newbullet[1].rect.x = ship.rect.x + 21
		newbullet[1].rect.y = ship.rect.y + 8
	elif level == 2:
		newbullet[0].rect.x = ship.rect.x
		newbullet[0].rect.y = ship.rect.y + 8
		newbullet[1].rect.x = ship.rect.x + 21
		newbullet[1].rect.y = ship.rect.y + 8
		newbullet[2].rect.x = ship.rect.x + 10
		newbullet[2].rect.y = ship.rect.y + 8
	elif level == 3:
		newbullet[0].rect.x = ship.rect.left - 5
		newbullet[0].rect.y = ship.rect.y + 8
		newbullet[1].rect.x = ship.rect.left + 5
		newbullet[1].rect.y = ship.rect.y + 8
		newbullet[2].rect.x = ship.rect.left + 16
		newbullet[2].rect.y = ship.rect.y + 8
		newbullet[3].rect.x = ship.rect.left + 26
		newbullet[3].rect.y = ship.rect.y + 8
	return newbullet
class Explosion(pygame.sprite.Sprite):
	anim = 4
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		ss = spritesheet('data/explosion.png')
		self.exp = []
		self.exp.append(ss.image_at((0, 0, 20, 37), -1))
		self.exp.append(ss.image_at((21, 0, 24, 36), -1))
		self.exp.append(ss.image_at((50, 0, 34, 36), -1))
		self.exp.append(ss.image_at((87, 0, 36, 36), -1))
		self.exp.append(ss.image_at((127, 0, 40, 38), -1))
		self.anim = 0
		self.image = self.exp[self.anim]
		self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.count = 0
		self.sound = pygame.mixer.Sound('data/Explosion3.wav')
		self.sound.set_volume(.05)


	def update(self):
		self.image = self.exp[self.anim]
		self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		if self.count == 7:
			self.anim += 1
			self.count = 0

		self.count += 1
		if self.anim == 4:
			return 1

def main():
	#Initialize Everything
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((1024, 800))

	#Create The Background
	background = pygame.image.load('data/space.jpg').convert()
	background_size = background.get_size()
	background_rect = background.get_rect()
	

	#Background scrolling
	w,h = background_size
	x = 0
	y = 0
	x1 = 0
	y1 = -h

	#Init Stuff
	pygame.display.set_caption('SpaceShooter!')
	pygame.mouse.set_visible(0)
	pygame.mixer.music.load('data/reso.mp3')
	pygame.mixer.music.play(-1)
	pygame.mixer.fadeout(2)
	#Prepare Game Objects
	clock = pygame.time.Clock()
	ship = Ship()
	allsprites = pygame.sprite.Group()
	bullet_list = pygame.sprite.Group()
	powerup_list = pygame.sprite.Group()
	enemy_list = pygame.sprite.Group()
	explosion_list = pygame.sprite.Group()

	allsprites.add(ship)
	pygame.key.set_repeat(50, 200)
	n = 200
	endgame = 0
	slowdown = 80

	score = 0
	font = pygame.font.Font(None, 36)
	#Main Loop
	while 1:
		screen.blit(background, background_rect)

		clock.tick(slowdown)

		ship.update()

		

		#Handle Input Events
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return
			elif event.type == KEYDOWN and event.key == K_SPACE and endgame == 0:
				newbullets = ship.shoot()
				for item in newbullets:
					bullet_list.add(item)

		for item in powerup_list:
			if ship.rect.colliderect(item.rect):
				powerup_list.remove(item)
				if ship.level <= 3:
					if n == 0 and ship.level != 3:
						n = 200
						ship.level += 1
						sound = pygame.mixer.Sound('data/lvl.wav')
						sound.set_volume(.1)
						sound.play()
					elif n == 0 and ship.level == 3:
						n = 0
						item.sound.play()
					else:
						n -= 20
						item.sound.play()
					pygame.key.set_repeat(50, n)
					

		if not endgame:
			for item in enemy_list:
				if ship.rect.colliderect(item.rect):
					newexp = Explosion(ship.rect.x, ship.rect.y)
					newexp2 = Explosion(item.rect.x, item.rect.y)
					newexp.sound.play()
					explosion_list.add(newexp)
					explosion_list.add(newexp2)
					allsprites.remove(ship)
					enemy_list.remove(item)
					endgame = 1
					pygame.mixer.music.load('data/slowdown.mp3')
					pygame.mixer.music.play()

		for item in enemy_list:
			for bul in bullet_list:
				if item.rect.colliderect(bul.rect):
					if random.randint(0, 20) == random.randint(0, 20):
						if ship.level != 3:
							newpowerup = Powerup()
							newpowerup.rect.x = item.rect.x
							newpowerup.rect.y = item.rect.y
							powerup_list.add(newpowerup)
						elif ship.level == 3 and n != 0:
							newpowerup = Powerup()
							newpowerup.rect.x = item.rect.x
							newpowerup.rect.y = item.rect.y
							powerup_list.add(newpowerup)
					newexp = Explosion(item.rect.x, item.rect.y)
					explosion_list.add(newexp)
					newexp.sound.play()
					enemy_list.remove(item)
					bullet_list.remove(bul)
					score += 5
					
					
		if random.randint(0, (30 / (ship.level+1))) == random.randint(0, (30 / (ship.level+1))):
			newenemy = Enemy()
			newenemy.rect.x = random.randint(20, 1000)
			newenemy.rect.y = 0
			enemy_list.add(newenemy)

		if random.randint(0, 1200) == random.randint(0, 1200):
			if ship.level != 3:
				newpowerup = Powerup()
				newpowerup.rect.x = random.randint(20, 1024)
				newpowerup.rect.y = random.randint(5, 150)
				powerup_list.add(newpowerup)
			elif ship.level == 3 and n != 0:
				newpowerup = Powerup()
				newpowerup.rect.x = random.randint(20, 1024)
				newpowerup.rect.y = random.randint(5, 150)
				powerup_list.add(newpowerup)

		y1 += 1
		y += 1

		allsprites.update()

		for item in bullet_list:
			if item.update() == 1:
				bullet_list.remove(item)
		for item in powerup_list:
			if item.update() == 1:
				powerup_list.remove(item)
		for item in enemy_list:
			if item.update() == 1:
				enemy_list.remove(item)
				score -= 10
		for item in explosion_list:
			if item.update() == 1:
				explosion_list.remove(item)

		if endgame:
			if slowdown <= 0:
				return
			else:
				slowdown -= .9

		#Draw Everything
		screen.blit(background, (x, y))
		screen.blit(background, (x1, y1))

		text = font.render("Score: " + str(score), 1, (WHITE))
		screen.blit(text, (0, 0))
		if y > h:
			y = -h
		if y1 > h:
			y1 = -h
			
		explosion_list.draw(screen)
		enemy_list.draw(screen)
		powerup_list.draw(screen)
		bullet_list.draw(screen)
		allsprites.draw(screen)
		pygame.display.flip()

	#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()