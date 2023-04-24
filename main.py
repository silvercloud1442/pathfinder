import sys
import pygame
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


pygame.init()
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
MAP_SIZE = 3
TILE_SIZE = SCREEN_WIDTH / MAP_SIZE
MOUSE_DOWN = False
START = (0,0)
FINISH = (17, 17)
G = nx.Graph()
adj_matrix = np.zeros((MAP_SIZE ** 2, MAP_SIZE  ** 2))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WINDOW = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
MAP = []


for i in range(MAP_SIZE):
    row = []
    for j in range(MAP_SIZE):
        if (i, j) == START:
            cell = '#'
        elif (i, j) == FINISH:
            cell = '@'
        else:
            cell = ''
        row.append(cell)
    MAP.append(row)

def get_graph(MAP):
    for i in range(len(adj_matrix)):
        for j in range(i + 1, len(adj_matrix)):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)
    nx.draw(G, with_labels=True)
    plt.show()

def get_adj(MAP):
    x = MAP_SIZE
    y = MAP_SIZE
    for i in range(x):
        for j in range(y):
            vertex = i * y + j# Номер вершины в матрице смежности
            for r in range(max(0, i - 1), min(x, i + 2)):
                for c in range(max(0, j - 1), min(y, j + 2)):
                    if r == i and c == j:
                        continue
                    neighbor = r * y + c # Номер соседней вершины в матрице смежности
                    if abs((vertex - r) + (neighbor - c)) != 3 :
                        if MAP[r][c] == '.':
                            adj_matrix[vertex][neighbor] = 0
                        else:
                            adj_matrix[vertex][neighbor] = 1
    print(adj_matrix)

def draw_map(WINDOW, TILE_SIZE, MAP):
    wall_color = (190, 190, 190)
    space_color = (65, 65, 65)

    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            cell = MAP[i][j]
            if cell == '#':
                color = (0, 0, 190)
            elif cell == '@':
                color = (0, 190, 0)
            else:
                color = space_color if MAP[i][j] == '' else wall_color
            pygame.draw.rect(WINDOW, color, (TILE_SIZE * i, TILE_SIZE * j, TILE_SIZE - 1, TILE_SIZE - 1))

get_adj(MAP)
get_graph(MAP)

for i in range(len(adj_matrix)):
    G.add_node(i)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            MOUSE_DOWN = True
            x, y = pygame.mouse.get_pos()
            cell_x = int(x // TILE_SIZE)
            cell_y = int(y // TILE_SIZE)
            MAP[cell_x][cell_y] = '.'
            get_adj(MAP)

        if event.type == pygame.MOUSEBUTTONUP:
            MOUSE_DOWN = False

        if event.type == pygame.MOUSEMOTION and MOUSE_DOWN:
            x, y = pygame.mouse.get_pos()
            cell_x = int(x // TILE_SIZE)
            cell_y = int(y // TILE_SIZE)
            MAP[cell_x][cell_y] = '.'
            get_adj(MAP)
        if event.type == pygame.K_SPACE:
            get_graph(MAP)

    draw_map(WINDOW, TILE_SIZE, MAP)

    screen.blit(WINDOW, (0,0))
    pygame.display.flip()
    clock.tick(60)