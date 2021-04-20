import queue


class Table:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.matrix = []
        self.xyRobot = []
        self.xyButters = []
        self.xyPersons = []

    def parseInput(self):
        for i in range(self.row):
            self.matrix.append(input().split())
            for j in range(self.column):
                self.setLocations(i, j)

    def setLocations(self, i, j):
        if 'r' in self.matrix[i][j]:
            self.xyRobot.append(j)
            self.xyRobot.append(i)
            self.matrix[i][j] = self.matrix[i][j].replace('r', '')
        if 'b' in self.matrix[i][j]:
            self.xyButters.append([j, i])
            self.matrix[i][j] = self.matrix[i][j].replace('b', '')
        if 'p' in self.matrix[i][j]:
            self.xyPersons.append([j, i])
            self.matrix[i][j] = self.matrix[i][j].replace('p', '')


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


class ForwardBFS:
    def __init__(self, tableInfo):
        self.tableInfo = tableInfo
        self.path = []
        self.cost = 0
        self.fringe = queue.Queue()
        self.explored = []
        self.lastNode = None

    def searchAlgorithm(self):
        initialNode = self.createNode(self.tableInfo.xyRobot[0], self.tableInfo.xyRobot[1], None, None, None)
        if self.checkGoal(initialNode):
            self.lastNode = initialNode
            return True
        self.fringe.put(initialNode)
        while True:
            if self.fringe.empty():
                return False
            node = self.fringe.get()
            # print("dequeue node:", node.state)
            state = node.state
            xyList, action, butterMove = self.successor(node)
            # print("current state: ", state)
            # print("current state xyButt: ", node.xyButters)
            # print("succ: ",successor)
            # print("action: ", action)
            # print("buttMove: ", butterMove)
            for i, xy in enumerate(xyList):
                newNode = self.createNode(xy[0], xy[1], node, action[i], butterMove[i])
                if newNode.state in self.explored:
                    continue
                if self.checkGoal(newNode):
                    self.lastNode = newNode
                    return True

                # print("enqueue node:", newNode.state)
                self.fringe.put(newNode)
            self.explored.append(node.state)
            print("explored: ", self.explored)

    def createNode(self, x, y, parentNode, action, butterMove):
        node = Node(x, y)
        node.cost = int(self.tableInfo.matrix[y][x])
        if parentNode is None:
            node.depth = 1
            node.xyButters = self.tableInfo.xyButters
        else:
            node.depth = parentNode.depth + 1
            node.parent = parentNode
            node.action = action
            node.butterMove = butterMove
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
            # print("new node: state:", node.state, "parent state: ", parentNode.state,"parent buttLoc: ", parentNode.xyButters, "action: ", node.action, "buttLoc: ", node.xyButters)
        return node

    def checkGoal(self, node):
        for xyP in self.tableInfo.xyPersons:
            for xyB in node.xyButters:
                if xyP == xyB:
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
        if self.tableInfo.matrix[y][x] == 'x':
            return False
        # person
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
            if y + 1 >= self.tableInfo.column or self.tableInfo.matrix[y + 1][x] == 'x':
                return False
        return True

    def calcPathAndCost(self):
        res = self.searchAlgorithm()
        if not res:
            print("no path")
        else:
            node = self.lastNode
            while node.parent is not None:
                # print("node:", node.state)
                # print("add to path", node.action)
                print("loc butt: ", node.xyButters)
                self.path.append(node.action)
                self.cost += node.cost
                node = node.parent
            self.cost += node.cost
        self.path = self.path[::-1]


def main():
    row, column = list(map(int, input().split()))
    table = Table(row, column)
    table.parseInput()

    # for test:
    for i in range(row):
        for j in range(column):
            print(table.matrix[i][j], end=" ")
        print()
    print(table.xyRobot)
    print(table.xyButters)
    print(table.xyPersons)
    print(table.matrix)

    fBfs = ForwardBFS(table)

    fBfs.calcPathAndCost()

    # print("action: ", fBfs.lastNode.parent.action)
    print("path:   ", fBfs.path)
    print("cost:   ", fBfs.cost)
    # print("depth:   ", fBfs.lastNode.depth)



if __name__ == '__main__':
    main()
