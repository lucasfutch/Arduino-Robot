from controller import Controller
from matlab_port import MatlabPort
from navigator import Navigator

class Rover():
    def __init__(self,
                 time_step,
                 forward_speed,
                 pivot_threshold,
                 tracker,
                 my_id,
                 comm,
                 target_id=None,
                 reversed=False):

        # system work horses
        self.controller = Controller(time_step,
                                     forward_speed,
                                     pivot_threshold,
                                     comm_port=comm,
                                     reversed=False)
        self.navigator = Navigator()
        self.tracker = tracker
        self.id = my_id
        self.target_id = target_id

        # state parameters
        self.current_heading = 0
        self.pos = [0, 0]
        self.target_pos = [0, 0]
        self.desired_heading = 0

    def update_state(self, target_pos=None, desired_heading=None):
        # update my state parameters
        self.current_heading = self.tracker.get_heading(self.id)
        self.pos = self.tracker.get_pos(self.id)

        # update my target's state parmeters
        if (target_pos):
            self.target_pos = target_pos
        elif (desired_heading):
            self.desired_heading = desired_heading
            self.target_pos = None
        else:
            self.target_pos = self.tracker.get_pos(self.target_id)
            if (self.pos and self.target_pos):
                self.desired_heading = self.navigator \
                .get_target_heading(self.pos, self.target_pos)
            else:
                self.desired_heading = None

    def update_action(self):
        if (self.pos and self.desired_heading):
            # there is enough information to act on
            self.controller.update_motors(self.current_heading,
                                          self.desired_heading)
        else:
            # no new data (fiducial is not in view)
            self.controller.coast()

    def end(self):
        self.controller.stop()
