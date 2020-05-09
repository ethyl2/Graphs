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
    # Put the ancestors into a graph. Probably with directed edges pointing from child to parent.
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
    print(graph)
    for element in graph.vertices:
        print(f'{element}: {graph.vertices[element]}')
    # Do a modified search -- dft? -- saving the paths, in order to later figure out the longest path,
    # and to return the element at index -1 of the longest path.
    # If 2 or more paths are all the longest, return just the lowest ID.
    # If no paths are longer than 1, return -1.


test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
                  (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
earliest_ancestor(test_ancestors, 1)
