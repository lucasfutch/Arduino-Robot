import numpy as np

class RoverDynamics:
    def __init__(self,
                 wheel_diameter,
                 wheel_separation,
                 starting_position,
                 starting_heading):

        # robot parameters
        self.wheel_diameter = wheel_diameter
        self.wheel_separation = wheel_separation

        # system state
        self.position = starting_position
        self.heading = starting_heading
        self.turn_radius = None
        self.d_theta = None

    def pivot(self, left_motor_deg, right_motor_deg):
        self.d_theta = self.get_linear_dist(left_motor_deg)/(np.pi*self.wheel_separation)*180
        self.heading += self.d_theta

    def forward_turn(self, left_motor_deg, right_motor_deg):
        if (left_motor_deg < right_motor_deg):
            s1 = self.get_linear_dist(right_motor_deg)
            s2 = self.get_linear_dist(left_motor_deg)
            self.d_theta = ((s1 - s2)/self.wheel_separation)*(180/np.pi)
            self.heading -= self.d_theta
        else:
            s1 = self.get_linear_dist(left_motor_deg)
            s2 = self.get_linear_dist(right_motor_deg)
            self.d_theta = ((s1 - s2)/self.wheel_separation)*(180/np.pi)
            self.heading += self.d_theta

        self.turn_radius = (s1*self.wheel_separation)/(s1-s2)

        # calcualte displacement for 0deg heading
        center_rad = self.turn_radius - (self.wheel_separation)/2.0
        dx = -(center_rad - center_rad*np.cos(self.d_theta*np.pi/180))
        dy = center_rad*np.sin(self.d_theta*np.pi/180)
        displacement = np.array([[dx],[dy]])

        # rotate the displacement vector
        rad = self.heading*np.pi/180.0
        rotation_matrix = np.array([[np.cos(-rad), -np.sin(-rad)], [np.sin(-rad), np.cos(-rad)]])
        displacement_rotated = np.matmul(rotation_matrix, displacement)

        # calculate the final position of the the rover
        self.position[0] += displacement_rotated[0][0]
        self.position[1] -= displacement_rotated[1][0]

    def move_straight(self, left_motor_deg, right_motor_deg):
        # calcualte distance forward
        dy = self.get_linear_dist(left_motor_deg)
        displacement = np.array([[0],[dy]])

        # rotate the displacement vector
        rad = self.heading*np.pi/180.0
        rotation_matrix = np.array([[np.cos(-rad), -np.sin(-rad)], [np.sin(-rad), np.cos(-rad)]])
        displacement_rotated = np.matmul(rotation_matrix, displacement)

        # calculate the final position of the the rover
        self.position[0] += displacement_rotated[0][0]
        self.position[1] -= displacement_rotated[1][0]

    def update_state(self, left_motor_deg, right_motor_deg):
        # evaluate type of motion
        if (left_motor_deg == -1*right_motor_deg):
            self.state_pivot(left_motor_deg, right_motor_deg)
        elif (left_motor_deg == right_motor_deg):
            self.move_straight(left_motor_deg, right_motor_deg)
        else:
            self.forward_turn(left_motor_deg, right_motor_deg)

    def get_linear_dist(self, angle_deg):
        return self.wheel_diameter*angle_deg*np.pi/180.0

    def get_new_heading(self):
        return self.heading

    def get_new_position(self):
        return self.position

if __name__ == '__main__':
    from render import RoverRender
    # state variables
    pos = [320, 240]
    heading = 0
    rover_rendering = RoverRender(pos, heading)
    rover = RoverDynamics(wheel_diameter=5,
                          wheel_separation=20,
                          starting_position=pos,
                          starting_heading=heading)

    while True:
        a = raw_input("Enter action: ")
        if a == "w":
            rover.update_state(30, 30)
        elif a =="a":
            rover.update_state(10, 20)
        elif a =="d":
            rover.update_state(20, 10)
        elif a=="s":
            rover.update_state(-10, -10)

        rover_rendering.render(rover.get_new_position(), rover.get_new_heading())
