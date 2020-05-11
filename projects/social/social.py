import random
from itertools import combinations
from util import Queue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        if num_users < avg_friendships:
            print(
                "Error: The number of users must be greater than the average number of friendships.")
            return None

        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        name_num = 0
        for i in range(0, num_users):
            name_num += 1
            self.add_user(f'Name{name_num}')

        # Create friendships:
        #   Create a list with all possible friendship combinations.
        # print(list(self.users.keys()))
        possibilities = list(combinations(list(self.users.keys()), 2))
        # print(possibilities)

        # Shuffle the list
        possibilities = fisher_yates_shuffle(possibilities)

        # Get N (num_users * avg_friendships // 2) connections by grabbing the first N elements of the list
        friendships = possibilities[:(num_users*avg_friendships // 2)]
        # print(friendships)
        # print("length of friendships: " + str(len(friendships)))

        # Add each of those to the graph.
        for friendship in friendships:
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.

        Loop through all of the users in the network.
        Get the bfs path from the user_id to that user.
        If there is a path,
            add the key/value pair of 'user: [bfs path]' to the visited dictionary.
        """
        visited = {}  # Note that this is a dictionary, not a set

        # Loop through all the users, to get the ones that aren't connected directly,
        # as well as the ones connnected directly.
        users = list(self.users)

        for user in users:
            # call bfs() with user_id as starting_vertex, user as destination_vertex
            path = self.bfs(user_id, user)
            # If the path is not []
            #   add to the visited dictionary
            #       value  <- user
            #       key <- path returned from bfs()
            if len(path) > 0:
                visited[user] = path
        return visited

    def bfs(self, starting_vertex, destination_vertex):
        print(
            f'Starting_vertex: {str(starting_vertex)}, Destination_vertex: {str(destination_vertex)}')
        visited = set()
        queue = Queue()
        queue.enqueue([starting_vertex])

        # return list containing the vertex if starting_vertex is the destination_vertex
        if starting_vertex == destination_vertex:
            return [starting_vertex]

        while queue.size() > 0:
            current_path = queue.dequeue()
            current_vertex = current_path[-1]
            if current_vertex not in visited:
                neighbors = list(self.friendships[current_vertex])
                for neighbor in neighbors:
                    new_path = list(current_path)
                    new_path.append(neighbor)
                    queue.enqueue(new_path)
                    if neighbor == destination_vertex:
                        print(f'Found path: {str(new_path)}')
                        return new_path
            visited.add(current_vertex)
        print(f'No path found to {destination_vertex}')
        return []

    def print_friendships_info(self):
        print(self.friendships)
        print("length of friendships: " + str(len(self.friendships)))
        print('\n')
        for user in list(self.friendships.items()):
            print(user)
        print('\n')
        total_connections = 0
        for user in list(self.friendships.items()):
            print(f'{user[0]}: num friends -- {len(list(user[1]))}')
            total_connections += len(list(user[1]))
        print('\n')
        print('total connections: ' + str(total_connections))
        ave_num_connections = total_connections/len(list(self.users))
        print('ave_num_connections: ' + str(ave_num_connections))


def fisher_yates_shuffle(l):
    for i in range(0, len(l)):
        random_index = random.randint(i, len(l) - 1)
        l[random_index], l[i] = l[i], l[random_index]
    return l


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)  # 10, 2

    '''
    for user in sg.users:
        print(f'{user}: {sg.users[user].name}')
    '''

    print(sg.friendships)
    print('\n')
    # sg.print_friendships_info()
    # print('\n')
    connections = sg.get_all_social_paths(1)
    print(connections)
