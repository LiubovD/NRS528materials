# 2. Push sys.argv to the limit
# Construct a rudimentary Python script that takes a series of inputs as a command from a bat file, and does something to them. The rules:
#
# Minimum of three arguments to be used.
# You must do something interesting in 15 lines or less within the Python file.
# Print or file generated output should be produced.

import sys

# calculate distance between 2 points using xy coordinated
def dist(x1, x2, y1, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2)**0.5

print(dist(int(sys.argv[1]),int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])))



