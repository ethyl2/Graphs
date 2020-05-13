islands = [[0, 1, 0, 1, 0],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [1, 0, 1, 0, 0],
           [1, 1, 0, 0, 0]]

class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

def island_counter(matrix):
    # Create a "visited" data structure
    visited = []

    for i in range(len(matrix)):
        visited.append([False] * len(matrix[0]))

    island_count = 0

    # Walk through all the nodes, elements in the input matrix
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):

            # If it's not visited:
            if not visited[row][col]:
                # If the value in the matrix at this position is a 1:
                if matrix[row][col] == 1:
                    # Do a traversal and mark each as visited
                    visited = dft(row, col, matrix, visited)

                    # Increment island counter
                    island_count += 1

                else:
                    # we hit water (0)
                    visited[row][col] = True

    return island_count

def dft(row, col, matrix, visited):
    s = Stack()

    # push starting vert on the stack
    s.push((row, col))

    # while stack not empty
    while s.size() > 0:
        # pop the first vert

        v = s.pop()

        row, col = v

        # If not visited, traverse!
        if not visited[row][col]:

            # Mark visited
            visited[row][col] = True

            for neighbor in get_neighbors(row, col, matrix):
                s.push(neighbor)

    return visited


def get_neighbors(row, col, matrix):
    neighbors = []

    # Check north
    if row > 0 and matrix[row - 1][col] == 1:
        neighbors.append((row-1, col))

    # Check south
    if row < len(matrix) - 1 and matrix[row + 1][col] == 1:
        neighbors.append((row+1, col))

    # Check west
    if col > 0 and matrix[row][col - 1] == 1:
        neighbors.append((row, col - 1))

    # Check east
    if col < len(matrix[0]) - 1 and matrix[row][col + 1] == 1:
        neighbors.append((row, col + 1))

    return neighbors

print(island_counter(islands))
