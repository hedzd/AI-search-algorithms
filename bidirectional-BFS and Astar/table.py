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
