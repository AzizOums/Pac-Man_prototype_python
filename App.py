import sys, pygame, time
from pygame.locals import *
from modele.pacman import Game
from modele.direction import up, down, left, right
from modele.map import size, scale
from modele.color import *

pygame.init()
clock = pygame.time.Clock()

key_to_dir = {
    K_RIGHT: right,
    K_LEFT: left,
    K_UP: up,
    K_DOWN: down
}

screen = pygame.display.set_mode(size)

imgs = {}

for name in ["Blinky", "Pinky", "Inky", "Clyde", "PacMan"]:
    for dir in [up, down, right, left]:
        imgs[(name, dir)] = pygame.transform.scale(pygame.image.load("./images/{}{}.png".format(name, dir)).convert_alpha(), (scale, scale))

imgs["BlueGhost"] = pygame.transform.scale(pygame.image.load("./images/BlueGhost.png").convert_alpha(), (scale, scale))
imgs["PacMan"] = pygame.transform.scale(pygame.image.load("./images/PacMan.png").convert_alpha(), (scale, scale))

game = Game()

tmp = 0
def draw_pacMan(pacMan):
    global tmp
    if tmp % 2:
        screen.blit(imgs[("PacMan", pacMan.dir)], pacMan.coord)
    else:
        tmp = 0
        screen.blit(imgs["PacMan"], pacMan.coord)
    tmp += 1

def draw_ghosts():
    global game
    for name in game.ghosts.keys():
        if game.ghosts[name].vulnerable:
            screen.blit(imgs["BlueGhost"], game.ghosts[name].coord)
        else:
            screen.blit(imgs[(name, game.ghosts[name].dir)], game.ghosts[name].coord)

while game.pacMan.alive:
    msElapsed = clock.tick(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == KEYDOWN and event.key in key_to_dir.keys():
            game.pacMan.change_dir(key_to_dir[event.key])

    game.maze.draw(screen)
    draw_pacMan(game.pacMan)
    draw_ghosts()
    game.step()
    pygame.display.update()

