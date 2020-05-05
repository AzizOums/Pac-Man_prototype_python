from modele import direction
from modele.map import Maze, size, scale
from random import choice
import pygame

class Perso():
	"""docstring for Perso"""
	def __init__(self, init_coord):
		self.dir = direction.right
		self.init_coord = init_coord
		self.coord = init_coord


	def respawn(self):
		self.dir = direction.right
		self.coord = self.init_coord

	def move(self):
		self.coord = direction.move_to(self.coord, self.dir)

	def change_dir(self, dir):
		self.dir = dir

	def get_rect(self, coord=None):
		if coord == None:
			x, y = self.coord
		else:
			x, y = coord
		
		return [x, y, scale, scale]


class PacMan(Perso):
	"""docstring for PacMan"""
	def __init__(self):
		super(PacMan, self).__init__((scale, scale))
		self.super = False
		self.alive = True
		self.lives = 3
		self.score = 0
		self.next_dir = None

	def add_score(self, score):
		self.score += score

	def respawn(self):
		super(PacMan, self).respawn()
		self.lives -= 1
		self.alive = (self.lives > 0)
		self.next_dir = None

	def change_dir(self, dir):
		self.next_dir = dir

	def move(self, maze):
		if self.next_dir != None and self.can_move_to(maze, self.next_dir):
			self.dir = self.next_dir
			self.next_dir = None

		if self.can_move_to(maze, self.dir):
			super(PacMan, self).move()

		self.adjust_coord()

	def can_move_to(self, maze, dir):
		coord = direction.move_to(self.coord, dir)
		rect = self.get_rect(coord)
		if maze.can_move(pacMan=rect):
			return True
		return False

	def adjust_coord(self):
		dx, dy = self.coord
		width, height = size
		if dx > width:
			dx = 0
		elif dx < 0:
			dx = width

		if dy > height:
			dy = 0
		elif dy < 0:
			dy = height

		self.coord = (dx, dy)


class Ghost(Perso):
	"""docstring for Ghost"""
	def __init__(self):
		super(Ghost, self).__init__((8 *scale, 11 *scale))
		self.vulnerable = False
		self.speed = 0

	def respawn(self):
		super(Ghost, self).respawn()
		self.vulnerable = False

	def change_dir(self):
		self.dir = choice([direction.up, direction.down, direction.left, direction.right])

	def die(self, game):
		if pygame.Rect(game.pacMan.get_rect()).colliderect(self.get_rect()):
			if game.pacMan.super and self.vulnerable:
				self.respawn()
			else:
				game.respawn()

	def move(self, maze):
		if (self.vulnerable and self.speed %2 == 0) or not self.vulnerable:
			self.speed = 0
			if self.can_move_to(maze, self.dir):
				super(Ghost, self).move()
			else:
				self.change_dir()
				self.move(maze)
		self.speed += 1

	def can_move_to(self, maze, dir):
		coord = direction.move_to(self.coord, dir)
		rect = self.get_rect(coord)
		if maze.can_move(ghost=rect):
			return True
		return False


class Game(object):
	"""docstring for Game"""
	def __init__(self):
		super(Game, self).__init__()
		self.maze = Maze()
		self.pacMan = PacMan()
		self.ghosts = {
			"Blinky": Ghost(),
			"Pinky": Ghost(),
			"Inky": Ghost(),
			"Clyde": Ghost()
		}
		self.timer = 0

	def step(self):
		self.pacMan.move(self.maze)
		for ghost in self.ghosts.values():
			ghost.move(self.maze)
			ghost.die(self)

		self.maze.actions(self)
		if self.timer >= 0:
			self.reduce_timer()

	def respawn(self):
		for ghost in self.ghosts.values():
			ghost.respawn()
		self.pacMan.respawn()

	def set_super_state(self):
		self.pacMan.super = True
		for ghost in self.ghosts.values():
			ghost.vulnerable = True
		self.timer = 300

	def reduce_timer(self):
		self.timer -= 1
		if self.timer <= 0:
			self.pacMan.super = False
			for ghost in self.ghosts.values():
				ghost.vulnerable = False