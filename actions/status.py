import os
from subprocess import call, check_output, CalledProcessError

import shared.pretty as pretty
from shared.repositories import Repo, get_repos
from shared.oscmd import devnull, callnull

def run(repos_path):
    repos = get_repos(repos_path)
    pretty.tell_num_of_repos(repos)
    pretty.print_dl()
    pretty.calc_max_repo_len(repos)
    # Loop over git repos
    for repo in repos:
        # Print repo name
        pretty.tellp_repo_name(repo)
        # Check if repo is a valid directory
        if repo.does_dir_exist():
            # Change working directory to git repo
            os.chdir(repo.get_path())
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
                            pretty.tellp_repo_status("NEEDS-SYNC", pretty.c.W)
                        # No commits to be pushed
                        else:
                            pretty.tellp_repo_status("OK", pretty.c.G)
                            # Handle rev-list errors
                    # Most likely their is no 'origin' set
                    except CalledProcessError, e:
                        pretty.tellp_repo_status("MIS-ORIGIN", pretty.c.F)
                        # Handle rev-parse errors
                # Repo is mostly likely new with 0 commits and thus no HEAD
                except CalledProcessError, e:
                    pretty.tellp_repo_status("FRESH-REPO", pretty.c.W)
            # Not a git repo
            else:
                # Print as error
                pretty.tellp_repo_status("NOT-A-REPO", pretty.c.F)
        # Not a valid directory
        else:
            # Print as error
            pretty.tellp_repo_status("NOT-A-DIR", pretty.c.F)
        # Print a newline
        pretty.print_new_line()