from room import Room
from player import Player
from world import World
from util import Queue
import sys
import os
import random
from ast import literal_eval
from typing import List


# Uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary

with open(os.path.join(sys.path[0], map_file), 'r') as f:
    room_graph = literal_eval(f.read())
    # print(room_graph)
world = World()
world.load_graph(room_graph)


class Game:
    def __init__(self):
        self.world = world
        self.player = Player(self.world.starting_room)
        self.moves_queue = Queue()
        self.path = []  # Traversal path to be created
        self.graph = {}  # Traversal graph to be created
        self.inverse_directions = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

    def backtrack_to_unexplored(self) -> List[int]:
        """
        Function for backtracking after a dead end has been reached, or after there are no more unexplored exits.
        Returns the path to get back to a room that has an unexplored direction to go to,
            specifically, a list of room id's from the player's current_room's id to the room with an unexplored direction.
        """
        backtracking_queue = Queue()
        visited = set()
        backtracking_queue.enqueue([self.player.current_room.id])
        while backtracking_queue.size() > 0:
            current_path = backtracking_queue.dequeue()
            prev_room = current_path[-1]
            if prev_room not in visited:
                visited.add(prev_room)
                for direction in self.graph[prev_room]:
                    if self.graph[prev_room][direction] == '?':
                        # found the way out
                        # print('path to backtrack: ', current_path)
                        return current_path
                    else:
                        # make a copy of the current_path
                        current_path_copy = list(current_path)
                        # Add the direction to it
                        current_path_copy.append(
                            self.graph[prev_room][direction])
                        # And add to the backtracking_queue
                        backtracking_queue.enqueue(current_path_copy)

        # If no valid backtracking path is found
        return []

    def enqueue_moves(self) -> None:
        """
        Adds to the moves_queue. 
            Either adds a direction to go to next, from the player's current room
                to a room that hasn't been explored (chosen randomly), 
                OR the directions needed to backtrack back to a room
                where there are unexplored exits.
        """
        current_room_exits = self.graph[self.player.current_room.id]

        unexplored_exits = []
        for direction in current_room_exits:
            if current_room_exits[direction] == '?':
                unexplored_exits.append(direction)
        if len(unexplored_exits) > 0:
            # Go to a random choice of the unexplored exits
            self.moves_queue.enqueue(
                unexplored_exits[random.randint(0, len(unexplored_exits)-1)])
        else:
            # Backtrack to a room that has unexplored exits
            # print("We need to backtrack.")
            path_to_unexplored = self.backtrack_to_unexplored()
            current_room_id = self.player.current_room.id
            for room_id in path_to_unexplored:
                for direction in self.graph[current_room_id]:
                    if room_id == self.graph[current_room_id][direction]:

                        self.moves_queue.enqueue(direction)
                        current_room_id = room_id
                        # Go on to next room in path_to_unexplored
                        break

    def create_path(self) -> None:
        new_room = {}
        for direction in self.player.current_room.get_exits():
            new_room[direction] = '?'
        self.graph[self.player.current_room.id] = new_room
        self.enqueue_moves()

        while self.moves_queue.size() > 0:
            # print('current moves_queue: ', moves_queue)
            starting_room_id = self.player.current_room.id
            next_direction = self.moves_queue.dequeue()
            self.player.travel(next_direction)
            self.path.append(next_direction)
            current_room_id = self.player.current_room.id
            self.graph[starting_room_id][next_direction] = current_room_id

            if current_room_id not in self.graph:
                # Create a new entry for it
                self.graph[current_room_id] = {}
                current_room_exits = self.player.current_room.get_exits()
                for direction in current_room_exits:
                    self.graph[current_room_id][direction] = '?'

            # Link the current room to the starting room
            self.graph[current_room_id][self.inverse_directions[next_direction]
                                        ] = starting_room_id
            '''
            print(
                f"Player started in room {starting_room_id} and went {next_direction} to {current_room_id}.")
            
            print('moves_queue size', moves_queue.size())
            '''
            # Get the next move if the moves_queue is empty.
            if self.moves_queue.size() <= 0:
                # print("moves_queue is empty, so time to call enqueue_moves")
                self.enqueue_moves()
        # return path

    def create_shortest_path(self, num):
        """
        Loops through path creation a specified number of times and keeps the shortest path generated as self.path
        """
        shortest_path_length = 99999999999
        shortest_path = []

        for i in range(num):
            self.path = []
            self.player.current_room = self.world.starting_room
            self.graph = {}
            self.moves_queue = Queue()
            self.create_path()

            if len(self.path) < shortest_path_length:
                shortest_path = self.path
                shortest_path_length = len(self.path)
        self.path = shortest_path

    def move_player_along_path(self) -> None:
        visited_rooms = set()
        self.player.current_room = self.world.starting_room
        visited_rooms.add(self.player.current_room)
        for direction in self.path:
            self.player.travel(direction)
            visited_rooms.add(self.player.current_room)

        print("Number of visited rooms: ", len(visited_rooms))
        print("Length of path: ", len(self.path))


game = Game()

# game.create_path()
game.create_shortest_path(500)
# print('path created: ', path)
# print('graph created: ', graph)
game.move_player_along_path()
