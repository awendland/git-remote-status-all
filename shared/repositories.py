import os

import pretty as pretty
from exceptions import Shutdown

class Repo:
    def __init__(self, serialized):
        self.path = serialized.strip()
    
    # Returns repo path string
    def get_path(self):
        return self.path
    
    # Standard for printing repo path
    # Prints last three path elements, separated by os.sep
    def pretty_path(self):
        return os.sep.join(self.get_path().split(os.sep)[-3:])
    
    # Is this repo a valid directory?
    def does_dir_exist(self):
        return os.path.isdir(self.get_path())
    
def get_repos_file(repos_path = None):
    # Set default repos_path if none is supplied
    if repos_path is None:
        repos_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + "repos"
    # Get repos file from script dirdef load_repos(repos_path):
    repos_path = os.sep.join(os.path.dirname((os.path.abspath(__file__))).split(os.sep)[:-1]) + os.sep + "repos"
    # Check if repos file exists
    if (os.path.isfile(repos_path)):
        return repos_path
    # If repos file doesn't exist
    else:
        pretty.tell_repos_file_missing(repos_path)
        if pretty.ask_create_repos_file():
            open(repos_path, 'w+')
            return repos_path
        raise Shutdown()

def get_repos(repos_path = None):
    # Print a newline
    pretty.print_new_line()
    # Get repos path
    repos_path = get_repos_file(repos_path)
    # Read git repo paths from repos file
    repos = [Repo(line) for line in open(repos_path)]
    return repos
        
def add_repo(path, repos_path = None):
    # Print a newline
    pretty.print_new_line()
    # Get repos path
    repos_path = get_repos_file(repos_path)
    # Open repos file
    f = open(repos_path, 'a')
    # Add repo to file
    f.write(path)
    # Close repos file
    f.close()