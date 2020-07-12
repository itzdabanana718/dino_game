#TODO, make cactus not appear next to eachother, make scoreboard
import sys
import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite
import time
import random
global screen
from threading import Timer
import math
#import pyautogui
#multiply time by this to get score
speed = 3
score = 0
Cacti = Group()
ducking = False
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Dino Game")
pygame.init()
inair = False
def run_game():
	dead = False
	while not dead:
		#determine_score(speed)
		update_screen(dino, screen, Cacti)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event, screen, dino, Cacti)
		
			elif event.type == pygame.KEYUP:
				check_keyup_events(event)
		dead = check_collisions(dino, Cacti)
		if determine_cactus():
			cactus = Cactus(screen)
			Cacti.add(cactus)
		
	
	
def update_screen(dino, screen, cacti):
	screen.fill((50,25,25))
	pygame.draw.rect(screen,(0,255,0),[0,300,1000,500])
	dino.blitme()
	dino.update()
	for cactus in cacti:
		cactus.blitme()
	move_cactus(Cacti)
	pygame.display.flip()
	
class Cactus(Sprite): 
	def __init__(self, screen):
		super(Cactus, self).__init__()
		self.screen = screen
		self.image = pygame.image.load('2cactus.png')
		self.rect = self.image.get_rect()
		
		self.rect.bottom = 300
		self.rect.left = 1000
	def blitme(self):
		self.screen.blit(self.image, self.rect)

def determine_score(speed):
	font = pygame.font.SysFont(None, 48)
	global score
	score += 0.01 * speed
	score_str = int(round(score, 0))
	score_image = font.render(score_str, True, (250, 0, 0), (245, 245, 245))
	
	score_rect = score_image.get_rect()
	score_rect.right = 990
	score_rect.top = 20
	screen.blit(score_image, score_rect)



def fall():
	global dino
	global inair
	if inair:	
		dino.rect.bottom += 50
		inair = False
	#print("falling")

def jump(dino, screen, cactus):
	global inair
	#print("please")
	if not inair:
		dino.rect.bottom -= 50
		t = Timer(0.75, fall)
		t.start()
		inair = True


class Dino(Sprite):
	def __init__(self, screen):
		super(Dino, self).__init__()
		self.screen = screen
		self.images = []
		run1 = pygame.image.load("running1.png")
		run2 = pygame.image.load("running2.png")
		run1 = pygame.transform.scale(run1, (10,10))
		self.images.append(pygame.image.load("running1.png"))
		self.images.append(pygame.image.load("running2.png"))
		self.index = 0
		self.image = self.images[self.index]
		
		self.rect = self.image.get_rect()
		
		self.rect.bottom = 300
		self.rect.left = 30
	def update(self):
		self.index += 1
		
		if self.index >= len(self.images):
			self.index = 0
			
		self.image = self.images[self.index]

	def blitme(self):
		self.screen.blit(self.image, self.rect)
		
def check_collisions(Dino, cacti):
	for cactus in cacti:
		if pygame.sprite.collide_rect(Dino, cactus):
			return True

def duck():
	dino.image = pygame.image.load('duck.png')

def destroy_cactus(Cacti):
	for cactus in Cacti:
		if cactus.rect.right <= 0:
			Cacti.remove(cactus)

def determine_cactus():
	"""a function to determine if a cactus should be placed"""
	x = random.randint(1,700)
	if x == 1:
		return True
	else:
		return False

def move_cactus(cacti):
	for cactus in cacti:
		cactus.rect.right -= speed
		destroy_cactus(cacti)

	
def check_keydown_events(event, screen, dino, cactus):
	global inair, ducking
	#print(event)
	if event.key == pygame.K_UP and not inair and not ducking:
		jump(dino, screen, cactus)
	elif event.key == pygame.K_q or pygame.QUIT:
		sys.exit()
	elif event.key == 274:
		duck()

def check_keyup_events(event):
	if event.key == pygame.K_UP:
		t = Timer(0.5, fall())
	elif event.key == pygame.K_q or pygame.QUIT:
		sys.exit()
dino = Dino(screen)


	

run_game()

