
# ID: <5959558329>
# DATE: 2022-11-24
# DESCRIPTION: <This program reads in user given profile and connection files and will create a similarity matrix
# along with recommendations for each member's friends. The program will then prompt the user a series of options and
# based on that, the program will execute various functions (ie. recommend friends, add friend, show friend graph, etc.>


from Graph import *
from typing import IO, Tuple, List

# TODO
# Declare and initialize constant variables
PROGRAMMER = "Charlie"
MEMBER_INFO = "1"
NUM_OF_FRIENDS = "2"
LIST_OF_FRIENDS = "3"
RECOMMEND = "4"
SEARCH = "5"
ADD_FRIEND = "6"
REMOVE_FRIEND = "7"
SHOW_GRAPH = "8"
SAVE = "9"

LINE = "\n*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*\n"


# TODO Complete the class.
class Member:
    # constructor method to set parameters of the class as well as declare the value
    def __init__(self, member_id: int,
                 first_name: str,
                 last_name: str,
                 email: str,
                 country: str,
                 connections):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.country = country
        self.connections = connections

    # this function adds another unique member id to the connections list
    def add_friend(self, friend_id) -> None:
        # Check if the friend_id is not already in the list
        # set repeat variable to false to check if there is a repeat
        repeat = False
        # iterate through the length of connections and check if the given member id matches any current connection
        for i in range(0, self.connections.len):
            # if there is a match, set repeat to true
            if friend_id == self.connections[i]:
                repeat = True
        # if repeat is false, we add a new connection
        if not repeat:
            self.connections.append(friend_id)

    # this function removes a specified member id from the connections list
    def remove_friend(self, friend_id) -> None:
        # Check if the friend_id is already in the list
        # set the breakpoint variable
        not_found = True
        # set the loop counter
        i = 0
        # while breakpoint is not reached and counter is less than the length of the connections, continue iterating
        while not_found and i < self.connections.len:
            # if the counter id matches the friend id we want to remove, then remove that connection
            if i == friend_id:
                self.connections[i].remove(friend_id)

    # this function returns the list of the members connections' id
    def friend_list(self) -> List[int]:
        # Return friends list
        return self.connections

    # this function returns the number of connections the member has
    def number_of_friends(self) -> int:
        # return the length of the connections list
        return self.connections.len

    # this function overrides the print function to print out a unique string message
    def __str__(self) -> str:
        # must be in the format as shown in the handout
        return self.first_name + " " + self.last_name + "\n" + self.email + \
               "\n" + "From " + self.country + "\n" + "Has " + str(self.connections.len) + " friends.\n"

    # Do not change
    def display_name(self) -> str:
        return self.first_name + " " + self.last_name


# this function prompts the user for a file name and opens that file
def open_file(file_type: str) -> IO:
    # prompt the user for a filename
    file_name = input("Enter the " + file_type + " filename:\n")
    # TODO To save time, comment out the above line and uncomment the following section.
    # TODO Do not forget to return it back before submitting.
    # if file_type == "profile":
    #     file_name = "profile_10.csv"
    # else:
    #     file_name = "connection_10.txt"
    file_pointer = None
    # check for if the filename is valid
    while file_pointer is None:
        try:
            # attempt to open the file
            file_pointer = open(file_name, "r")
        except IOError:
            # if there is an error opening the file, print this
            print(f"An error occurred while opening the file {file_name}.\n"
                  f"Make sure the file path and name are correct \nand that "
                  f"the file exist and is readable.")
            # re-prompt the user for a filename
            file_name = input("Enter the " + file_type + " filename:\n")
    # return the file pointer
    return file_pointer


