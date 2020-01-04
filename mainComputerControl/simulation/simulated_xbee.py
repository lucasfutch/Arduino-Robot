class SimulatedXbee(object):
    def __init__(self, system_dynamics):
        self.dynamics = system_dynamics
        self.mode = 'FORWARD'
        self.scaling = 1.0/10.0
        self.left_motor_input = None
        self.right_motor_input = None

    def send_command(self, strOut):
        if (strOut == 0): # stop
            return
        elif (strOut == 1):
            self.mode = "PIVOT_LEFT"
        elif (strOut == 2):
            self.mode = "PIVOT_RIGHT"
        elif (strOut == 3):
            self.mode = "FORWARD"
        elif (strOut == 4):
            pass # prelimitor
        elif (strOut == 5):
            pass # postlimitor
        else:
            if (self.mode == "FORWARD"):
                if (self.left_motor_input):
                    self.right_motor_input = strOut*self.scaling
                else:
                    self.left_motor_input = strOut*self.scaling
                    return

            elif (self.mode == "PIVOT_RIGHT"):
                self.left_motor_input = strOut*self.scaling
                self.right_motor_input = strOut*self.scaling*-1


            elif (self.mode == "PIVOT_LEFT"):
                self.left_motor_input = strOut*self.scaling*-1
                self.right_motor_input = strOut*self.scaling

            self.dynamics.update_state(self.left_motor_input,
                                       self.right_motor_input)
            self.left_motor_input = None
            self.right_motor_input = None

    def close(self):
        # needed to simulate real serial port of used for Xbee
        return
