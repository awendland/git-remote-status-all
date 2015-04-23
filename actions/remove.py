from shared.repositories import remove_repo
import shared.pretty as pretty

def run(repos_path, rem_repo_path):
    remove_repo(rem_repo_path, repos_path)
    # Alert user about success
    pretty.tell_repo_removed(rem_repo_path)