# this function creates the network based on the file the user gives
# takes in a file pointer as a parameter and returns a matrix containing the network
def create_network(fp: IO) -> List[List[int]]:
    # get the size of the line
    size = int(fp.readline())
    network = []

    # iterate through the size of the file line
    for i in range(size):
        # append the values to matrix
        network.append([])

    # read in the line
    line = fp.readline()

    # while the line is not empty and the length of the line is greater or equal to 3
    # iterate through the lines
    while line is not None and len(line) >= 3:
        # split the lines by whitespace
        split_line = line.strip().split(" ")
        # get the member id of the first column
        member_id1 = int(split_line[0])
        # get the member id of the second column
        member_id2 = int(split_line[1])
        # if not a duplicate, add a connection between the 2 id's
        if member_id2 not in network[member_id1]:
            network[member_id1].append(member_id2)
        # if not a duplicate, add a connection between the 2 id's
        if member_id1 not in network[member_id2]:
            network[member_id2].append(member_id1)

        # sort the matrix of member 1 and 2
        network[member_id1].sort()
        network[member_id2].sort()
        # get a new line
        line = fp.readline()

    # return the matrix
    return network


# this function finds the number of common friends between 2 members friends lists
def num_in_common_between_lists(list1: List, list2: List) -> int:
    # set the counter variable
    degree = 0
    # iterate through the length of member 1
    for i in range(len(list1)):
        # if there is a common friend, iterate the counter
        if list1[i] in list2:
            degree += 1
    # return the counter
    return degree


# this function creates a 2D matrix with the size of the # of members by the # of members
def init_matrix(size: int) -> List[List[int]]:
    # declare the matrix
    matrix = []
    # iterate through the length of size
    for row in range(size):
        # append a space at each iteration
        matrix.append([])
        # populate the columns with 0
        for column in range(size):
            matrix[row].append(0)

    # return the matrix
    return matrix


# this function calculates the similarity score between 2 members
def calc_similarity_scores(profile_list: List[Member]) -> List[List[int]]:
    # create the matrix by calling the init_matrix function, passing the profile list that was read in
    matrix = init_matrix(len(profile_list))

    # iterate through the length of the profile_list
    for i in range(len(profile_list)):
        # iterate through the length of i profile_lists' size
        for j in range(i, len(profile_list)):
            # call the num in common function to get a similarity score
            degree = num_in_common_between_lists(
                profile_list[i].friends_id_list,
                profile_list[j].friends_id_list)

            # add the similarity score to the matrix for both members
            matrix[i][j] = degree
            matrix[j][i] = degree

    # return the matrix
    return matrix


# this function will recommend a member a friend based on similarity scores
def recommend(member_id: int, friend_list: List[int], similarity_list: List[int]) -> int:
    max_similarity_val = -1
    max_similarity_pos = -1

    # iterate through the length of the similarity_list
    for i in range(len(similarity_list)):
        # check if the 2 are not friends already
        if i not in friend_list and i != member_id:
            # if the similarity score is enough, then update the max_similarity position
            if max_similarity_val < similarity_list[i]:
                max_similarity_pos = i
                max_similarity_val = similarity_list[i]

    # return the recommended id
    return max_similarity_pos


# this function creates the profile list given the file pointer
def create_members_list(profile_fp: IO) -> List[Member]:
    # declare the profiles list
    profiles = []
    # read in the lines
    profile_fp.readline()
    line = profile_fp.readline()
    # split the lines by commas (bc the file being read in is a csv file
    profile_list = line.split(',')
    # while there are still lines and the length of profile_list is 5
    while line is not None and len(profile_list) == 5:
        # create a member class and append it to the profile list
        mem = Member(profile_list[0], profile_list[1], profile_list[2], profile_list[3], profile_list[4],
                     profile_list.friends_id_list)
        profiles.append(mem)

    # return the profile list
    return profiles


# this function prompts the user to choose an option from a menu
def display_menu():
    # print the display menu
    print("\nPlease select one of the following options.\n")
    print(MEMBER_INFO + ". Show a member's information \n" +
          NUM_OF_FRIENDS + ". Show a member's number of friends\n" +
          LIST_OF_FRIENDS + ". Show a member's list of friends\n" +
          RECOMMEND + ". Recommend a friend for a member\n" +
          SEARCH + ". Search members by country\n" +
          ADD_FRIEND + ". Add friend\n" +
          REMOVE_FRIEND + ". Remove friend\n" +
          SHOW_GRAPH + ". Show graph\n" +
          SAVE + ". Save changes\n"
          )

    return input("Press any other key to exit.\n")


