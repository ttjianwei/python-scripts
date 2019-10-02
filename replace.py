import os
import re
import time
import mimetypes

# Author: Huang Jian Wei
# Date Created: 26/9/2019
# Date Last Modified: 27/9/2019

# Regex Reference
# []	A set of characters	                                                            e.g "[a-m]"
# \	    Signals a special sequence (can also be used to escape special characters)	    e.g "\d"
# .	    Any character (except newline character)	                                    e.g "he..o"
# ^   	Starts with	"^hello"
# $	    Ends with "world$"
# *	    Zero or more occurrences	                                                    e.g "aix*"
# +	    One or more occurrences	"aix+"
# {}	Exactly the specified number of occurrences	"al{2}"
# |	    Either or "falls|stays"
# ()	Capture and group

# \A	Returns a match if the specified characters are at the beginning of the string	"\AThe"
# \b	Returns a match where the specified characters are at the beginning or at the end of a word	r"\bain"
#       r"ain\b"
# \B	Returns a match where the specified characters are present, but NOT at the beginning (or at the end) of a word
#       r"\Bain" r"ain\B"
# \d	Returns a match where the string contains digits (numbers from 0-9)	"\d"
# \D	Returns a match where the string DOES NOT contain digits	"\D"
# \s	Returns a match where the string contains a white space character	"\s"
# \S	Returns a match where the string DOES NOT contain a white space character	"\S"
# \w	Returns a match where the string contains any word characters (characters from a to Z, digits from 0-9, and the
#       underscore _ character)	"\w"
# \W	Returns a match where the string DOES NOT contain any word characters	"\W"
# \Z	Returns a match if the specified characters are at the end of the string	"Spain\Z"

# [arn]	        Returns a match where one of the specified characters (a, r, or n) are present
# [a-n]	        Returns a match for any lower case character, alphabetically between a and n
# [^arn]	    Returns a match for any character EXCEPT a, r, and n
# [0123]	    Returns a match where any of the specified digits (0, 1, 2, or 3) are present
# [0-9]	        Returns a match for any digit between 0 and 9
# [0-5][0-9]	Returns a match for any two-digit numbers from 00 and 59
# [a-zA-Z]	    Returns a match for any character alphabetically between a and z, lower case OR upper case
# [+]	        In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for
#               any + character in the string

log_file = open("log.txt", "a+")
format_date = time.strftime("%Y%m%d%M%S")

# Perform Logging Task
perform_logging = 1


def main():
    lprint(str(format_date) + ": INFO Initializing program...", perform_logging)
    # loop until user exit
    while 1:
        user_input = input("(1) for single file, (2) for directory,"
                           "(3) to exit:""\n1.) File\n2.) Directory\n3.) Exit\n")

        print("perform logging:" + str(perform_logging))

        if user_input == '3':
            print("Exiting program...")
            lprint(str(format_date) + " INFO Exiting program...", perform_logging)
            break

        # Relative path
        elif user_input == '1':
            try:
                filename = input("Input name of file:")
                lprint(str(format_date) + ": INFO Name of file is " + filename, perform_logging)
                print(filename)
            except Exception:
                print("Cannot find file or invalid file! Please try again.")

            try:
                blacklist = input("Input name of blacklist:")
                lprint(str(format_date) + ": INFO Name of blacklist is " + blacklist, perform_logging)
                print(blacklist)

            except Exception:
                print("Cannot find file or invalid blacklist file! Please try again.")
                lprint(str(format_date) + ": INFO Cannot find file or invalid blacklist file: " + blacklist,
                       perform_logging)

            sanitize(filename, blacklist)

        elif user_input == '2':
            try:
                directory_path = input("Input name of directory:")
                lprint(str(format_date) + ": INFO Name of directory is " + directory_path, perform_logging)

            except Exception:
                print("Cannot find file or invalid blacklist file! Please try again.")
                lprint(str(format_date) + ": INFO Cannot find file or invalid blacklist file: ", perform_logging)

            list_of_files = getListOfFiles(directory_path)

            try:
                blacklist = input("Input name of blacklist:")
                print(blacklist)

            except Exception:
                print("Cannot find file or invalid blacklist file! Please try again.")

            for elem in list_of_files:
                sanitize(elem, blacklist)

            # Get the list of all files in directory tree at given path
        else:
            print("Invalid input. Please try again.")


def sanitize(filename, blacklist):
    # add very common filter here
    default_filter = ["example.com.sg,<REMOVED>",
                      "172\\.\\d+\\.\\d+\\.\\d+,<REMOVED IP>",
                      "192\\.\\d+\\.\\d+\\.\\d+,<REMOVED IP>",
                      "255\\.\\d+\\.\\d+\\.\\d+,<REMOVED IP>",
                      ]

    blacklist_array = []

    # Read from blacklist and store inside array
    with open(blacklist) as blf:
        for line in blf:
            if line[0] != '#' and line[0] != '|' and line[0] != "\n":
                blacklist_array.append(line)

    mime = mimetypes.guess_type(filename)

    print("Filename is " + filename + ", type is " + str(mime) + "...reading..")
    lprint(str(format_date) + ": INFO Filename is " + filename + ", type is " + str(mime) + "...reading..",
           perform_logging)

    if str(mime).find("text/plain") or str(mime).find("None, None") > -1:

        f_open = open(filename, "r")
        f_content = f_open.read()
        f_open.close()

        # filter using items in blacklist
        for item in blacklist_array:
            cols = item.split(',')
            ori = cols[0]
            replace = cols[1].replace("\n", "")

            matches = re.findall(ori, f_content)

            print("Pattern is :" + ori)
            print("Number of matches :" + str(len(matches)))
            if len(matches) > 0:
                print("Match occurrence :")
                print(matches)
                lprint("Match occurrence :", perform_logging)
                lprint(str(matches), perform_logging)

            f_content = re.sub(ori, replace, f_content)

        # filter using items in default filter
        for d_item in default_filter:
            d_cols = d_item.split(',')
            d_ori = d_cols[0]
            d_replace = d_cols[1].replace("\n", "")

            matches = re.findall(d_ori, f_content)

            print("Pattern is : \"" + d_ori + "\"")
            print("Number of matches :" + str(len(matches)))
            lprint("Pattern is :" + d_ori, perform_logging)
            lprint(str(format_date) + ": INFO Filename is " + filename + ", type is " + str(mime) + "...reading..",
                   perform_logging)

            if len(matches) > 0:
                print("Match occurrence :")
                print(matches)
                lprint("Match occurrence :", perform_logging)
                lprint(str(matches), perform_logging)

            f_content = re.sub(d_ori, d_replace, f_content)

        #       print(f_content)
        filename = filename.replace(".*", "")
        write_file = open(filename + "_" + format_date + ".txt", "w+")
        write_file.write(f_content)

    else:
        print("File is not readable..skipping...")


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def lprint(toprint, valid):
    if valid:
        log_file.write(toprint + "\n")


if __name__ == "__main__":
    main()
    lprint("Task finishing...ending program...", perform_logging)
#   log_file.close()

