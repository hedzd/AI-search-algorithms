from table import Table
from bidirectionalBFS import BidirectionalBFS
from drawBoard import DrawBoard
from aStar import AStar
import time


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

    # bbfs
    bbfs = BidirectionalBFS(table)
    startT = time.time()
    bbfs.calcPathAndCost()
    endT = time.time()

    if not bbfs.path:
        print("Can't pass the butter")
    else:
        print("path:   ", bbfs.path)
        print("cost:   ", bbfs.cost)
        print("depthForward:  ", bbfs.forwardLastNode.depth)
        print("depthBackward: ", len(bbfs.path2))
        print("sum of depth: ", len(bbfs.path))

    print("Execution time in seconds: ", endT - startT)
    print("Expanded Nodes: ", bbfs.numVisitedNodes)
    print("Generated Nodes: ", bbfs.numAllNodes)
    # #Draw
    # draw = DrawBoard(table, bbfs.path)
    # draw.draw()

    # aStar
    aStar = AStar(table)

    startT = time.time()
    aStar.calcPathAndCost()
    endT = time.time()

    if not aStar.path:
        print("Can't pass the butter")
    else:
        print("path:   ", aStar.path)
        print("cost:   ", aStar.cost)
        print("depth: ", aStar.lastNode.depth)

    print("Execution time in seconds: ", endT - startT)
    print("Expanded Nodes: ", aStar.numVisitedNodes)
    print("Generated Nodes: ", aStar.numAllNodes)

    # Draw
    # draw = DrawBoard(table, aStar.path)
    # draw.draw()


if __name__ == '__main__':
    main()
