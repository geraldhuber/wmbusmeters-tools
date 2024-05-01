import sys


# Helper method to print to stderr
def eprint(*args, **kwargs): # TODO: Add docstrings
    # need to import sys first
    print(*args, file=sys.stderr, **kwargs)