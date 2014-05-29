#! /usr/bin/env python

# Used for easily checking the remote status of local repos
# Best if local repos use SSH for connection
#
# Add repos to check in the 'repos' file in the same directory as this script.
# Execute 
#   find /home/awendland/bigdrive/coding_projects/projects/ -name .git -type d > repos
# to easily generate the 'repos' file
#
# Influenced by http://stackoverflow.com/questions/5143795/how-can-i-check-in-a-bash-script-if-my-local-git-repo-has-changes

from subprocess import call, check_output, CalledProcessError
import os
import sys

# Open dev\null io
devnull = open(os.devnull, 'w')
# Convenience function for running subprocess.call with all output piped to devnull
def callnull(arr):
    return call(arr, stdout=devnull, stderr=devnull)

# Convenience function for calling print w/o inserting a newline at the end    
def printn(s):
    print s,

# Class holding console color codes
class c:
    H = '\033[95m'  # HEADER
    LG = '\033[37m'  # LGRAY
    B = '\033[94m'  # OK/BLUE
    G = '\033[92m'  # OK/GREEN
    W = '\033[93m'  # WARNING/YELLOW
    F = '\033[91m'  # FAIL/RED
    E = '\033[0m'   # ENDC/RESET

# Apply a console color to a string    
def colr(s, cl):
    return cl + s + c.E;

# Calculate the longest string in a list
def get_max_len(strings):
    max_len = 0
    for s in strings:
        if len(s) > max_len:
            max_len = len(s)
    return max_len

# Standard for printing repo path
# Prints last three path elements, separated by os.sep
def pretty_repo(path):
    return os.sep.join(path.split(os.sep)[-3:])

def execute():
    # Print a newline
    print("")
    # Get repos file from script dir
    repos_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + "repos"
    # Check if repos file exists
    if (os.path.isfile(repos_path)):
        # Read git repo paths from repos file
        repo_paths = [line.strip() for line in open(repos_path)]
        # Print number of repos
        print(" " + str(len(repo_paths)) + " git repositories")
        # Print a dividing line
        print(" " + "-" * 40)
        # Get max length of repo paths and + 2 for padding
        max_repo_len = get_max_len([pretty_repo(r) for r in repo_paths]) + 2
        # Loop over git repos
        for repo in repo_paths:
            # Print repo name
            printn(" " + colr(pretty_repo(repo).ljust(max_repo_len, " "), c.LG))
            # Check if repo is a valid directory
            if os.path.isdir(repo):
                # Change working directory to git repo
                os.chdir(repo)
                # Check if directory is a git repo
                if callnull(["git", "status"]) == 0:
                    # Run git fetch to update remote status
                    callnull(["git", "fetch"])
                    try:
                        # Get current branch
                        cur_branch = check_output(["git","rev-parse","--abbrev-ref","HEAD"], stderr=devnull).strip()
                        try:
                            # Check if there are outstanding commits
                            if int(check_output(["git","rev-list","HEAD...origin/" + cur_branch,"--ignore-submodules","--count"], stderr=devnull)) > 0:
                                printn("[ " + colr("NEEDS-SYNC", c.W) + " ]")
                            # No commits to be pushed
                            else:
                                printn("[ " + colr("    OK    ", c.G) + " ]")
                        # Handle rev-list errors
                        # Most likely their is no 'origin' set
                        except CalledProcessError, e:
                                printn("[ " + colr("MIS-ORIGIN", c.F) + " ]")
                    # Handle rev-parse errors
                    # Repo is mostly likely new with 0 commits and thus no HEAD
                    except CalledProcessError, e:
                            printn("[ " + colr("FRESH-REPO", c.W) + " ]")
                # Not a git repo
                else:
                    # Print as error
                    printn("[ " + colr("NOT-A-REPO", c.F) + " ]")
            # Not a valid directory
            else:
                # Print as error
                printn("[ " + colr("NOT-A-DIR ", c.F) + " ]")
            # Print a newline
            print("")
    # If repos file doesn't exist
    else:
        # Print missing repos error
        print("No 'repos' file found at '" + path + "'")
    # Print a newline
    print("")

if __name__ == '__main__':
    try:
        # Execute main functionality
        execute()
    # Gracefully handle keyboard interrups
    except KeyboardInterrupt:
        print("")
        sys.exit();
