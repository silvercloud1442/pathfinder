import numpy as np

#bimbimbambam
x = 3
y = 3
# Создаем матрицу [x][y]
matrix = np.random.randint(0, 2, size=(x, y))

# Создаем матрицу смежности размером [x][y]
adj_matrix = np.zeros((x*y, x*y))

# Заполняем матрицу смежности
for i in range(x):
    for j in range(y):
        vertex = i * y + j  # Номер вершины в матрице смежности
        for r in range(max(0, i-1), min(x, i+2)):
            for c in range(max(0, j-1), min(y, j+2)):
                if r == i and c == j:
                    continue
                neighbor = r * y + c  # Номер соседней вершины в матрице смежности
                if matrix[r][c] == '.':
                    adj_matrix[vertex][neighbor] = 20000000
                else:
                    adj_matrix[vertex][neighbor] = 1
print(adj_matrix)