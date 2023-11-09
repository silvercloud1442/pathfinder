import sys
import pygame
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import deque


pygame.init()
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
MAP_SIZE = 20
TILE_SIZE = SCREEN_WIDTH / MAP_SIZE
MOUSE_DOWN = False
START = 0
start_coords = (START // MAP_SIZE, START - (START // MAP_SIZE))
FINISH = 375
finish_coords = (FINISH // MAP_SIZE), FINISH - (FINISH // MAP_SIZE) * MAP_SIZE,
G = nx.Graph()
adj_matrix = np.zeros((MAP_SIZE ** 2, MAP_SIZE ** 2))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WINDOW = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
MAP = []

for i in range(MAP_SIZE):
    row = []
    for j in range(MAP_SIZE):
        if (i, j) == start_coords:
            cell = '#'
        elif (i, j) == finish_coords:
            cell = '@'
        else:
            cell = ''
        row.append(cell)
    MAP.append(row)

def update_map():
    for idx, row in enumerate(MAP):
        for idy, j in enumerate(row):
            if j.isdigit():
                MAP[idx][idy] = ''

def get_graph():
    for i in range(len(adj_matrix)):
        for j in range(i + 1, len(adj_matrix)):
            if adj_matrix[i][j] == 1:
                G.add_edge(i, j)
    nx.draw(G, with_labels=True)
    plt.show()

def get_adj():
    global MAP
    adj_matrix = np.zeros((MAP_SIZE ** 2, MAP_SIZE ** 2))
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
                    if (abs(i - r) + abs(j - c) == 1) and MAP[r][c] != '.' and MAP[i][j] != '.':
                        adj_matrix[vertex][neighbor] = 1
    return adj_matrix

def draw_map(WINDOW, TILE_SIZE, MAP, path):
    wall_color = (190, 190, 190)
    space_color = (65, 65, 65)

    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            cell = MAP[i][j]
            if cell == '#':
                color = (0, 0, 190)
            elif cell == '@':
                color = (0, 190, 0)
            elif cell.isdigit():
                color = (255 - (int(cell) * int(255 / (len(path))) if path else 1), 0, int(cell) * int(255 / (len(path))) if path else 1)
            else:
                color = space_color if MAP[i][j] == '' else wall_color
            pygame.draw.rect(WINDOW, color, (TILE_SIZE * i, TILE_SIZE * j, TILE_SIZE - 1, TILE_SIZE - 1))

def dfs(adj_matrix, start, finish, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    visited.add(start)
    path.append(start)

    if start == finish:
        return path

    for neighbor in range(len(adj_matrix[start])):
        if adj_matrix[neighbor][start] != 0 and neighbor not in visited:
            new_path = dfs(adj_matrix, neighbor, finish, visited, path)
            if new_path:
                return new_path

    path.pop()
    return None


def bfs(graph, start, end):
    queue = deque()
    queue.append(start)
    visited = set()
    visited.add(start)
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            path = [end]
            while current != start:
                current = parent[current]
                path.append(current)
            return path
        for neighbor in range(len(graph[current])):
            if graph[current][neighbor] != 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    return None


def draw_path(MAP, path):
    for idx, i in enumerate(path):
        x = i - (i // MAP_SIZE) * MAP_SIZE
        y = i // MAP_SIZE
        MAP[y][x] = f'{idx}'
    return MAP

for i in range(len(adj_matrix)):
    G.add_node(i)

left = False
right = False
path = None

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.MOUSEWHEEL:
            adj_matrix = get_adj()
            path = bfs(adj_matrix, START, FINISH)
            print(path)
            update_map()

        if event.type == pygame.MOUSEBUTTONDOWN:
            MOUSE_DOWN = True
            if event.button == 1:
                left = True
                x, y = pygame.mouse.get_pos()
                if x >= 0 and x <= SCREEN_WIDTH - 1 and y >= 0 and y <= SCREEN_HEIGHT - 1:
                    cell_x = int(x // TILE_SIZE)
                    cell_y = int(y // TILE_SIZE)
                    MAP[cell_x][cell_y] = '.'
                    path = None
            if event.button == 3:
                right = True
                x, y = pygame.mouse.get_pos()
                if x >= 0 and x <= SCREEN_WIDTH - 1 and y >= 0 and y <= SCREEN_HEIGHT - 1:
                    cell_x = int(x // TILE_SIZE)
                    cell_y = int(y // TILE_SIZE)
                    MAP[cell_x][cell_y] = ''
                    path = None
            # adj_matrix = get_adj()
            # path = dfs(adj_matrix, START, FINISH)
            # print(path)
            # update_map()

        if event.type == pygame.MOUSEBUTTONUP:
            MOUSE_DOWN = False
            left = False
            right = False

        if event.type == pygame.MOUSEMOTION and MOUSE_DOWN:
            if left:
                x, y = pygame.mouse.get_pos()
                if x >= 0 and x <= SCREEN_WIDTH - 1 and y >= 0 and y <= SCREEN_HEIGHT - 1:
                    cell_x = int(x // TILE_SIZE)
                    cell_y = int(y // TILE_SIZE)
                    MAP[cell_x][cell_y] = '.'
                    path = None
            if right:
                x, y = pygame.mouse.get_pos()
                if x >= 0 and x <= SCREEN_WIDTH - 1 and y >= 0 and y <= SCREEN_HEIGHT - 1:
                    cell_x = int(x // TILE_SIZE)
                    cell_y = int(y // TILE_SIZE)
                    MAP[cell_x][cell_y] = ''
                    path = None
            # adj_matrix = get_adj()
            # path = dfs(adj_matrix, START, FINISH)
            # print(path)
            # update_map()


    if path:
        MAP = draw_path(MAP, path)


    draw_map(WINDOW, TILE_SIZE, MAP, path)

    screen.blit(WINDOW, (0,0))
    pygame.display.flip()
    clock.tick(60)