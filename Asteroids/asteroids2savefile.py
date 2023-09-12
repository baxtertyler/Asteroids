import pygame
import random
import math

pygame.init()

screenX = 1000
screenY = 600
win = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Asteroids... 2!")
clock = pygame.time.Clock()
FPS = 60

class Ship(object):
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.angle = 0
		self.turnSpeed = 4
		self.speed = 3

		self.image = pygame.image.load('images/ship2.png')
		self.rotatedImage = pygame.transform.rotate(self.image, self.angle)

		self.w, self.h = self.image.get_size()
		self.box = []
		self.rotatedBox = []
		self.minBox = 0
		self.maxBox = 0
		self.origin = (self.x, self.y)

		self.image_rect = self.image.get_rect(topleft = (self.x - self.w/2, self.y - self.h/2))
		self.offset_center_to_pivot = pygame.math.Vector2((self.x, self.y)) - self.image_rect.center
		self.rotated_offset = self.offset_center_to_pivot.rotate(self.angle * -1)
		self.rotated_image_center = (self.x - self.rotated_offset.x, self.y - self.rotated_offset.y)
		self.rotated_image_rect = []


	def draw(self):
		self.box = [pygame.math.Vector2(p) for p in [(0,0),(self.w,0),(self.w,self.h * -1),(0,self.h * -1)]]
		self.rotatedBox = [p.rotate(self.angle) for p in self.box]
		self.minBox = (min(self.rotatedBox, key=lambda p: p[0])[0], min(self.rotatedBox, key=lambda p: p[1])[1])
		self.maxBox = (max(self.rotatedBox, key=lambda p: p[0])[0], max(self.rotatedBox, key=lambda p: p[1])[1])
		self.origin = (self.x + self.minBox[0], self.y - self.maxBox[1])

		self.image_rect = self.image.get_rect(topleft = (self.x - self.w/2, self.y - self.h/2))
		self.offset_center_to_pivot = pygame.math.Vector2((self.x, self.y)) - self.image_rect.center
		self.rotated_offset = self.offset_center_to_pivot.rotate(self.angle * -1)
		self.rotated_image_center = (self.x - self.rotated_offset.x, self.y - self.rotated_offset.y)

		self.rotatedImage = pygame.transform.rotate(ship.image, ship.angle)
		self.rotatedImageRect = self.rotatedImage.get_rect(center = self.rotated_image_center)
		win.blit(self.rotatedImage, self.rotatedImageRect)

class Bullet(object):

	def __init__(self, x, y, angle):
		self.x = x
		self.y = y
		self.angle = angle
		self.speed = 5

	def draw(self):
		pygame.draw.circle(win, (255,255,255), (self.x, self.y), 3)

class Asteroid(object):

	def __init__(self, shipX, shipY):
		self.x = 0
		self.y = random.randrange(0, screenY)
		self.shipX = shipX
		self.shipY = shipY
		self.dx = self.x - self.shipX
		self.dy = self.y - self.shipY
		self.dz = math.sqrt(self.dx**2 + self.dy**2)
		self.speed = random.randrange(1, 4)
		self.imageIndex = random.randrange(1, 4, 1)
		self.side = random.randrange(1, 4, 1)
		match self.imageIndex:
			case 1:
				self.image = pygame.image.load('images/asteroid1.png')
			case 2:
				self.image = pygame.image.load('images/asteroid2.png')
			case 3:
				self.image = pygame.image.load('images/asteroid3.png')
			case 4:
				self.image = pygame.image.load('images/asteroid4.png')
		self.hitbox = [self.x + 10, self.x + 60, self.y + 10, self.y + 60]

	def draw(self):
		win.blit(self.image, (self.x - 20, self.y))

def redraw():
	pygame.draw.rect(win, (0, 0, 0), (0, 0, screenX, screenY))
	for bullet in bullets:
		bullet.draw()
	for asteroid in asteroids:
		asteroid.draw()
	ship.draw()
	pygame.display.update()

run = True
ship = Ship(screenX / 2, screenY / 2)
bullets = []
asteroids = []
cooldown = 360
now = 0
last = 0
multiplier = 1

while(run):
	clock.tick(FPS)
	now = pygame.time.get_ticks()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	for bullet in bullets:
		bullet.x -= bullet.speed * math.cos((bullet.angle * math.pi / 180) - math.pi / 2)
		bullet.y += bullet.speed * math.sin((bullet.angle * math.pi / 180) - math.pi / 2)
		if bullet.x > screenX or bullet.x < 0 or bullet.y > screenY or bullet.y < 0:
			bullets.pop(bullets.index(bullet))
			multiplier += 0.2

	for asteroid in asteroids:
		asteroid.x -= multiplier * asteroid.speed * asteroid.dx/asteroid.dz
		asteroid.y -= multiplier * asteroid.speed * asteroid.dy/asteroid.dz
		for bullet in bullets:
			if bullet.x > asteroid.hitbox[0] and bullet.x < asteroid.hitbox[1] and bullet.y > asteroid[2] and bullet.y < asteroid[3]:
				asteroids.pop(asteroids.index(asteroid))

	if len(asteroids) < 5:
		asteroids.append(Asteroid(ship.x, ship.y))

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		ship.angle += ship.turnSpeed
	elif keys[pygame.K_RIGHT]:
		ship.angle -= ship.turnSpeed
	if keys[pygame.K_UP]:
		if ship.x < screenX - 25 and ship.x > 25:
			ship.x -= ship.speed * math.cos((ship.angle * math.pi / 180) - math.pi / 2)
		else:
			if ship.x < screenX / 2:
				ship.x += 1
			else:
				ship.x -= 1
		if ship.y < screenY - 25 and ship.y > 25:
			ship.y += ship.speed * math.sin((ship.angle * math.pi / 180) - math.pi / 2)
		else:
			if ship.y < screenY / 2:
				ship.y += 1
			else:
				ship.y -= 1
	if keys[pygame.K_SPACE] and now - last >= cooldown:
		bullets.append(Bullet(ship.rotated_image_center[0], ship.rotated_image_center[1], ship.angle))
		last = pygame.time.get_ticks()

	redraw()


pygame.quit
