import pygame
import random
pygame.init()

screenSize = 600

# game window
win = pygame.display.set_mode((screenSize, screenSize))

# window title
pygame.display.set_caption("Asteroids!")

# load in ship images
shipImage = pygame.image.load('images/ship.png')
rockImage = pygame.image.load('images/rock.png')

# ship class
class Ship(object):
	# init method
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.moving = False
		self.velocity = 5

	def draw(self, win):
		win.blit(shipImage, (self.x - 25, self.y - 25))

	def hit(self):
		print('hit')
		score = 0
		self.x = 275
		self.y = 275
		font1 = pygame.font.SysFont('comicsans', 100)
		text = font1.render('GAME OVER', 1, (255, 0, 0))
		win.blit(text, (5, 200))
		pygame.display.update()
		for rock in rocks:
			rocks.pop(rocks.index(rock))
		i = 0
		while i < 200:
			pygame.time.delay(10)
			i += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				i = 301
				pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, color, direction) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = 8
        self.direction = direction

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Rock(object):
	def __init__(self, x, y, velocity, direction):
		self.x = x
		self.y = y
		self.velocity = velocity
		self.direction = direction

	def draw(self, win):
		win.blit(rockImage, (self.x, self.y))

def redrawGameWindow():
	pygame.draw.rect(win, (0, 0, 0), (0, 0, screenSize, screenSize))
	ship.draw(win)
	for bullet in bullets:
		bullet.draw(win)
	for rock in rocks:
		rock.draw(win)
	text = pygame.font.SysFont('comicsans', 30, True).render('Score: ' + str(score), 1, (255, 255, 255))
	win.blit(text, (10, 10))
	pygame.display.update()

# create objects
ship = Ship(300, 300)

bullets = []
rocks = []
score = 0
# main loop
run  = True
while run:
	# loops through events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	for bullet in bullets:
		if bullet.x < 0 or bullet.x > 600 or bullet.y < 0 or bullet.y > 600:
			bullets.pop(bullets.index(bullet))
		if bullet.direction == 'up':
			bullet.y -= bullet.velocity
		if bullet.direction == 'down':
			bullet.y += bullet.velocity
		if bullet.direction == 'left':
			bullet.x -= bullet.velocity
		if bullet.direction == 'right':
			bullet.x += bullet.velocity
		for rock in rocks:
			if bullet.x > rock.x + 20 and bullet.x < rock.x + 80 and bullet.y > rock.y + 20 and bullet.y < rock.y + 80:
				rocks.pop(rocks.index(rock))
				bullets.pop(bullets.index(bullet))
				score += 1

	for rock in rocks:
		if rock.x < -100 or rock.x > 700 or rock.y < -100 or rock.y > 700:
			rocks.pop(rocks.index(rock))
		if rock.direction == 'up' or rock.direction == 'down':
			rock.y += rock.velocity
		if rock.direction == 'left' or rock.direction == 'right':
			rock.x += rock.velocity
		rockL = rock.x
		rockR = rock.x + 100
		rockT = rock.y
		rockB = rock.y + 100
		shipL = ship.x
		shipR = ship.x + 45
		shipT = ship.y
		shipB = ship.y + 45
		if shipL > rockL and shipR < rockR and shipT > rockT and shipB < rockB:
			ship.hit()
			score = 0

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] and ship.x > 50:
		ship.x -= ship.velocity
	if keys[pygame.K_RIGHT] and ship.x < 550:
		ship.x += ship.velocity
	if keys[pygame.K_UP] and ship.y > 50: 
		ship.y -= ship.velocity
	if keys[pygame.K_DOWN] and ship.y < 550:
		ship.y += ship.velocity

	if keys[pygame.K_SPACE] and len(bullets) < 4:
		bullets.append(projectile(ship.x - 2.5, ship.y + 30, 5, (255,255,255), 'down'))
		bullets.append(projectile(ship.x - 2.5, ship.y - 30, 5, (255,255,255), 'up'))
		bullets.append(projectile(ship.x - 30, ship.y - 2.5, 5, (255,255,255), 'left'))
		bullets.append(projectile(ship.x + 22.5, ship.y - 2.5, 5, (255,255,255), 'right'))

	if len(rocks) < 4:
		num = random.randrange(100)
		if num < 25: #up
			rocks.append(Rock(random.randrange(600), 600, random.randrange(-5, -3, 1), 'up'))
		elif num < 50: #down
			rocks.append(Rock(random.randrange(600), 0, random.randrange(3, 5, 1), 'down'))
		elif num < 75: #left
			rocks.append(Rock(600, random.randrange(600), random.randrange(-5, -3, 1), 'left'))
		elif num < 100:
			rocks.append(Rock(0, random.randrange(600), random.randrange(3, 5, 1), 'right'))

	# call method that draws
	redrawGameWindow()

pygame.quit