# check to see if the given member id is valid
def receive_verify_member_id(size: int):
    valid = False
    # iterate while checking that valid is false
    while not valid:
        # if valid is false, prompt the user to enter a valid mamber id
        member_id = input(f"Please enter a member id between 0 and {size}:\n")
        # check if the given id is a digit
        if not member_id.isdigit():
            # TODO provide proper message.
            print("This is not a valid entry.")
        # check if the given id is within the bounds of the id's
        elif not 0 <= int(member_id) < size:
            # TODO provide proper message.
            print("This is not a valid entry")
        else:
            valid = True
    # return the member id
    return int(member_id)


# this function creates a connection between 2 friends
def add_friend(profile_list: List[Member],
               similarity_matrix: List[List[int]]) -> None:
    # get the size of the profile_list
    size = len(profile_list)
    # prompt the user for 2 member id's
    print("For the first friend: ")
    member1 = input(f"Please enter a member id between 0 and {size}:\n")
    print("For the second friend: ")
    member2 = input(f"Please enter a member id between 0 and {size}:\n")

    # check to see they aren't the same id and aren't friends already
    if member1 == member2:
        print("You need to enter two different ids. Please try again.")
    elif member1 in profile_list[member2].friends_id_list:
        print("These two members are already friends. Please try again.")
    else:
        # call the add_friend function for both members
        profile_list[member1].add_friend(member2)
        profile_list[member2].add_friend(member1)

        # update the similarity matrix
        for i in range(size):
            if member2 in profile_list[i].friends_id_list:
                similarity_matrix[member1][i] += 1
                if member1 != i:
                    similarity_matrix[i][member1] += 1
            if member1 in profile_list[i].friends_id_list:
                similarity_matrix[member2][i] += 1
                if member2 != i:
                    similarity_matrix[i][member2] += 1

        print("The connection is added. Please check the graph.")


# this function removes a connection between 2 members
def remove_friend(profile_list: List[Member],
                  similarity_matrix: List[List[int]]) -> None:
    size = len(profile_list)
    # get the id of the first friend and ask the user for a friend of theirs
    print("For the first friend: ")
    member1 = receive_verify_member_id(size)

    print(f"For the second friend, select from following list: {profile_list[member1].friends_id_list}")
    member2 = receive_verify_member_id(size)
    # check to make sure they aren't the same id and that these 2 id's are indeed friends
    if member1 == member2:
        print("You need to enter two different ids. Please try again.")
    elif member1 not in profile_list[member2].friends_id_list:
        print("These two members are not friends. Please try again.")
    else:
        # call remove_friend for each member class
        profile_list[member1].remove_friend(member2)
        profile_list[member2].remove_friend(member1)

        # update the similarity matrix
        for i in range(size):

            if member2 in profile_list[i].friends_id_list:
                # TODO
                similarity_matrix = calc_similarity_scores(profile_list)
            if member1 in profile_list[i].friends_id_list:
                # TODO
                similarity_matrix = calc_similarity_scores(profile_list)

        similarity_matrix[member1][member1] -= 1
        similarity_matrix[member2][member2] -= 1

        print("The connection is removed. Please check the graph.")


# This function asks for a country name and list all members from that country.
def search(profile_list: List[Member]) -> None:
    # ask for a country name
    c = input("Please enter a country name")
    # iterate through the length of profile list
    for i in range(0, profile_list.len):
        # if the people is from that country, print their first and last name
        if profile_list[i].country == c:
            print(profile_list[i].first_name + " " + profile_list[i].last_name)


# Do not change.
# this function adds friends to profiles
def add_friends_to_profiles(profile_list: List[Member],
                            network: List[List[int]]) -> None:
    for i in range(len(profile_list)):
        profile_list[i].friends_id_list = network[i]


