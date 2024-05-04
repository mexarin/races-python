import pygame
import random
import sys
import math
width = 1300
height = 1100
bg = (213,193,154,255)
dist=0
move=False
class Car:

	# list of available cars, take random everytime
	car_sprites = ( "Black_viper", "Orange", "Police", "Taxi")

	def __init__(self):
		self.random_sprite()

		self.angle = 0
		self.speed = 0
		self.k_rot = 0

		self.radars = []
		self.collision_points = []

		self.is_alive = True
		self.goal = False
		self.distance = 0
		self.time_spent = 0

	def random_sprite(self):
		self.car_sprite = pygame.image.load('sprites/' + random.choice(self.car_sprites) + '.png')
		self.car_sprite = pygame.transform.scale(self.car_sprite,
			(math.floor(self.car_sprite.get_size()[0]/3), math.floor(self.car_sprite.get_size()[1]/3)))
		self.car = self.car_sprite

		# recompute
		self.pos = [650, 955]
		self.compute_center()

	def compute_center(self):
		self.center = (self.pos[0] + (self.car.get_size()[0]/2), self.pos[1] + (self.car.get_size()[1] / 2))

	def draw(self, screen):
		screen.blit(self.car, self.pos)
		self.draw_radars(screen)

	def draw_center(self, screen):
		pygame.draw.circle(screen, (0,72,186), (math.floor(self.center[0]), math.floor(self.center[1])), 5)

	def draw_radars(self, screen):
		for r in self.radars:
			p, d = r
			pygame.draw.line(screen, (183,235,70), self.center, p, 1)
			pygame.draw.circle(screen, (183,235,70), p, 5)

	def compute_radars(self, degree, road):
		length = 0
		x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
		y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

		while not road.get_at((x, y)) == bg and length < 300:
			length = length + 1
			x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
			y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

		dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
		self.radars.append([(x, y), dist])

	def compute_collision_points(self):
		self.compute_center()
		lw = 0
		lh = 0

		lt = [self.center[0] + math.cos(math.radians(360 - (self.angle + 20))) * lw, self.center[1] + math.sin(math.radians(360 - (self.angle + 20))) * lh]
		rt = [self.center[0] + math.cos(math.radians(360 - (self.angle + 160))) * lw, self.center[1] + math.sin(math.radians(360 - (self.angle + 160))) * lh]
		lb = [self.center[0] + math.cos(math.radians(360 - (self.angle + 200))) * lw, self.center[1] + math.sin(math.radians(360 - (self.angle + 200))) * lh]
		rb = [self.center[0] + math.cos(math.radians(360 - (self.angle + 340))) * lw, self.center[1] + math.sin(math.radians(360 - (self.angle + 340))) * lh]

		self.collision_points = [lt, rt, lb, rb]



	def check_collision(self, road):
		self.is_alive = True

		for p in self.collision_points:
			try:
				if road.get_at((int(p[0]), int(p[1]))) == bg:
					self.is_alive = False
					break
			except IndexError:
				self.is_alive = False

	def rotate(self, angle):
		orig_rect = self.car_sprite.get_rect()
		rot_image = pygame.transform.rotate(self.car_sprite, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()

		self.car = rot_image

	def update(self, road):

		# rotate
		self.rotate(self.angle)
		self.k_rot=0

		# move
		self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
		if self.pos[0] < 20:
			self.pos[0] = 20
		elif self.pos[0] > width - 120:
			self.pos[0] = width - 120

		self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
		if self.pos[1] < 20:
			self.pos[1] = 20
		elif self.pos[1] > height - 120:
			self.pos[1] = height - 120

		# update distance & time spent
		if c.is_alive:
		 self.distance += self.speed
		self.time_spent += 1 # aka turns

		# compute/check collision points & create radars
		self.compute_collision_points()
		self.check_collision(road)

		self.radars.clear()
		for d in range(-90, 120, 45):
			self.compute_radars(d, road)
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
road = pygame.image.load('sprites/road.png')
pygame.key.set_repeat(100, 30)

font = pygame.font.SysFont("Roboto", 40)
heading_font = pygame.font.SysFont("Roboto", 80)
c = Car()
start = False
while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					start = True

				elif event.key == pygame.K_LEFT:
					c.angle += 7
				elif event.key == pygame.K_RIGHT:
					c.angle -= 7
				elif event.key == pygame.K_UP:
					move=True
				elif event.key == pygame.K_DOWN:
					move=False
				elif event.key == pygame.K_a:
					c.angle += 7
				elif event.key == pygame.K_d:
					c.angle -= 7
				elif event.key == pygame.K_w:
					move=True
				elif event.key == pygame.K_s:
					move=False

		if not start:
			continue
		screen.blit(road, (0, 0))
		label = heading_font.render("Проехал: " + str(int(c.distance/50)), True, (73,168,70))
		label_rect = label.get_rect()
		label_rect.center = (width / 1.5, 300)
		screen.blit(label, label_rect)
		c.update(road)
		c.radars=[]
		if move:
		 if c.is_alive:
	          c.speed=0.75
		 else:
			 c.speed =0.25
		else:
			c.speed=0
		c.compute_collision_points()
		c.draw(screen)
		pygame.display.flip()
		clock.tick(0)
