# Convenience function for printing a newline  
def print_new_line():
    print("")

# Convenience function for calling print w/o inserting a newline at the end    
def printn(s):
    print s,

# Print a dividing line
def print_dl():
    print(" " + "-" * 40)

# Class holding console color codes
class c:
    BACK_LN = '\033[F' # Back to prev line
    H = '\033[95m'  # HEADER
    LG = '\033[37m' # LGRAY
    B = '\033[94m'  # OK/BLUE
    G = '\033[92m'  # OK/GREEN
    W = '\033[93m'  # WARNING/YELLOW
    F = '\033[91m'  # FAIL/RED
    E = '\033[0m'   # ENDC/RESET

# Apply a console code to a string    
def ccode(s, cl):
    return cl + s + c.E;

# Calculate the longest string in a list
def get_max_len(strings):
    max_len = 0
    for s in strings:
        if len(s) > max_len:
            max_len = len(s)
    return max_len
        
###############
#   Dynamic   #
###############

max_repo_len = 0
# Get max length of repo paths and + 2 for padding
def calc_max_repo_len(repos):
    global max_repo_len
    max_repo_len = get_max_len([r.pretty_path() for r in repos]) + 2

count = 0
def loading(msg = ""):
    sym = ""
    global count
    mod = count % 4
    if mod == 0:
        sym = "|"
    elif mod == 1:
        sym = "/"
    elif mod == 2:
        sym = "-"
    elif mod == 3:
        sym = "\\"
    count += 1
    print(c.BACK_LN + sym + msg + c.E)

###############
# Repo Status #
###############

# Print repo name
def tellp_repo_name(repo):
    printn(" " + ccode(repo.pretty_path().ljust(max_repo_len, " "), c.LG))

# Print repo name
def tellp_repo_status(status, color):
    pad = ( 10 - len(status) ) / 2
    printn("[ " + ccode(" " * pad + status + " " * pad, color) + " ]")
    
###############
#   Add Repo  #
###############

# Tell user how many folders have been searched
def tell_folder_search_count(num):
    # TODO: clear current line and reprint
    print(ccode(" " + str(num) + " folders searched", c.LG))

# Tell user that the repo path was added
def tell_repo_added(repo):
    print(ccode(" Repo '", c.LG) + ccode(repo, c.G) + ccode("' added.", c.LG))


# Tell user that the repo path was added
def tell_repo_already_tracked(repo):
    print(ccode(" Repo '", c.LG) + ccode(repo.get_path(), c.B) + ccode("' is already tracked.", c.LG))

###############
# Remove Repo #
###############

# Tell user that the repo path was added
def tell_repo_removed(repo):
    print(ccode(" Repo '" + repo + "' removed.", c.LG))

###############
#  Responses  #
###############

# Tell user that the repos file is missing
def tell_repos_file_missing(repos_path):
    print("No 'repos' file found at '" + repos_path + "'")
    print("")

# Tell user the number of repos
def tell_num_of_repos(repos):
    print(" " + str(len(repos)) + " git repositories")

###############
# Interactive #
###############

# Test if user input is a 'yes' response
y_resp_dict = ['y', 'yes', 'yeah', 'ya']
def is_yes(resp):
    return resp.lower() in y_resp_dict

# Prompts user for Y/n if repos file should be created
def ask_create_repos_file():
    y_or_n = raw_input("Create a blank repos file? (Y/n): ")
    return is_yes(y_or_n)