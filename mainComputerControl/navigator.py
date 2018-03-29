import numpy as np

class Navigator():
    def __init__(self):
        self.my_pos = None
        self.target_pos = None
        self.target_heading = None

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
                print "Qaudrant 1"
                self.target_heading = theta_complimentary_deg
            else:
                # Quadrant 2
                print "Qaudrant 2"
                self.target_heading = theta_complimentary_deg + 90
        else:
            if (target_pos[1] < my_pos[1]):
                # Quadrant 4
                print "Qaudrant 4"
                self.target_heading = 360 - theta_complimentary_deg
            else:
                # Quadrant 3
                print "Qaudrant 3"
                self.target_heading = theta_complimentary_deg + 180

        return self.target_heading
