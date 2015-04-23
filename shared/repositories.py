import os
from os.path import expanduser

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
        repos_path = expanduser("~") + os.sep + ".git-remote-status-repos"
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
    # Get current repos
    cur_repos = get_repos(repos_path)
    # Check if repo already tracked
    for repo in cur_repos:
        if os.path.abspath(repo.get_path()) == os.path.abspath(path):
            pretty.tell_repo_already_tracked(repo)
            return False
    # Add new repo
    cur_repos.append(Repo(path))
    # Open repos file
    f = open(get_repos_file(repos_path), 'w+')
    # Add repo to file
    f.write("\n".join([repo.get_path() for repo in cur_repos]))
    # Close repos file
    f.close()
    return True

def remove_repo(path, repos_path = None):
    # Print a newline
    pretty.print_new_line()
    # Get repos path if not supplied
    if not repos_path:
        repos_path = get_repos_file(repos_path)
    # Open repos file
    f = open(repos_path, 'w+')
    # Var for holding new repo list
    cleaned_repos = []
    # Load file to string for manipulation
    for repo in f:
        if os.path.abspath(repo) != os.path.abspath(path):
            cleaned_repos.append(repo)
    # Add repo to file
    f.write("\n".join(cleaned_repos))
    # Close repos file
    f.close()