import sys

# calculate distance between 2 points using xy coordinated
def dist(x1, x2, y1, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2)**0.5

print(dist(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))



