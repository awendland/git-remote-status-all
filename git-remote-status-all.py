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
import argparse

from shared.exceptions import Shutdown

# Exit function
def exit(msg="", code=0):
    if msg is not None:
        print(msg)
    print("")
    sys.exit(code)

def execute():
    # Setup Arguments Parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='(status, list, add, remove)', dest='action')
    # Add status action
    parser_status = subparsers.add_parser('status', help='show the sync status of each repo')
    # Add list action
    parser_list = subparsers.add_parser('list', help='list the tracked repos')
    # Add add action
    parser_add = subparsers.add_parser('add', help='add a folder to the list of repos')
    parser_add.add_argument("--walk", action="store_const", dest="walk_sub_dirs", const=True, default=False, help="walk sub directories to look for .git folders")
    parser_add.add_argument('dir', nargs='?', default=os.getcwd(), help='repo directory to add. defaults to current dir.')
    # Add remove action
    parser_remove = subparsers.add_parser('remove', help='remove a repo from the tracked list')
    parser_remove.add_argument('dir', nargs='?', default=os.getcwd(), help='repo directory to remove. defaults to current dir.')
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands               
    if args.action == "status":
        print("Running bulk status check")
        import actions.status as status
        status.run()
    elif args.action == "list":
        print("Listing tracked repos")
    elif args.action == "add":
        print("Adding new repo to tracking")
        import actions.add as add
        add.run(args.repos, args.dir, args.walk_sub_dirs)
    elif args.action == "remove":
        print("Removing repo from tracking")
        import actions.remove as remove
        remove.run(args.repos, args.dir)
    else:
        parser.print_help()
    print("")

if __name__ == '__main__':
    try:
        # Execute main functionality
        execute()
    # Gracefully handle keyboard interrups, as well as program requests for exit
    except (KeyboardInterrupt, Shutdown):
        exit()