# this function asks the user what they want to do
def select_action(profile_list: List[Member],
                  network: List[List[int]],
                  similarity_matrix: List[List[int]]) -> str:
    # get user input and display the menu
    response = display_menu()

    print(LINE)
    size = len(profile_list)

    if response in [MEMBER_INFO, NUM_OF_FRIENDS, LIST_OF_FRIENDS, RECOMMEND]:
        member_id = receive_verify_member_id(size)

    # complete function if it matches the user prompt
    # always check for a valid user input
    if response == MEMBER_INFO:
        temp = receive_verify_member_id(size)
        # print using the overriden print function
        profile_list[temp].__str__()
        print(LINE)
    elif response == NUM_OF_FRIENDS:
        # TODO Complete the code
        temp = receive_verify_member_id(size)
        # get the number of friends of the person
        num = profile_list[temp].number_of_friends()
        print(profile_list[temp].name + " has " + num + " friends.\n")
        print(LINE)
    elif response == LIST_OF_FRIENDS:
        # TODO Complete the code
        temp = receive_verify_member_id(size)
        friends = profile_list[temp].friends_list()
        # print the id and first/last name of every friend of a given person
        for i in range(0, friends.len):
            print(friends[i].id + " " + friends[i].first_name + " " + friends[i].last_name + "\n")
        print(LINE)
    elif response == RECOMMEND:
        # TODO Complete the code
        temp = receive_verify_member_id(size)
        # call the recommend function
        rec_id = recommend(temp, profile_list[temp].connections, similarity_matrix)
        # print the message
        print("The suggested friend for " + profile_list[temp].first_name + " " + profile_list[temp].last_name +
              " is " + profile_list[rec_id].first_name + " " + profile_list[rec_id].last_name + " with id " + rec_id)
        print(LINE)
    elif response == SEARCH:
        search(profile_list)
        print(LINE)
    elif response == ADD_FRIEND:
        # TODO Complete the code
        add_friend(profile_list, similarity_matrix)
    elif response == REMOVE_FRIEND:
        # TODO Complete the code
        remove_friend(profile_list, similarity_matrix)
    elif response == SHOW_GRAPH:
        tooltip_list = []
        # iterates through the profiles and appends the profile to the tooltip list
        for profile in profile_list:
            tooltip_list.append(profile)
        # create the graph class
        graph = Graph(PROGRAMMER,
                      [*range(len(profile_list))],
                      tooltip_list, network)
        # draw the graph
        graph.draw_graph()
        print("Graph is ready. Please check your browser.")
    elif response == SAVE:
        # TODO Complete the code
        save_changes(profile_list)

    else:
        return "Exit"

    print(LINE)

    return "Continue"


# this function will save the changes made
def save_changes(profile_list: List[Member]) -> None:
    file_name = input("Please enter the filename:")
    wf = open_file(file_name, "w")
    wf.write(profile_list.len + "\n")
    for i in range(0, profile_list.len):
        for j in range(0, profile_list[i].connections.len):
            wf.write(profile_list[i].member_id + profile_list[i].connections[j] + "\n")


# Do not change
# this function initializes the files and creates the similarity matrix
def initialization() -> Tuple[List[Member], List[List[int]], List[List[int]]]:
    # open the profiles file
    profile_fp = open_file("profile")
    profile_list = create_members_list(profile_fp)

    # open the connections file
    connection_fp = open_file("connection")
    network = create_network(connection_fp)
    # ensure the files have the same number of members
    if len(network) != len(profile_list):
        input("Both files must have the same number of members.\n"
              "Please try again.")
        exit()

    # add friends to the profiles
    add_friends_to_profiles(profile_list, network)
    # create similarity matrix
    similarity_matrix = calc_similarity_scores(profile_list)

    # close the files
    profile_fp.close()
    connection_fp.close()

    # return the profile list, network, and similarity matrix
    return profile_list, network, similarity_matrix


#  Do not change.
def main():
    print("Welcome to the network program.")
    print("We need two data files.")
    profile_list, network, similarity_matrix = initialization()
    action = "Continue"
    while action != "Exit":
        action = select_action(profile_list, network, similarity_matrix)

    input("Thanks for using this program.")


if __name__ == "__main__":
    main()
