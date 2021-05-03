import queue
from node import Node


class BidirectionalBFS:
    def __init__(self, tableInfo):
        self.tableInfo = tableInfo
        self.path1 = []
        self.path2 = []
        self.path = []
        self.cost = 0
        self.forwardFringe = queue.Queue()
        self.forwardExplored = []
        self.backwardFringe = queue.Queue()
        self.backwardExplored = []
        self.forwardLastNode = None
        self.backwardLastNode = None

    def searchAlgorithm(self):
        initialNode = self.createInitialNode()
        finalNode = self.createFinalNode()
        if finalNode is None:
            return False
        if initialNode.state == finalNode.state:
            self.forwardLastNode = initialNode
            return True

        self.forwardFringe.put(initialNode)
        self.backwardFringe.put(finalNode)

        while True:
            # FORWARD SEARCH
            if self.forwardFringe.empty():
                return False
            currNode = self.forwardFringe.get()
            xyList, action, butterMove = self.successor(currNode)
            # print("dequeue node:", node.state)
            # print("current state: ", state)
            # print("current state xyButt: ", node.xyButters)
            # print("succ: ",successor)
            # print("action: ", action)
            # print("buttMove: ", butterMove)
            for i, xy in enumerate(xyList):
                newNode = self.createNode(xy[0], xy[1], currNode, action[i], butterMove[i], "forward")
                if self.checkExplored(newNode, "forward"):
                    continue
                isGoal, backwardLastNode = self.checkGoal(newNode, "forward")
                if isGoal:
                    self.forwardLastNode = newNode
                    self.backwardLastNode = backwardLastNode
                    return True

                # print("enqueue node:", newNode.state)
                self.forwardFringe.put(newNode)
            self.forwardExplored.append(currNode)
            # print("explored: ", end="")
            # for exp in self.forwardExplored:
            #     print(exp.state, end=", ")
            # print()

            # BACKWARD SEARCH
            if self.forwardFringe.empty():
                return False
            currNode = self.backwardFringe.get()
            xyList, action, butterMove = self.predecessor(currNode)
            for i, xy in enumerate(xyList):
                newNode = self.createNode(xy[0], xy[1], currNode, action[i], butterMove[i], "backward")
                if self.checkExplored(newNode, "backward"):
                    continue
                isGoal, forwardLastNode = self.checkGoal(newNode, "backward")
                if isGoal:
                    self.forwardLastNode = forwardLastNode
                    self.backwardLastNode = newNode
                    return True
                self.backwardFringe.put(newNode)
            self.backwardExplored.append(currNode)
            # print("back explored: ", end="")
            # for exp in self.backwardExplored:
            #     print(exp.state, end=", ")
            # print()

    def checkExplored(self, newNode, direction):
        newXYRobot = newNode.xyRobot
        newXYButters = newNode.xyButters
        if direction == "forward":
            for exNode in self.forwardExplored:
                if newXYRobot == exNode.xyRobot:
                    z = [tuple(y) for y in newXYButters]
                    x = [tuple(y) for y in exNode.xyButters]
                    return set(x) == set(z)
        else:
            for exNode in self.backwardExplored:
                if newXYRobot == exNode.xyRobot:
                    z = [tuple(y) for y in newXYButters]
                    x = [tuple(y) for y in exNode.xyButters]
                    return set(x) == set(z)

    def createNode(self, x, y, parentNode, action, butterMove, direction):
        node = Node(x, y)
        node.cost = int(self.tableInfo.matrix[y][x])
        node.depth = parentNode.depth + 1
        node.parent = parentNode
        node.action = action
        node.butterMove = butterMove  # TODO
        node.xyButters = list(parentNode.xyButters)
        if butterMove:
            if direction == "forward":
                butterIndex = parentNode.xyButters.index([x, y])
                if action == 'L':
                    node.xyButters[butterIndex] = [x - 1, y]
                elif action == 'R':
                    node.xyButters[butterIndex] = [x + 1, y]
                elif action == 'U':
                    node.xyButters[butterIndex] = [x, y - 1]
                elif action == 'D':
                    node.xyButters[butterIndex] = [x, y + 1]
            elif direction == "backward":  # TODO: refactor
                if action == 'L':
                    butterIndex = parentNode.xyButters.index([x - 2, y])
                    node.xyButters[butterIndex] = [x - 1, y]
                elif action == 'R':
                    butterIndex = parentNode.xyButters.index([x + 2, y])
                    node.xyButters[butterIndex] = [x + 1, y]
                elif action == 'U':
                    butterIndex = parentNode.xyButters.index([x, y - 2])
                    node.xyButters[butterIndex] = [x, y - 1]
                elif action == 'D':
                    butterIndex = parentNode.xyButters.index([x, y + 2])
                    node.xyButters[butterIndex] = [x, y + 1]
        node.state = [node.xyRobot, node.xyButters]
        # print("new node: state:", node.state, "parent state: ", parentNode.state,"parent buttLoc: ", parentNode.xyButters, "action: ", node.action, "buttLoc: ", node.xyButters)
        return node

    def checkGoal(self, node, direction):
        if direction == "forward":
            for otherNode in self.backwardExplored:
                if node.xyRobot == otherNode.xyRobot:
                    z = [tuple(y) for y in node.xyButters]
                    x = [tuple(y) for y in otherNode.xyButters]
                    if set(x) == set(z):
                        return True, otherNode
        else:
            for otherNode in self.forwardExplored:
                if node.xyRobot == otherNode.xyRobot:
                    z = [tuple(y) for y in node.xyButters]
                    x = [tuple(y) for y in otherNode.xyButters]
                    if set(x) == set(z):
                        return True, otherNode
        return False, None

    def predecessor(self, node):
        x = node.xyRobot[0]
        y = node.xyRobot[1]
        xyList = []
        actionList = []
        butterMove = []
        if x + 1 < self.tableInfo.column and [x + 1, y] not in node.xyButters:
            if self.checkRobotCell(x + 1, y):
                if [x - 1, y] in node.xyButters:
                    butterMove.append(True)
                    xyList.append([x + 1, y])
                    actionList.append('L')
                butterMove.append(False)
                xyList.append([x + 1, y])
                actionList.append('L')
        if x - 1 >= 0 and [x - 1, y] not in node.xyButters:
            if self.checkRobotCell(x - 1, y):
                if [x + 1, y] in node.xyButters:
                    butterMove.append(True)
                    xyList.append([x - 1, y])
                    actionList.append('R')
                butterMove.append(False)
                xyList.append([x - 1, y])
                actionList.append('R')
        if y + 1 < self.tableInfo.row and [x, y + 1] not in node.xyButters:
            if self.checkRobotCell(x, y + 1):
                if [x, y - 1] in node.xyButters:
                    butterMove.append(True)
                    xyList.append([x, y + 1])
                    actionList.append('U')
                butterMove.append(False)
                xyList.append([x, y + 1])
                actionList.append('U')
        if y - 1 >= 0 and [x, y - 1] not in node.xyButters:
            if self.checkRobotCell(x, y - 1):
                if [x, y + 1] in node.xyButters:
                    butterMove.append(True)
                    xyList.append([x, y - 1])
                    actionList.append('D')
                butterMove.append(False)
                xyList.append([x, y - 1])
                actionList.append('D')
        return xyList, actionList, butterMove

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

    def createInitialNode(self):
        x = self.tableInfo.xyRobot[0]
        y = self.tableInfo.xyRobot[1]
        node = Node(x, y)
        node.cost = int(self.tableInfo.matrix[y][x])
        node.depth = 1
        node.xyButters = self.tableInfo.xyButters
        node.state = [node.xyRobot, node.xyButters]
        return node

    def createFinalNode(self):
        node = None
        xyButters = list(self.tableInfo.xyPersons)
        for xy in self.tableInfo.xyPersons:
            x = xy[0]
            y = xy[1]
            if x + 1 < self.tableInfo.column:
                if self.checkRobotCell(x + 1, y):
                    node = Node(x + 1, y)
                    node.action = 'L'
                    break
            if x - 1 >= 0:
                if self.checkRobotCell(x - 1, y):
                    node = Node(x - 1, y)
                    node.action = 'R'
                    break
            if y + 1 < self.tableInfo.row:
                if self.checkRobotCell(x, y + 1):
                    node = Node(x, y + 1)
                    node.action = 'U'
                    break
            if y - 1 >= 0:
                if self.checkRobotCell(x, y - 1):
                    node = Node(x, y - 1)
                    node.action = 'D'
                    break
        if node is not None:
            node.xyButters = xyButters
            node.cost = int(self.tableInfo.matrix[node.xyRobot[1]][node.xyRobot[0]])
            node.depth = 1
            node.state = [node.xyRobot, node.xyButters]
        return node

    def calcPathAndCost(self):
        res = self.searchAlgorithm()
        if not res:
            print("can't pass the butter")
        else:
            # print("f: ",self.forwardLastNode.state)
            # print("f: ", self.forwardLastNode.parent.state)
            # print("f: ", self.forwardLastNode.parent.parent.state)
            # print(self.backwardLastNode.state)
            # print(self.backwardLastNode.parent.state)
            # print(self.backwardLastNode.parent.parent.state)
            # print(self.backwardLastNode.parent.parent.parent.state)
            node = self.forwardLastNode
            while node.parent is not None:
                self.path1.append(node.action)
                self.cost += node.cost
                node = node.parent
            self.cost += node.cost
            self.path1 = self.path1[::-1]
            node = self.backwardLastNode
            node.cost = 0
            while node.parent is not None:
                self.path2.append(node.action)
                self.cost += node.cost
                node = node.parent
            self.cost += node.cost
            self.path = self.path1 + self.path2
