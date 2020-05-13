import random
from itertools import combinations
from util import Queue
from statistics import mean


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
        # This way doesn't use combinations() and therefore, should run in O(n) instead of O(n^2) ?
        friendships = set()
        possibilities = list(self.users.keys())
        num_connections = num_users * avg_friendships // 2
        while len(friendships) < num_connections:
            ranInd1 = random.randint(0, len(possibilities) - 1)
            ranInd2 = random.randint(0, len(possibilities) - 1)
            new_connection = tuple(
                [possibilities[ranInd1], possibilities[ranInd2]])
            connection_check = tuple(
                [possibilities[ranInd2], possibilities[ranInd1]])
            # As long as the 2 nums aren't the same,
            #  and that the inverse tuple isn't already in the friendships set,
            #  add the new connection
            if ranInd1 != ranInd2 and connection_check not in friendships:
                friendships.add(new_connection)
        # print(friendships)
        '''
        # The way to do it, according to the hints:
        #   Create a list with all possible friendship combinations.
        # print(list(self.users.keys()))
        possibilities = list(combinations(list(self.users.keys()), 2))
        # print(possibilities)

        # Shuffle the list
        possibilities = fisher_yates_shuffle(possibilities)

        # Get N (num_users * avg_friendships // 2) connections by grabbing the first N elements of the list
        friendships = possibilities[:(num_users*avg_friendships // 2)]
        print(friendships)
        # print("length of friendships: " + str(len(friendships)))
        '''
        # Add each of those to the graph.
        for friendship in friendships:
            self.add_friendship(friendship[0], friendship[1])

        ''' 
        # Another way to generate friendships, from lecture:
        
        possible_friendships = []
        # Avoid duplicates by ensuring the first number is smaller than the second
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))
        # Shuffle the possible friendships
        random.shuffle(possible_friendships)
        # Create friendships for the first X pairs of the list
        # X is determined by the formula: num_users * avg_friendships // 2
        # Need to divide by 2 since each add_friendship() creates 2 friendships
        for i in range(num_users * avg_friendships // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])
        '''

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
        # print(visited)
        return visited

    def bfs(self, starting_vertex, destination_vertex):
        '''
        print(
            f'Starting_vertex: {str(starting_vertex)}, Destination_vertex: {str(destination_vertex)}')
        '''
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
                        # print(f'Found path: {str(new_path)}')
                        return new_path
            visited.add(current_vertex)
        # print(f'No path found to {destination_vertex}')
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

    def calculate_percentage(self):
        '''
        Returns the average percentage of users in a network that aren't directly connected to a user, but
        are in a user's extended social network
        Sum(
        Users in user's extended social network, but not connected directly / total users in user's extended network * 100
        ) / number of total users in network
        '''
        # Loop through all users in the network.
        #   Get the users directly connected to them. directly_connected
        #   Get the users connected to them with a path.
        #       paths = self.get_all_social_paths()
        #       all_connected = list(paths.keys())
        #   Find which users are connectly indirectly (all_connected - directly_connected)
        #   percentage_for_user = num_indirectly_connected/all_connected * 100
        # Then find the average percentage.
        percentages = []

        users = list(self.users)
        for user in users:
            directly_connected = self.friendships[user]
            # print(directly_connected)
            paths = self.get_all_social_paths(user)
            all_connected = list(paths.keys())
            # print(all_connected)
            indirectly_connected = set()
            for connected_user in all_connected:
                if connected_user not in directly_connected:
                    indirectly_connected.add(connected_user)
            # print(indirectly_connected)
            '''
            print(
                f'{user}: Direct: {directly_connected}, All: {all_connected}, Indirect: {indirectly_connected}')
            '''
            percentage_for_user = len(
                list(indirectly_connected))/len(all_connected) * 100
            # print(percentage_for_user)
            percentages.append(percentage_for_user)

        # ave_percentage = sum(percentages)/len(percentages)
        ave_percentage = round(mean(percentages), 2)
        # print('\n')
        print(f'{ave_percentage}%')
        return ave_percentage

    def calculate_percentage2(self):
        '''
        For each user in a network, finds the percentage of users that are connected (directly or indirectly) to that user.
        connected_users/total_users * 100

        And then finds the ave percentage for all the users in the network.
        '''
        percentages = []

        users = list(self.users)
        for user in users:
            paths = self.get_all_social_paths(user)
            all_connected = list(paths.keys())
            percentage = len(all_connected) / len(users) * 100
            # print(percentage)
            # print(f'{len(all_connected)}/{len(users)} * 100 = {percentage}')
            percentages.append(percentage)

        ave_percentage = round(mean(percentages), 2)
        print(f'{ave_percentage}%')
        return ave_percentage

    def calculate_ave_degree_of_separation_overall(self):
        '''
        Returns the average degree of separation between each user and his/her extended network,
        in the entire network.

        The distance, or degrees of separation, between any two nodes is the number of links 
        along the shortest path that separates them.
         = len(shortest_path) - 1

        Loop through each user in the network.
            Get the paths for each user and his/her connections:
                For each user,
                    For each connection,
                        Calculate the length of each path - 1 = degrees_of_separation
                Calculate the ave degrees_of_separation for that user.

        Calculate the overall ave degrees_of_separation.
        '''
        degrees = []
        users = list(self.users)
        for user in users:
            degree = self.calculate_ave_degree_of_separation_for_user(user)
            degrees.append(degree)

        ave_degree = round(mean(degrees), 0)
        print(f'Overall average degrees of separation: {ave_degree}%')
        return ave_degree

    def calculate_ave_degree_of_separation_for_user(self, user):
        degrees = []
        paths = list(self.get_all_social_paths(user).values())
        for path in paths:
            # print(path)
            degree = len(path) - 1
            degrees.append(degree)
        ave_degrees = round(mean(degrees), 2)
        # print(f'Average degrees for user {user}: {ave_degrees}')
        return ave_degrees


def fisher_yates_shuffle(l):
    for i in range(0, len(l)):
        random_index = random.randint(i, len(l) - 1)
        l[random_index], l[i] = l[i], l[random_index]
    return l


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(100, 5)  # 10, 2

    '''
    for user in sg.users:
        print(f'{user}: {sg.users[user].name}')
    '''

    # print(sg.friendships)
    # print('\n')
    # sg.print_friendships_info()

    # print('\n')
    # connections = sg.get_all_social_paths(1)
    # print(connections)

    # sg.calculate_percentage()
    # sg.calculate_percentage2()
    sg.calculate_ave_degree_of_separation_overall()
