import sys
import os
from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
"""
room_graph=literal_eval(open(map_file, "r").read())
"""
with open(os.path.join(sys.path[0], map_file), 'r') as f:
    room_graph = literal_eval(f.read())


world.load_graph(room_graph)


# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)


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

    # Find which directions are still unexplored
    unexplored_directions = [entry[0] for entry in list(
        graph[player.current_room.id].items()) if entry[1] == '?']
    move = unexplored_directions[random.randint(
        0, len(unexplored_directions) - 1)]
    stack.append(move)
    # print("unexplored_directions" + str(unexplored_directions))
    while len(visited_rooms) < len(room_graph):
        # print("length of visited_rooms: " + str(len(visited_rooms)))
        # while len(stack) > 0:
        while len(visited_rooms) < len(room_graph):
            # print("current stack before popping: " + str(stack))
            move = stack.pop()
            # Hold on to the prev room's id to update the graph
            prev_room = player.current_room.id
            # Travel that direction
            player.travel(move)
            # Log that direction
            traversal_path.append(move)

            # Add current_room to visited_rooms
            visited_rooms.add(player.current_room)
            # print("traversal_path: " + str(traversal_path))
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
            print("graph so far: " + str(graph))
            # print(graph)

            # Find which directions are still unexplored
            unexplored_directions = [entry[0] for entry in list(
                graph[player.current_room.id].items()) if entry[1] == '?']
            # If still has unexplored_directions,
            # Pick a random unexplored direction from the current room.
            if len(unexplored_directions) > 0:
                move = unexplored_directions[random.randint(
                    0, len(unexplored_directions) - 1)]
                # Add it to the stack
                stack.append(move)
            else:
                if move in graph[player.current_room.id]:
                    stack.append(move)
                else:
                    choices = []
                    if 'n' in graph[player.current_room.id] and 'n' != move:
                        choices.append('n')
                    if 's' in graph[player.current_room.id] and 's' != move:
                        choices.append('s')
                    if 'e' in graph[player.current_room.id] and 'e' != move:
                        choices.append('e')
                    if 'w' in graph[player.current_room.id] and 'w' != move:
                        choices.append('w')
                    next_move = choices[random.randint(0, len(choices) - 1)]
                    stack.append(next_move)

    print("Traversal_path is made! " + str(traversal_path))
    return traversal_path


traversal_path = create_traversal_path()

# Test, where player travels through traversal_path.
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)

'''
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
'''
