from node import Node


def sortingFunc(node):
    return node.evaluation


class AStar:
    def __init__(self, tableInfo):
        self.tableInfo = tableInfo
        self.path = []
        self.cost = 0
        self.fringe = []
        self.explored = []
        self.lastNode = None

    def searchAlgorithm(self):
        initialNode = self.createInitialNode()
        self.fringe.append(initialNode)
        while True:
            if not self.fringe:
                return False

            self.fringe.sort(key=sortingFunc)
            currNode = self.fringe.pop(0)
            isGoal = self.checkGoal(currNode)
            if isGoal:
                self.lastNode = currNode
                return True
            xyList, action, butterMove = self.successor(currNode)
            print("current node xyRobot:", currNode.xyRobot)
            print("current state xyButt: ", currNode.xyButters)
            print("current state eval: ", currNode.evaluation)
            # print("xy list: ", xyList)
            # print("action: ", action)
            # print("buttMove: ", butterMove)
            for i, xy in enumerate(xyList):
                newNode = self.createNode(xy[0], xy[1], currNode, action[i], butterMove[i])
                if self.checkExplored(newNode):
                    continue
                self.fringe.append(newNode)
            self.explored.append(currNode)
            # print("explored:")
            # for e in self.explored:
            #     print(e.state)
            # print("------")

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
        self.calcNodeEvaluation(node)
        return node

    def calcNodeEvaluation(self, node):
        h = 0
        minDistFromButter = 5000
        for xy in node.xyButters:
            dist = (abs(xy[1] - node.xyRobot[1]) + abs(xy[0] - node.xyRobot[0]))
            if dist < minDistFromButter:
                minDistFromButter = dist
                xyMin = xy

        minDistFromPerson = 5000
        for xyP in self.tableInfo.xyPersons:
            dist = (abs(xy[1] - xyP[1]) + abs(xy[0] - xyP[0]))
            if dist < minDistFromPerson:
                minDistFromPerson = dist
        h += minDistFromPerson

        node.evaluation = h + node.cost - x
        #+ node.cost

    def checkExplored(self, newNode):
        newXYRobot = newNode.xyRobot
        newXYButters = newNode.xyButters

        for exNode in self.explored:
            if newXYRobot == exNode.xyRobot:
                z = [tuple(y) for y in newXYButters]
                x = [tuple(y) for y in exNode.xyButters]
                if set(x) == set(z):
                    return True
        return False

    def successor(self, node):
        x = node.xyRobot[0]
        y = node.xyRobot[1]
        xyList = []
        actionList = []
        butterMove = []
        if x + 1 < self.tableInfo.column:
            if self.checkRobotCell(x + 1, y):
                if [x + 1, y] in node.xyButters:
                    if self.checkButterCell(x + 1, y, 'R'):
                        butterMove.append(True)
                        xyList.append([x + 1, y])
                        actionList.append('R')
                else:
                    butterMove.append(False)
                    xyList.append([x + 1, y])
                    actionList.append('R')

        if x - 1 >= 0:
            if self.checkRobotCell(x - 1, y):
                if [x - 1, y] in node.xyButters:
                    if self.checkButterCell(x - 1, y, 'L'):
                        butterMove.append(True)
                        xyList.append([x - 1, y])
                        actionList.append('L')
                else:
                    butterMove.append(False)
                    xyList.append([x - 1, y])
                    actionList.append('L')

        if y + 1 < self.tableInfo.row:
            if self.checkRobotCell(x, y + 1):
                if [x, y + 1] in node.xyButters:
                    if self.checkButterCell(x, y + 1, 'D'):
                        butterMove.append(True)
                        xyList.append([x, y + 1])
                        actionList.append('D')
                else:
                    butterMove.append(False)
                    xyList.append([x, y + 1])
                    actionList.append('D')
        if y - 1 >= 0:
            if self.checkRobotCell(x, y - 1):
                if [x, y - 1] in node.xyButters:
                    if self.checkButterCell(x, y - 1, 'U'):
                        butterMove.append(True)
                        xyList.append([x, y - 1])
                        actionList.append('U')
                else:
                    butterMove.append(False)
                    xyList.append([x, y - 1])
                    actionList.append('U')
        return xyList, actionList, butterMove

    def checkRobotCell(self, x, y):
        # check forbidden cell
        if self.tableInfo.matrix[y][x] == 'x':
            return False
        # check person cell
        for xyP in self.tableInfo.xyPersons:
            if xyP == [x, y]:
                return False
        return True

    def checkButterCell(self, x, y, action):
        if action == 'R':
            if x + 1 >= self.tableInfo.column or self.tableInfo.matrix[y][x + 1] == 'x':
                return False
        if action == 'L':
            if x - 1 < 0 or self.tableInfo.matrix[y][x - 1] == 'x':
                return False
        if action == 'U':
            if y - 1 < 0 or self.tableInfo.matrix[y - 1][x] == 'x':
                return False
        if action == 'D':
            if y + 1 >= self.tableInfo.row or self.tableInfo.matrix[y + 1][x] == 'x':
                return False
        return True

    def createNode(self, x, y, parentNode, action, butterMove):
        node = Node(x, y)
        node.cost = int(self.tableInfo.matrix[y][x])
        node.depth = parentNode.depth + 1
        node.parent = parentNode
        node.action = action
        node.butterMove = butterMove  # TODO
        node.xyButters = list(parentNode.xyButters)
        if butterMove:
            butterIndex = parentNode.xyButters.index([x, y])
            if action == 'L':
                node.xyButters[butterIndex] = [x - 1, y]
            elif action == 'R':
                node.xyButters[butterIndex] = [x + 1, y]
            elif action == 'U':
                node.xyButters[butterIndex] = [x, y - 1]
            elif action == 'D':
                node.xyButters[butterIndex] = [x, y + 1]
        node.state = [node.xyRobot, node.xyButters]
        # added:
        self.calcNodeEvaluation(node)
        # print("new node: state:", node.state, "parent state: ", parentNode.state,"parent buttLoc: ", parentNode.xyButters, "action: ", node.action, "buttLoc: ", node.xyButters)
        return node

    def calcPathAndCost(self):
        res = self.searchAlgorithm()
        if not res:
            print("can't pass the butter")
        else:
            node = self.lastNode
            while node.parent is not None:
                self.path.append(node.action)
                self.cost += node.cost
                node = node.parent
            self.cost += node.cost
            self.path = self.path[::-1]
