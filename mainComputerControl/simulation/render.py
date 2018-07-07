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
        
        self.shape = [np.array([0,-15]),
                      np.array([-10,10]),
                      np.array([10,10]),
                      np.array([0,-15])]

        self.points = [np.array([0,1]),
                       np.array([-1,-1]),
                       np.array([1,-1]),
                       np.array([0,1])]

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
        self.screen = pygame.display.set_mode((1000,1000))
        self.screen.fill(white)
        self.render()

    def draw(self, position, heading, color):
        self.screen.fill(white)
        self.rover_shape.move(position, heading)
        pygame.draw.lines(self.screen, color, False, self.rover_shape.get_tuple_points(), 1)

    def render(self):
        pygame.display.update()
