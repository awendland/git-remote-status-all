from shared.repositories import add_repo
import shared.pretty as pretty

def run(repos_path, new_repo_path, walk_sub_dirs):
	new_repo_paths = []
	if walk_sub_dirs:
		print("\n")
		import os
		count = 0
		for root, dirs, files in os.walk(u"."):
			count += 1
			if count % 1000 == 0:
				pretty.loading(" searching for repos")
			if os.path.basename(root) == ".git" and ".git-remote-status-all-ignore" not in files:
				parent = os.sep.join(root.split(os.sep)[:-1])
				new_repo_paths.append(os.path.abspath(parent))
	else:
		new_repo_paths.append(new_repo_path)
	# Loop over repo paths to add
	for new_path in new_repo_paths:
		# Add new_path
	    if add_repo(new_path, repos_path):
		    # Alert user about adding this path
		    pretty.tell_repo_added(new_path)