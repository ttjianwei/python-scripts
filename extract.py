import re
import os

# Author: Huang Jian Wei
# Date Created: 08/11/2019
# Date Last Modified: 11/11/2019

result_file = open("result.txt", "a+")

def main():

    while 1:
        user_input = input("(1) for single file, (2) for directory,"
                           "(3) to exit:""\n1.) File\n2.) Directory\n3.) Exit\n")
		
        if user_input == '3':
            print("Exiting program...")
            break
		        # Relative path
        elif user_input == '1':
            try:
                filename = input("Input name of file:")
                print(filename)
            except Exception:
                print("Cannot find file or invalid file! Please try again.")
		
        elif user_input == '2':
           
            directory_path = input("Input name of directory:")
				
            list_of_files = getListOfFiles(directory_path)

            for elem in list_of_files:
                sconcat(elem)

            # Get the list of all files in directory tree at given path
        else:
            print("Invalid input. Please try again.")

def sconcat(filename):

    match_pattern = re.compile(r'(<Insert your pattern here>)')
    result_arr =[]
    with open(filename) as blf:
        for line in blf:
            if(match_pattern.search(line)):
                result_arr.append(line)
				
    for arr in result_arr:
        result_file.write(arr+"\n")
		 
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
		 
if __name__ == "__main__":
    main()
#   log_file.close()
