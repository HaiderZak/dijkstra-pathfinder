import pygame
import math
from queue import PriorityQueue

WIDTH = 800
numRows = 50
blockSize = WIDTH // numRows
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0,0,255)
PURPLE = (128, 0, 128)
TURQUOISE = (64, 224, 208)
ORANGE = (255, 165 ,0)
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra Path Finding Algorithm")

class Node:
	def __init__(self, color, row, col):
		self.color = color
		self.row = row
		self.col = col
		self.neighbors = []
	def getColor(self):
		return self.color
	def setColor(self, newColor):
		self.color = newColor
	def draw(self):
		pygame.draw.rect(WIN, self.color, (self.row * blockSize, self.col * blockSize, blockSize, blockSize))
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < numRows - 1 and not grid[self.row + 1][self.col] == BLACK:
			self.neighbors.append(grid[self.row + 1][self.col])
		if self.row > 0 and not grid[self.row - 1][self.col] == BLACK:
			self.neighbors.append(grid[self.row - 1][self.col])
		if self.col < numRows - 1 and not grid[self.row][self.col + 1] == BLACK:
			self.neighbors.append(grid[self.row][self.col + 1])
		if self.col > 0 and not grid[self.row][self.col - 1] == BLACK:
			self.neighbors.append(grid[self.row][self.col - 1])

def nodesIntoGrid(numRows, width):
	grid = []
	for i in range(numRows):
		grid.append([])
		for j in range(numRows):
			node = Node(WHITE, i, j)
			grid[i].append(node)
	return grid

def drawGrid(numRows, width, gap):
	for i in range(numRows):
		pygame.draw.line(WIN, GREY, (0, i * gap), (width, i * gap))
		for j in range(numRows):
			pygame.draw.line(WIN, GREY, (j * gap, 0), (j * gap, width))

def draw(grid, numRows, width):
	for row in grid:
		for node in row:
			node.draw()

	drawGrid(numRows, WIDTH, blockSize)
	pygame.display.update()

def mousePosition_to_blockLocation(x, y):
	row = x // blockSize
	col = y // blockSize
	return row, col

def h(p1, p2): # distance between 2 points (heuristic function)
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(from_list, start, end):
	if end == start:
		return
	end.setColor(PURPLE)
	reconstruct_path(from_list, start, from_list[end])

def get_min_distance(distance, visited):
	minimum = next(iter(distance))
	for item in distance:
		if distance[item] < distance[minimum] and not visited[item]:
			minimum = item
	return minimum

def dijkstra(draw, grid, start, end):

	visited = {col: False for row in grid for col in row}
	distance = {col: float("inf") for row in grid for col in row}
	distance[start] = 0

	from_list = {}

	while any(visited):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return

		current = get_min_distance(distance, visited)

		if current == end:
			reconstruct_path(from_list,start,end)
			end.setColor(TURQUOISE)
			return

		for neighbour in current.neighbors:
			temp_dist = distance[current] + 1
			if temp_dist < distance[neighbour]:
				distance[neighbour] = temp_dist
				from_list[neighbour] = current

		current.setColor(BLUE)
		current.draw()
		start.setColor(ORANGE)
		start.draw()
		pygame.display.update()
		visited[current] = True

def main():
	WIN.fill(WHITE)
	running = True
	grid = nodesIntoGrid(numRows, WIDTH)
	start = None
	end = None
	while running:
		draw(grid, numRows, WIDTH)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					xPos, yPos = pygame.mouse.get_pos()
					r, c = mousePosition_to_blockLocation(xPos, yPos)
					node = grid[r][c]
					if not start and node != end:
						start = node
						start.setColor(GREEN)
					elif not end and node != start:
						end = node
						end.setColor(RED)
				elif event.button == 2:
					xPos, yPos = pygame.mouse.get_pos()
					r, c = mousePosition_to_blockLocation(xPos, yPos)
					node = grid[r][c]
					node.setColor(WHITE)
					if node == start:
						start = None
					elif node == end:
						end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					x = lambda: draw(grid, numRows, WIDTH)
					dijkstra(x, grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = nodesIntoGrid(numRows, WIDTH)
	pygame.quit()

main()
	