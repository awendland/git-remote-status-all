from shared.repositories import add_repo
import shared.pretty as pretty

def run(repo_path):
    add_repo(repo_path)
    # Alert user about success
    pretty.tell_repo_added(repo_path)