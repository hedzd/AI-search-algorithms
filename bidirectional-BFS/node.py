class Node:
    def __init__(self, x, y):
        self.xyRobot = [int(x), int(y)]
        self.child = []
        self.parent = None
        self.action = None
        self.depth = None
        self.cost = None
        self.butterMove = None
        self.xyButters = None
        self.state = None
