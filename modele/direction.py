directions = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0)
}

up = "Up"
down = "Down"
left = "Left"
right = "Right"

def move_to(coord, dir):
	x, y = coord
	dx, dy = directions[dir]
	return (x + dx, y + dy)