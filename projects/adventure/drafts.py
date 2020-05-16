def create_traversal_path():
    visited_rooms = set()
    player = Player(world.starting_room)
    visited_rooms.add(player.current_room)
    traversal_path = []
    stack = []
    graph = dict()
    graph[player.current_room.id] = dict()
    current_exits = player.current_room.get_exits()
    for exit in current_exits:
        graph[player.current_room.id][exit] = '?'
    print("graph so far: ")
    print(graph)

    # Find which directions are still unexplored
    unexplored_directions = [entry[0] for entry in list(
        graph[player.current_room.id].items()) if entry[1] == '?']
    move = unexplored_directions[random.randint(
        0, len(unexplored_directions) - 1)]
    print("time to go " + move)
    stack.append(move)
    # print("unexplored_directions" + str(unexplored_directions))
    # while len(visited_rooms) < len(room_graph):
    while len(stack) > 0:
        move = stack.pop()
        while len(unexplored_directions) > 0:
            # Pick a random unexplored direction from the current room.
            '''
            move = unexplored_directions[random.randint(
                0, len(unexplored_directions) - 1)]
            print("time to go " + move)
            '''
            # Hold on to the prev room's id to update the graph
            prev_room = player.current_room.id
            # Travel that direction
            player.travel(move)
            # Log that direction
            traversal_path.append(move)

            # Add current_room to visited_rooms
            visited_rooms.add(player.current_room)
            print("traversal_path: " + str(traversal_path))
            current_exits = player.current_room.get_exits()
            # Update the graph

            # Update the entry for the prev room
            graph[prev_room][move] = player.current_room.id

            # Make an entry for the current room if it's not already there
            if player.current_room.id not in graph:
                graph[player.current_room.id] = dict()
                for exit in current_exits:
                    graph[player.current_room.id][exit] = '?'

            # Update the entry for the current room.
            opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
            opposite = opposites[move]
            # print(opposite)
            graph[player.current_room.id][opposite] = prev_room
            print("graph so far: ")
            print(graph)

            # Find which directions are still unexplored
            unexplored_directions = [entry[0] for entry in list(
                graph[player.current_room.id].items()) if entry[1] == '?']
            # If still has unexplored_directions,
            # Pick a random unexplored direction from the current room.
            if len(unexplored_directions) > 0:
                move = unexplored_directions[random.randint(
                    0, len(unexplored_directions) - 1)]
                print("time to go " + move)
                # Add it to the stack
                stack.append(move)
            else:
                stack.append(opposites[move])

    print("Traversal_path is made! " + str(traversal_path))
    return traversal_path
