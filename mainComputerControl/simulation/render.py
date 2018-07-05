import pygame
import numpy as np
import time

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

class RoverShape:
    def __init__(self):
        """
        self.shape = [np.array([0,-15]),
                      np.array([-10,10]),
                      np.array([10,10]),
                      np.array([0,-15])]

        self.points = [np.array([0,1]),
                       np.array([-1,-1]),
                       np.array([1,-1]),
                       np.array([0,1])]
        """
        self.shape = [np.array([0,5]),
                      np.array([0,-5])]
        self.points = [np.array([0,5]),
                       np.array([0,-5])]

    def move(self, translation, rotation):

        # rotate and translate shape
        rad = rotation*np.pi/180 # rotate clockwise
        rotation_matrix = np.array([[np.cos(rad), -np.sin(rad)], \
                                    [np.sin(rad), np.cos(rad)]])

        for i in range(len(self.points)):
            self.points[i] = np.matmul(rotation_matrix, self.shape[i])
            self.points[i][0] += translation[0]
            self.points[i][1] += translation[1]

    def get_tuple_points(self):
        tuple_list = []
        for coordinate in self.points:
            tuple_list.append(tuple(coordinate))
        return tuple_list

class RoverRender:
    def __init__(self, starting_position, starting_heading):
        self.position = starting_position
        self.heading = starting_heading
        self.rover_shape = RoverShape()

        # start screen
        self.screen = pygame.display.set_mode((640,480))
        self.screen.fill(white)
        self.render(self.position, self.heading)

    def render(self, position, heading):
        self.rover_shape.move(position, heading)
        #self.screen.fill(white)
        pygame.draw.lines(self.screen, black, False, self.rover_shape.get_tuple_points(), 1)
        pygame.display.update()


if __name__ == '__main__':
    import curses

    # get the curses screen window
    screen = curses.initscr()

    # turn off input echoing
    curses.noecho()

    # respond to keys immediately (don't wait for enter)
    curses.cbreak()

    # map arrow keys to special values
    screen.keypad(True)

    # stae variables
    pos = [320, 240]
    heading = 0
    rover = RoverRender(pos, heading)

    try:
        while True:
            char = screen.getch()
            heading_rotated = heading + 90
            if char == ord('q'):
                break
            elif char == curses.KEY_RIGHT:
                # print doesn't work with curses, use addstr instead
                heading += 5
            elif char == curses.KEY_LEFT:
                heading -= 5
            elif char == curses.KEY_UP:
                pos[0] -= np.arccos(heading_rotated)
                pos[1] += np.arcsin(heading_rotated)
            elif char == curses.KEY_DOWN:
                pos[0] += np.arccos(heading_rotated)
                pos[1] -= np.arcsin(heading_rotated)
            print heading
            rover.render(pos, heading)
    finally:
        # shut down cleanly
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()
