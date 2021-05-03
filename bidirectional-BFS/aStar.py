from node import Node


class AStar:
    def __init__(self, tableInfo):
        self.tableInfo = tableInfo
        self.path = []
        self.cost = 0
        self.fringe = []
        self.explored = []

    def searchAlgorithm(self):
        initialNode = self.createInitialNode()
        self.fringe.append(initialNode)
        while True:
            if self.fringe.empty():
                return False
            # TODO

    def checkGoal(self, node):
        z = [tuple(y) for y in self.tableInfo.xyPersons]
        x = [tuple(y) for y in node.xyButters]
        return set(x) == set(z)

    def createInitialNode(self):
        x = self.tableInfo.xyRobot[0]
        y = self.tableInfo.xyRobot[1]
        node = Node(x, y)
        node.cost = int(self.tableInfo.matrix[y][x])
        node.depth = 1
        node.xyButters = self.tableInfo.xyButters
        node.state = [node.xyRobot, node.xyButters]
        return node

    def checkExplored(self, newNode):
        newXYRobot = newNode.xyRobot
        newXYButters = newNode.xyButters

        for exNode in self.explored:
            if newXYRobot == exNode.xyRobot:
                z = [tuple(y) for y in newXYButters]
                x = [tuple(y) for y in exNode.xyButters]
                return set(x) == set(z)

    def successor(self, node):
        #TODO
        return None
