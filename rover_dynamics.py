import numpy as np

class RoverDynamics:
    def __init__(self,
                 wheel_diameter,
                 wheel_separation,
                 starting_position,
                 starting_heading):

        # robot parameters
        self.wheel_diameter = wheel_diamter
        self.wheel_separation = wheel_separation

        # system state
        self.position = starting_position
        self.heading = starting_heading
        self.turn_radius
        self.d_theta

    def update_state(left_motor_deg, right_motor_deg):
        # get linear distance traveled by each wheel
        s1 = self.get_linear_dist(right_motor_deg)
        s2 = self.get_linear_dist(left_motor_deg)

        # get change in heading
        self.d_theta = (s1 - s2)/self.wheel_separation

        # get turn radius
        if (s1 > s2):
            self.turn_radius = (s1*self.wheel_separation)/(s1-s2)
        elif(s1 < s2):
            self.turn_radius = (s1*self.wheel_separation)/(s1-s2)
        else:
            self.turn_radius = None

        # update heading
        self.heading += self.d_theta

        # calculate new position
        center_rad = self.turn_radius - (self.wheel_separation)/2.0
        dx = center_rad - center_rad*np.cos(self.d_theta)
        dy = center_rad*np.sin(self.d_theta)
        self.position[0] += dx
        self.position[1] += dy

    def get_linear_dist(angle_deg):
        return self.wheel_diameter*angle_deg*np.pi/180.0

    def get_new_heading(left_motor_deg, right_motor_deg):
        return self.heading

    def get_new_position(left_motor_deg, right_motor_deg):
        return self.position
