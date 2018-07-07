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
        dx = abs(target_pos[0]-my_pos[0])
        dy = abs(target_pos[1]-my_pos[1])

        if (dx != 0):
            theta_complimentary_rad = np.arctan(dy/dx)
            theta_complimentary_deg = theta_complimentary_rad*(180.0/np.pi)
        else:
            theta_complimentary_deg = 90

        print "theta compl: ", theta_complimentary_deg

        # determine what quadrant the target is in
        if (target_pos[0] > my_pos[0]):
            if (target_pos[1] < my_pos[1]):
                # Quadrant 1
                print "Q1"
                self.target_heading = 90 - theta_complimentary_deg
            else:
                # Quadrant 2
                print "Q2"
                self.target_heading = theta_complimentary_deg + 90
        else:
            if (target_pos[1] > my_pos[1]):
                # Quadrant 3
                print "Q3"
                self.target_heading = 270 - theta_complimentary_deg
            else:
                # Quadrant 4
                print "Q4"
                self.target_heading = 270 + theta_complimentary_deg

        print self.target_heading
        return self.target_heading

    def has_arrived(self):
        if (self.my_pos and self.target_pos):
            self.distance_to_target = np.sqrt((self.my_pos[0]-self.target_pos[0])**2 + (self.my_pos[1]-self.target_pos[1])**2)
        else:
            self.distance_to_target = None

        if (self.my_pos and self.target_pos):
            if (self.distance_to_target < self.arrival_distance):
                return True
        return False

if __name__ == '__main__':
    n = Navigator()
    my_pos = [500, 500]
    while True:
        x = int(raw_input("X: "))
        y = int(raw_input("Y: "))
        n.get_target_heading(my_pos, [x, y])
