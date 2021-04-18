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
        self.state = [int(x), int(y)]
        self.child = []
        self.parent = None
        self.action = None
        self.depth = None
        self.cost = None


class ForwardBFS:
    def __init__(self, tableInfo):
        self.tableInfo = tableInfo
        self.path = []
        self.cost = 0
        self.fringe = queue.Queue()
        self.explored = []
        self.lastNode = None
        self.initialNode = None

    def searchAlgorithm(self):
        initialNode = self.createNode(self.tableInfo.xyRobot[0], self.tableInfo.xyRobot[1], None, None)
        if self.checkGoal(initialNode):
            self.lastNode = initialNode
            return True
        self.fringe.put(initialNode)
        while True:
            if self.fringe.empty():
                return False
            node = self.fringe.get()
            print("dequeue node:", node.state)
            state = node.state
            successor, action = self.successor(state)
            for i,s in enumerate(successor):
                if s in self.explored:
                    continue
                newNode = self.createNode(s[0], s[1], node, action[i])
                node.child.append(newNode)
                if self.checkGoal(newNode):
                    print(newNode.state," action: ", newNode.action)
                    self.lastNode = newNode
                    return True

                print("enqueue node:", newNode.state)
                self.fringe.put(newNode)
            self.explored.append(node.state)
            print("explored: ", self.explored)

    def createNode(self, x, y, parentNode, action):
        node = Node(x, y)
        node.cost = int(self.tableInfo.matrix[y][x])
        if parentNode is None:
            node.depth = 1
        else:
            node.depth = parentNode.depth + 1
            node.parent = parentNode
            node.action = action
        return node

    def checkGoal(self, node):
        for xyP in self.tableInfo.xyPersons:
            #for xyB in self.tableInfo.xyButters:
            if xyP == node.state:
                # TODO:
                # check xyB == xyP and
                return True
        return False

    def successor(self, state):
        x = state[0]
        y = state[1]
        sList = []
        actionList = []
        if x + 1 < self.tableInfo.column:
            if self.checkCell(x + 1, y):
                sList.append([x + 1, y])
                actionList.append('R')
        if x - 1 >= 0:
            if self.checkCell(x - 1, y):
                sList.append([x - 1, y])
                actionList.append('L')
        if y + 1 < self.tableInfo.row:
            if self.checkCell(x, y + 1):
                sList.append([x, y + 1])
                actionList.append('D')
        if y - 1 >= 0:
            if self.checkCell(x, y - 1):
                sList.append([x, y - 1])
                actionList.append('U')
        return sList, actionList

    def checkCell(self, x, y):
        if self.tableInfo.matrix[y][x] == 'x':
            return False
        # TODO: pesron
        # for xyP in self.tableInfo.xyPersons:
        #     if xyP == [x, y]:
        #         return False
        # TODO: butter?! :-??
        return True

    def calcPathAndCost(self):
        res = self.searchAlgorithm()
        if not res:
            print("no path")
        else:
            node = self.lastNode
            while node.parent is not None:
                print("node:", node.state)
                print("add to path", node.action)
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
    print("path:   ",fBfs.path)
    print("cost:   ",fBfs.cost)
    # ForwardBFS(table)


if __name__ == '__main__':
    main()
