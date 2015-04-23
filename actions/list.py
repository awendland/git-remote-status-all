from shared.repositories import get_repos
import shared.pretty as pretty

def run(repo_path):
    repos = get_repos(repo_path)
    # Header for num of repos
    pretty.tell_num_of_repos(repos)
    pretty.print_dl()
    # List the repo paths
    for repo in repos:
    	pretty.tellp_repo_name(repo)
        # Print a newline
        pretty.print_new_line()