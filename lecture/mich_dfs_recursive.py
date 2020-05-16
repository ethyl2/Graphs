def dfs_recursive(self, starting_vertex, destination_vertex, path=None):
    result = None
    if not path:
        path = []
    if len(path) == 0:
        path.append(starting_vertex)
    if path[-1] == destination_vertex:
        return path
    next_vertex = path[-1]
    for v in self.vertices[next_vertex]:
        if v not in path:
            new_path = list(path)
            new_path.append(v)
            result = self.dfs_recursive(
                starting_vertex, destination_vertex, new_path)
    return result
