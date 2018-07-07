import numpy as np

class Navigator():
    def __init__(self):
        self.my_pos = None
        self.target_pos = None
        self.target_heading = None
        self.distance_to_target = None
        self.arrival_distance = 0.05

    def get_target_heading(self, my_pos, target_pos):
        # save values
        self.my_pos = my_pos
        self.target_pos = target_pos

        # calculate complimentary angle
        theta_complimentary_rad = np.arctan(abs(target_pos[0]-my_pos[0])/abs(target_pos[1]-my_pos[1]))
        theta_complimentary_deg = theta_complimentary_rad*(180.0/np.pi)

        # determine what quadrant the target is in
        if (target_pos[0] > my_pos[0]):
            if (target_pos[1] < my_pos[1]):
                # Quadrant 1
                self.target_heading = theta_complimentary_deg
            else:
                # Quadrant 2
                self.target_heading = theta_complimentary_deg + 90
        else:
            if (target_pos[1] < my_pos[1]):
                # Quadrant 4
                self.target_heading = 360 - theta_complimentary_deg
            else:
                # Quadrant 3
                self.target_heading = theta_complimentary_deg + 180

        return self.target_heading

    def has_arrived(self):
        if (self.my_pos and self.target_pos):
            self.distance_to_target = np.sqrt((self.my_pos[0]-self.target_pos[0])**2 + (self.my_pos[1]-self.target_pos[1])**2)
        else:
            self.distance_to_target = None

        if (self.my_pos and self.target_pos):
            if (self.distance_to_target < self.arrival_distance):
                print "Arrived"
                return True
        print "Not Arrived"
        return False
