import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
cellWidth = 50
cellHeight = 50
MARGIN = 5


class DrawBoard:

    def __init__(self, tableInfo, path):
        self.row = tableInfo.row
        self.column = tableInfo.column
        self.matrix = tableInfo.matrix
        self.path = path
        self.robotImg = pygame.image.load('icons/robot.png')
        self.butterImg = pygame.image.load('icons/butter.png')
        self.personImg = pygame.image.load('icons/avatar.png')
        self.xyButters = tableInfo.xyButters
        self.xyPersons = tableInfo.xyPersons
        self.xyRobot = tableInfo.xyRobot
        self.matrix[self.xyRobot[1]][self.xyRobot[0]] = '*'

    def move(self):
        currMove = self.path.pop(0)
        if currMove == 'R':
            self.xyRobot[0] = self.xyRobot[0] + 1
        elif currMove == 'L':
            self.xyRobot[0] = self.xyRobot[0] - 1
        elif currMove == 'U':
            self.xyRobot[1] = self.xyRobot[1] - 1
        elif currMove == 'D':
            self.xyRobot[1] = self.xyRobot[1] + 1
        self.matrix[self.xyRobot[1]][self.xyRobot[0]] = '*'
        for xy in self.xyButters:
            if [self.xyRobot[0], self.xyRobot[1]] == xy:
                if currMove == 'R':
                    xy[0] = xy[0] + 1
                elif currMove == 'L':
                    xy[0] = xy[0] - 1
                elif currMove == 'U':
                    xy[1] = xy[1] - 1
                elif currMove == 'D':
                    xy[1] = xy[1] + 1

    def calcXY(self, x, y):
        xy = [x * (cellWidth + MARGIN) + ((cellWidth - 24) / 2), y * (cellHeight + MARGIN) + ((cellHeight - 24) / 2)]
        return xy

    def draw(self):
        pygame.init()
        WINDOW_SIZE = [self.column * (cellWidth + MARGIN) + MARGIN, self.row * (cellHeight + MARGIN) + MARGIN]
        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Path finding using bidirectional BFS")
        # pygame.display.toggle_fullscreen()
        done = False
        clock = pygame.time.Clock()

        while not done:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            for row in range(self.row):
                for column in range(self.column):
                    color = WHITE
                    if self.matrix[row][column] == 'x':
                        color = RED
                    if self.matrix[row][column] == '*':
                        color = GREEN
                    pygame.draw.rect(screen, color,
                                     [(MARGIN + cellWidth) * column + MARGIN,
                                      (MARGIN + cellHeight) * row + MARGIN,
                                      cellWidth,
                                      cellHeight])

            xyR = self.calcXY(self.xyRobot[0], self.xyRobot[1])
            screen.blit(self.robotImg, (xyR[0], xyR[1]))
            for xy in self.xyButters:
                xyB = self.calcXY(xy[0], xy[1])
                screen.blit(self.butterImg, (xyB[0], xyB[1]))

            for xy in self.xyPersons:
                xyP = self.calcXY(xy[0], xy[1])
                screen.blit(self.personImg, (xyP[0], xyP[1]))

            if self.path:
                self.move()
            # Limit to 60 frames per second
            # clock.tick(60)
            # # Go ahead and update the screen with what we've drawn.
            # pygame.display.flip()
            pygame.time.wait(1000)
            pygame.display.update()
        pygame.quit()