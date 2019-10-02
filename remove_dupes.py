# Author: Huang Jian Wei
# Date Created: 1/10/2019
# Date Last Modified: 1/10/2019


def main():

    user_input = input("Enter name of file:\n")
    print("Name of file is: " + str(user_input))
    unique_set = set()

    with open(user_input) as file:
        for line in file:
            line = line.replace("\n", "")
            unique_set.add(line)

    unique_set = sorted(unique_set)
    print(str(unique_set))


if __name__ == "__main__":
    main()

