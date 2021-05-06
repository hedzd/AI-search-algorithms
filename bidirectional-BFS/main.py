from table import Table
from bidirectionalBFS import BidirectionalBFS
from drawBoard import DrawBoard
from aStar import AStar


def main():
    row, column = list(map(int, input().split()))
    table = Table(row, column)
    table.parseInput()

    # for test:
    # for i in range(row):
    #     for j in range(column):
    #         print(table.matrix[i][j], end=" ")
    #     print()
    # print(table.xyRobot)
    # print(table.xyButters)
    # print(table.xyPersons)
    # print(table.matrix)

    #bbfs
    bbfs = BidirectionalBFS(table)

    bbfs.calcPathAndCost()

    print("path:   ", bbfs.path)
    print("cost:   ", bbfs.cost)

    #Draw
    draw = DrawBoard(table, bbfs.path)
    draw.draw()


    #aStar
    # aStar = AStar(table)
    # aStar.calcPathAndCost()
    # print("path:   ", aStar.path)
    # print("cost:   ", aStar.cost)
    #
    # # Draw
    # draw = DrawBoard(table, aStar.path)
    # draw.draw()

if __name__ == '__main__':
    main()
