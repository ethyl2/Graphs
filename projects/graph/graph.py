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
        if v2 in self.vertices and v1 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            print(f'{v2} and/or {v1} is not in graph')
            raise IndexError("Vertex does not exist in graph")

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
        gray = set()
        queue = Queue()

        # Add the starting_vertex to the queue
        queue.enqueue(starting_vertex)

        # Stay in this loop as long as there are vertices in the queue
        while queue.size() > 0:
            # Get the head of the queue
            current = queue.dequeue()
            # Mark it gray
            gray.add(current)
            # Print it
            print(current)

            # Get its neighbors. If they are still white, make them gray and add them to the queue.
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in gray:
                    gray.add(neighbor)
                    queue.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Similar to bft, except using a stack instead of a queue
        gray = set()
        stack = Stack()

        gray.add(starting_vertex)
        stack.push(starting_vertex)

        while stack.size() > 0:
            current = stack.pop()
            gray.add(current)
            print(current)
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in gray:
                    gray.add(neighbor)
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

    def dft_recursive2(self, start, visited=None):
        # This version is very similar, but uses a set to store visited and subtracts visited in the loop
        # print(visited)
        if visited is None:
            visited = set()
        visited.add(start)
        print(start)

        for next in self.get_neighbors(start) - visited:
            self.dft_recursive2(next, visited)
        # return visited

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # keep track of explored nodes
        # gray = []
        gray = set()

        # keep track of all the paths to be checked
        # Unlike bft, the queue holds subarrays, the paths.
        queue = Queue()
        queue.enqueue([starting_vertex])

        # return queue if starting_vertex is the destination_vertex
        if starting_vertex == destination_vertex:
            return queue

        # keeps looping until all possible paths have been checked
        while queue:
            print("Current state of the queue: " + str(queue.queue))
            # get the head from the queue
            current_path = queue.dequeue()
            # get the last node from the path
            current_vertex = current_path[-1]
            print("Now visiting " + str(current_vertex) +
                  " whose neighbors are " + str(self.get_neighbors(current_vertex)))
            if current_vertex not in gray:
                neighbors = self.get_neighbors(current_vertex)
                # Go through all neighbor nodes
                #   Construct a new path which consists of the path, with the neighbor appended to it.
                #   Push the new path into the queue
                for neighbor in neighbors:
                    new_path = list(current_path)
                    new_path.append(neighbor)
                    queue.enqueue(new_path)
                    # return path if neighbor is destination_vertex
                    if neighbor == destination_vertex:
                        print("Found destination_vertex " +
                              str(destination_vertex) + "!")
                        return new_path

                # mark node as explored
                # gray.append(current_vertex)
                gray.add(current_vertex)

        # If there's no path between the 2 vertices:
        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path (not necessarily the shortest) from
        starting_vertex to destination_vertex in
        depth-first order.

        Note that there are multiple valid paths.
        """
        # Similar to bfs, except using a stack instead of a queue
        gray = []
        stack = Stack()

        gray.append(starting_vertex)
        # Unlike dft, the stack holds arrays (paths) instead of ints
        stack.push([starting_vertex])

        if starting_vertex == destination_vertex:
            return stack

        while stack.size() > 0:
            current_path = stack.pop()
            current_node = current_path[-1]
            gray.append(current_node)
            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor not in gray:
                    new_path = list(current_path)
                    new_path.append(neighbor)
                    if neighbor == destination_vertex:
                        return new_path
                    gray.append(neighbor)
                    stack.push(new_path)
        return None

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path (not necessarily the shortest)
        from starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.

        Note that there are multiple valid paths.
        """
        gray = {starting_vertex}
        path = [starting_vertex]

        return self.dfs_visit(starting_vertex, destination_vertex, path, gray)

    def dfs_visit(self, vertex, destination_vertex, path, gray):

        print("current vertex: " + str(vertex))

        if vertex == destination_vertex:
            print('found it!')
            return path

        neighbors = self.get_neighbors(vertex)
        for neighbor in neighbors:
            if neighbor not in gray:
                print(path)
                gray.add(neighbor)
                result = self.dfs_visit(
                    neighbor, destination_vertex, path + [neighbor], gray)
                print("result: " + str(result))
                if result is not None:
                    return result

    def dfs_paths(self, start, goal, path=None):
        # This is one way I found, which uses a generator.
        if path is None:
            path = [start]
        if start == goal:
            yield path
        for unvisited_neighbor in self.get_neighbors(start) - set(path):
            yield from self.dfs_paths(unvisited_neighbor, goal, path + [unvisited_neighbor])

    def return_path_from_dfs_paths(self, starting_vertex, ending_vertex):
        # Returns the first element that is generated by the dfs_paths method
        return list(self.dfs_paths(starting_vertex, ending_vertex))[0]

    def generate_dft_paths(self, starting_node, path=None):
        if path is None:
            path = [starting_node]

        unvisited_neighbors = self.get_neighbors(starting_node) - set(path)
        if len(unvisited_neighbors) < 1:
            yield path
        else:
            for unvisited_neighbor in unvisited_neighbors:
                yield from self.generate_dft_paths(unvisited_neighbor, path + [unvisited_neighbor])

    def get_all_dft_paths(self, starting_node):
        return list(self.generate_dft_paths(starting_node))


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

    # graph.dft_recursive(1)
    # print(graph.dft_recursive2(1))

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
    # print(graph.dfs(1, 6))

    # print(graph.dfs_recursive(1, 6))

    # print(list(graph.dfs_paths(1, 6)))
    # print(graph.return_path_from_dfs_paths(1, 6))
