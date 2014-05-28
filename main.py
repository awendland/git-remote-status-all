# Used for easily checking the remote status of local repos
# Best if local repos use SSH for connection
#
# Add repos to check in the 'repos' file in the same directory as this script.
# Execute 
#   find /home/awendland/bigdrive/coding_projects/projects/ -name .git -type d > repos
# to easily generate the 'repos' file
#
# Influenced by http://stackoverflow.com/questions/5143795/how-can-i-check-in-a-bash-script-if-my-local-git-repo-has-changes

from subprocess import call, check_output, CalledProcessError, STDOUT
import os
import sys

# Open dev null io
devnull = open(os.devnull, 'w')
def callnull(arr):
    return call(arr, stdout=devnull, stderr=devnull)
    
def printn(s):
    print s,

class c:
    H = '\033[95m'  # HEADER
    B = '\033[94m'  # OKBLUE
    G = '\033[92m'  # OKGREEN
    W = '\033[93m'  # WARNING
    F = '\033[91m'  # FAIL
    E = '\033[0m'   # ENDC
    
def colr(s, cl):
    return cl + s + c.E;
    
def get_max_path_len(paths):
    maxlen = 0
    for path in paths:
        parts = path.split(os.sep)
        pathlen = len(os.sep.join(parts[-3:]))
        if pathlen > maxlen:
            maxlen = pathlen
    return maxlen

def pretty_repo(path):
    return os.sep.join(path.split(os.sep)[-3:])

def execute():
    # Print a newline
    print("")
    # Get repos file from script dir
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep + "repos"
    # Check if repos file exists
    if (os.path.isfile(path)):
        # Read git repo paths from repos file
        repo_paths = [line.strip() for line in open(path)]
        # Print number of repos
        print(" " + str(len(repo_paths)) + " git repositories")
        print(" " + "-" * 40)
        # Get maxlen of repo paths
        max_repo_len = get_max_path_len(repo_paths) + 2
        # Loop over git repos
        for repo in repo_paths:
            # Print repo name
            printn(" " + pretty_repo(repo).ljust(max_repo_len, " "))
            if os.path.isdir(repo):
                # Change working directory to git repo
                os.chdir(repo)
                # Check if git repo
                if callnull(["git", "status"]) == 0:
                    # Run git fetch to update remote status
                    callnull(["git", "fetch"])
                    try:
                        # Get current branch
                        cur_branch = check_output(["git","rev-parse","--abbrev-ref","HEAD"], stderr=devnull).strip()
                        try:
                            # Check if there are commits to be pushed
                            if int(check_output(["git","rev-list","HEAD...origin/" + cur_branch,"--ignore-submodules","--count"], stderr=devnull)) > 0:
                                printn("[ " + colr("NEEDS-SYNC", c.W) + " ]")
                            # No commits to be pushed
                            else:
                                printn("[ " + colr("UP-TO-DATE", c.G) + " ]")
                        # Handle rev-list errors
                        except CalledProcessError, e:
                                printn("[ " + colr("NO-REMOTE ", c.F) + " ]")
                    # Repo is mostly likely new with 0 commits
                    except CalledProcessError, e:
                            printn("[ " + colr("FRESH-REPO", c.W) + " ]")
                # Not a git repo
                else:
                    # Print as error
                    printn("[ " + colr("NOT-A-REPO", c.F) + " ]")
                # Print newline
            else:
                # Print as error
                printn("[ " + colr("NOT-A-DIR ", c.F) + " ]")
            print("")
    # If config doesn't exist
    else:
        # Print missing config error
        print("No config file found at '" + path + "'")
    # Print a newline
    print("")

if __name__ == '__main__':
    try:
        execute()
    except KeyboardInterrupt:
        print("")
        sys.exit();
