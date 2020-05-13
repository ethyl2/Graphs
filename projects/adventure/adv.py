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
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
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
traversal_path = ['n', 'n']


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
print("visited_rooms at start: " + str(visited_rooms))
'''
# Traversal graph creation
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
# print("unexplored_directions" + str(unexplored_directions))

while len(unexplored_directions) > 0:
    # Pick a random unexplored direction from the current room.
    move = unexplored_directions[random.randint(
        0, len(unexplored_directions) - 1)]
    print("time to go " + move)

    # Hold on to the prev room's id to update the graph
    prev_room = player.current_room.id
    # Travel that direction
    player.travel(move)
    # Log that direction
    traversal_path.append(move)
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

# When current room has no unexplored paths, walk back to nearest room that does contain an unexplored path.
#   -- Use a bfs for a room with a '?' for an exit.
'''
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
    print("visited_rooms: " + str(visited_rooms))

print("visited_rooms: ", str(visited_rooms))
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
