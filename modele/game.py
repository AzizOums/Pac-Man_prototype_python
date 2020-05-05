from modele.map import Maze
from modele.perso import PacMan, Ghost

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