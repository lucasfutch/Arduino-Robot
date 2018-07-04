import pygame
import numpy as np

class RoverShape:
    def __init__(self):
        self.shape = [np.array([0,1]),
                      np.array([-1,-1]),
                      np.array([1,-1])]

        self.points = [np.array([0,1]),
                      np.array([-1,-1]),
                      np.array([1,-1])]]

    def move(translation, rotation):

        # rotate and translate shape
        rad = -1*degree*np.pi/180 # rotate clockwise
        rotation_matrix = np.array([np.cos(rad), -np.sin(rad)],
                                   [np.sin(rad), np.cos(rad)])

        for i in range(len(self.points)):
            self.point[i] = np.matmul(rotation_matrix, self.shape[i])
            self.point[i][0] += translation[0]
            self.point[i][1] += translation[1]

class RoverRender
    def __init__(self, starting_position,starting_position):
        self.position = starting_position
        self.heading = starting_heading
        self.rover_shape = RoverShape()
        screen = pygame.display.set_mode((640,480))

    def render(position, heading):
        self.rover_shape.move(position, heading)
