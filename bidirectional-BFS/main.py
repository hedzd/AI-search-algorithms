class Table:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.matrix = []

    def parseInput(self):
        for i in range(self.row):
            self.matrix.append(input().split())


def main():
    row, column = list(map(int, input().split()))
    table = Table(row, column)
    table.parseInput()


if __name__ == '__main__':
    main()
