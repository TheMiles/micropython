

# reads in a a file expecting each line to be in
#  key = value
# format.
# returns a dictionary
def readConfig(filename):
    with open(filename, 'r') as infile:
        config = { e[0].strip(): e[1].strip() for e in [ l.split('=') for l in infile ] }
    return config
