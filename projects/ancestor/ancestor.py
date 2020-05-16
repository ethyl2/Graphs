from graph import Graph


def earliest_ancestor(ancestors, starting_node):
    '''
    Given a list of ancestors, such as [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), 
    (4, 8), (8, 9), (11, 8), (10, 1)]
    in the format (parent, child)
    And a starting_node,
    Return the node at the furthest distance from the starting_node. 
    If more than one node is found at that furthest distance, return the one with the lowest ID.
    If the starting_node has no parents, return -1.
    '''
    # Put the ancestors into a graph, with directed edges pointing from child to parent.
    graph = Graph()

    # Add the vertices
    for pair in ancestors:
        if not pair[0] in graph.vertices:
            graph.add_vertex(pair[0])
        if not pair[1] in graph.vertices:
            graph.add_vertex(pair[1])
    '''
    print(graph)
    for element in sorted(graph.vertices.keys()):
        print(element)
    '''
    # Add the edges.
    for pair in ancestors:
        graph.add_edge(pair[1], pair[0])

    '''
    print(graph)
    for element in graph.vertices:
        print(f'{element}: {graph.vertices[element]}')
    '''
    # Do a modified dft which saves the paths, in order to later figure out the longest path,
    #   and to return the element at index -1 of the longest path.

    # Call the get_all_dfs_paths() method to find the dfs paths
    candidate_paths = graph.get_all_dft_paths(starting_node)

    # If only the starting_node is in the path, it has no parents, so return -1
    if len(candidate_paths[0]) == 1:
        # print("no parents")
        return -1

    # If there is only 1 path, return the tail of the path.
    elif len(candidate_paths) == 1:
        # print(candidate_paths[0][-1])
        return candidate_paths[0][-1]

    else:
        # Find the longest path length.
        longest_path_length = max([len(path) for path in candidate_paths])
        # print("longest_path_length: " + str(longest_path_length))

        # Find the paths that have that length.
        longest_paths = [path for path in candidate_paths if len(
            path) == longest_path_length]
        # print("longest paths: " + str(longest_paths))

        # Return the tail with the smallest ID
        # print(min([x[-1] for x in longest_paths]))
        return min([x[-1] for x in longest_paths])


if __name__ == '__main__':
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
                      (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    print(earliest_ancestor(test_ancestors, 9))
