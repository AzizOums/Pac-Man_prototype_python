import pygame
from modele.color import *

w = 7
v = 8
d = 9

level = [
	[w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w],
	[w,0,0,0,w,w,0,0,0,0,0,0,0,0,w,w],
	[w,0,w,0,w,w,0,w,w,w,w,w,w,0,w,w],
	[w,0,w,0,w,w,0,0,0,0,0,1,w,0,w,w],
	[w,0,w,0,w,w,w,w,w,1,w,0,w,0,w,w],
	[w,0,w,0,w,0,0,0,0,0,0,0,w,0,w,w],
	[w,1,w,0,w,w,w,w,w,w,w,w,w,0,w,w],
	[w,0,0,0,0,0,1,0,0,0,0,0,0,0,w,w],
	[w,w,w,0,w,w,d,d,d,w,w,0,w,w,w,w],
	[w,w,w,0,w,w,v,v,v,w,w,1,w,w,w,w],
	[v,v,v,0,w,w,v,v,v,w,w,0,v,v,v,v],
	[w,w,w,0,w,w,v,v,v,w,w,0,w,w,w,w],
	[w,w,w,0,w,w,w,w,w,w,w,0,w,w,w,w],
	[w,0,0,0,0,0,0,0,0,0,0,0,0,0,0,w],
	[w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w]
]

width = len(level[0])
height = len(level)

scale = 50
size = (width * (scale+1), height * (scale+1))

class MapObj():
	"""docstring for MapObj"""
	def __init__(self, rect, color):
		self.rect = rect
		self.color = color
		self.width = 2

	def can_pacMan_move(self):
		return False

	def action(self):
		return 0

class PacGom(MapObj):
	"""docstring for PacGom"""
	def __init__(self, rect, color, score):
		super(PacGom, self).__init__(rect, color)
		self.score = score
		self.width = 0

	def can_pacMan_move(self):
		return True

	def action(self):
		return self.score

def fill_maze(level):
	maze = []
	for x in range(0, len(level[0])):
		for y in range(0, len(level)):
			if level[y][x] == w:
				rect = pygame.Rect(x*scale, y*scale, scale, scale)
				color = blue
				maze.append(MapObj(rect, color))
			elif level[y][x] == d:
				rect = pygame.Rect(x*scale, y*scale, scale, scale)
				color = red
				maze.append(MapObj(rect, color))
			elif level[y][x] == 1:
				rect = pygame.Rect(x*scale + scale/3, y*scale + scale/3, scale/3, scale/3)
				color = orange
				score = 300
				maze.append(PacGom(rect, color, score))
			elif level[y][x] == 0:
				rect = pygame.Rect(x*scale + 3*scale/8, y*scale + 3*scale/8, scale/4, scale/4)
				color = yellow
				score = 100
				maze.append(PacGom(rect, color, score))
	return maze

class Maze():
	"""docstring for Maze"""
	def __init__(self):
		self.maze = fill_maze(level)

	def can_move(self, pacMan=None, ghost=None):
		if pacMan != None:
			for o in self.maze:
				if o.rect.colliderect(pygame.Rect(*pacMan)) and not o.can_pacMan_move():
					return False
			return True
		elif ghost != None:
			for o in self.maze:
				if o.rect.colliderect(pygame.Rect(*ghost)) and not o.can_pacMan_move() and o.color != red:
					return False
			return True

	def actions(self, game):
		for o in self.maze:
			if o.rect.colliderect(game.pacMan.get_rect()) and o.can_pacMan_move():
				game.pacMan.add_score(o.action())
				if(o.color == orange):
					game.set_super_state()
				self.maze.remove(o)

	def draw(self, screen):
		screen.fill(black)
		for o in self.maze:
			pygame.draw.rect(screen, o.color, o.rect, o.width)