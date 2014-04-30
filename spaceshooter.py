#! /usr/bin/python

#Import Modules
import os, pygame, random, sys
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

class MenuItem (pygame.font.Font):
	'''
	The Menu Item should be derived from the pygame Font class
	'''
	def __init__(self,text, position,fontSize=36, antialias = 1, color = (255, 255, 255), background=None):
		pygame.font.Font.__init__(self,None, fontSize)
		self.text = text
		if background == None:
			self.textSurface = self.render(self.text,antialias,(255,255,255))
		else:
			self.textSurface = self.render(self.text,antialias,(255,255,255),background)
		self.position=self.textSurface.get_rect(centerx=position[0],centery=position[1])
	def get_pos(self):
		return self.position
	def get_text(self):
		return self.text
	def get_surface(self):
		return self.textSurface                

class Menu:
	'''
	The Menu should be initalized with a list of menu entries
	it then creates a menu accordingly and manages the different
	print Settings needed
	'''

	MENUCLICKEDEVENT = USEREVENT +1

	def __init__(self,menuEntries, menuCenter = None):
		'''
		The constructer uses a list of string for the menu entries,
		which need  to be created
		and a menu center if non is defined, the center of the screen is used
		'''
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.background = pygame.Surface(screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0))
		self.active=False

		if pygame.font:
			fontSize = 36
			fontSpace= 4
			# loads the standard font with a size of 36 pixels
			# font = pygame.font.Font(None, fontSize)

			# calculate the height and startpoint of the menu
			# leave a space between each menu entry
			menuHeight = (fontSize+fontSpace)*len(menuEntries)
			startY = self.background.get_height()/2 - menuHeight/2  

			#listOfTextPositions=list()
			self.menuEntries = list()
			for menuEntry in menuEntries:
				centerX=self.background.get_width()/2
				centerY = startY+fontSize+fontSpace
				newEnty = MenuItem(menuEntry,(centerX,centerY))
				self.menuEntries.append(newEnty)
				self.background.blit(newEnty.get_surface(), newEnty.get_pos())
				startY=startY+fontSize+fontSpace

	def drawMenu(self):
		self.active=True            
		screen = pygame.display.get_surface()
		screen.blit(self.background, (0, 0))

	def isActive(self):
		return self.active
	def activate(self,):
		self.active = True
	def deactivate(self):
		self.active = False
	def handleEvent(self, event):
		# only send the event if menu is active
		if event.type == MOUSEBUTTONDOWN and self.isActive():
			# initiate with menu Item 0
			curItem = 0
			# get x and y of the current event 
			eventX = event.pos[0]
			eventY = event.pos[1]
			# for each text position 
			for menuItem in self.menuEntries:
				textPos = menuItem.get_pos()
				# check if current event is in the text area 
				if eventX > textPos.left and eventX < textPos.right \
				and eventY > textPos.top and eventY < textPos.bottom:
					# if so fire new event, which states which menu item was clicked                        
					menuEvent = pygame.event.Event(self.MENUCLICKEDEVENT, item=curItem, text=menuItem.get_text())
					pygame.event.post(menuEvent)
				curItem = curItem + 1

def main():
	#Initialize Everything
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((1024, 800),  pygame.DOUBLEBUF | pygame.HWSURFACE )

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
	pygame.mouse.set_visible(1)
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


	# code for our menu 
	mainMenu = ("Start Game",
		"How to Play",
		"Quit")
	ingameMenu = ("Resume",
		"Restart",
		"Quit")
	isGameActive = False
	reset = False
	howtoplay = False
	myMenu = Menu(mainMenu)
	inMenu = Menu(ingameMenu)
	myMenu.drawMenu()
	#  pygame.display.flip()
	#Main Loop
	while 1:
		screen.blit(background, background_rect)

		clock.tick(slowdown)

		ship.update()

		

		#Handle Input Events
		for event in pygame.event.get():
			myMenu.handleEvent(event)
			inMenu.handleEvent(event)
			if event.type == QUIT:
				return

			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				pygame.mouse.set_visible(1)
				inMenu.activate()
				isGameActive = False

			elif event.type == Menu.MENUCLICKEDEVENT:
				if event.text=="Quit":
					return

				elif event.item == 0:
					isGameActive = True
					reset = False
					howtoplay = False
					myMenu.deactivate()
					inMenu.deactivate()

				elif event.item == 1 and myMenu.active:
					isGameActive = True
					howtoplay = True
					inMenu.deactivate()
					myMenu.deactivate()

				elif event.item == 1:
					isGameActive = True
					reset = True
					howtoplay = False
					inMenu.deactivate()
					myMenu.deactivate()

			elif event.type == KEYDOWN and event.key == K_SPACE and endgame == 0:
				newbullets = ship.shoot()
				for item in newbullets:
					bullet_list.add(item)

		if isGameActive:
			pygame.mouse.set_visible(0)
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
							slowdown += 10
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
				newenemy.rect.x = random.randint(20, 900)
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
				if slowdown == 3:
					slowdown = 80
					isGameActive = True
					reset = True
					endgame = False
				else:
					slowdown -= 1

			#Draw Everything
			screen.blit(background, (x, y))
			screen.blit(background, (x1, y1))

			if howtoplay:
				text = font.render("Use the mouse to move, and the spacebar to shoot!", 1, (WHITE))
				screen.blit(text, (100, 50))
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
			if not endgame:
				allsprites.draw(screen)

		if myMenu.isActive():
			myMenu.drawMenu()

		if inMenu.isActive():
			inMenu.drawMenu()

		if reset:
			explosion_list.empty()
			enemy_list.empty()
			powerup_list.empty()
			bullet_list.empty()
			reset = False
			pygame.mixer.music.load('data/reso.mp3')
			pygame.mixer.music.play(-1)
			score = 0
			ship.level = 0

		pygame.display.flip()

	#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()