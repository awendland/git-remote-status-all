import os
from subprocess import call, check_output, CalledProcessError

# Open dev\null io
devnull = open(os.devnull, 'w')
# Convenience function for running subprocess.call with all output piped to devnull
def callnull(arr):
    return call(arr, stdout=devnull, stderr=devnull)