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
        self.vertices[v1].add(v2)

    def bdfs_recursive(self, start_vert, taret_value, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []
        visited.add(start_vert)
        path = path + [start_vert]
        if start_vert == taret_value:
            return path
        for child_vert in self.vertices[start_vert]:
            if child_vert not in visited:
                new_path = self.bdfs_recursive(
                    child_vert, taret_value, visited, path)
                if new_path:
                    return new_path
        return None


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
print(graph.bdfs_recursive(1, 6))
