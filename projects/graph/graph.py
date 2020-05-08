"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            print(f'{v2} is not in graph')
        # Should we add a check to see if v1 is in the graph, too?

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        return None

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # Pseudo-code from lecture:
        # Mark all vertices as white
        # Mark the starting_vertex as gray
        # Enqueue the starting_vertex
        # While the queue is not empty:
        #   Assign a pointer to the head of the queue
        #   Loop through the head's neighbors:
        #       If the neighbor is white:
        #           Color it gray
        #           Add it to the queue
        #   Now, dequeue the head
        #   And mark it as black.
        #   And print it.

        # Assume the vertices are all white at first
        gray = []
        queue = Queue()

        # Add the starting_vertex to the queue
        queue.enqueue(starting_vertex)

        # Stay in this loop as long as there are vertices in the queue
        while queue.size() > 0:
            # Get the head of the queue
            current = queue.dequeue()
            # Mark it gray
            gray.append(current)
            # Print it
            print(current)

            # Get its neighbors. If they are still white, make them gray and add them to the queue.
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in gray:
                    gray.append(neighbor)
                    queue.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Similar to bft, except using a stack instead of a queue
        gray = []
        stack = Stack()

        gray.append(starting_vertex)
        stack.push(starting_vertex)

        while stack.size() > 0:
            current = stack.pop()
            gray.append(current)
            print(current)
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in gray:
                    gray.append(neighbor)
                    stack.push(neighbor)

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        gray = []

        def dft_visit(vertex):
            gray.append(vertex)
            print(vertex)
            neighbors = self.get_neighbors(vertex)
            for neighbor in neighbors:
                if neighbor not in gray:
                    dft_visit(neighbor)

        dft_visit(starting_vertex)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        pass  # TODO

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        pass  # TODO

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)

    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    # print(graph.vertices)

    # graph.add_edge(4, 0)
    # print(graph.get_neighbors(7))

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    # graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # graph.dft(1)

    graph.dft_recursive(1)
    """
    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
    """
