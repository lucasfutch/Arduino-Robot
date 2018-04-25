from controller import Controller
from matlab_port import MatlabPort
from navigator import Navigator

class rover():
    def __init__(time_step,
                 forward_speed,
                 pivot_threshold,
                 tracker,
                 my_id,
                 target_id=None):

        # system work horses
        self.controller = Controller(time_step, forward_speed, pivot_threshold)
        self.navigator = Navigator()
        self.tracker = tracker
        self.id = my_fid
        self.target_id = target_fid

        # state parameters
        self.current_heading = 0
        self.pos = [0, 0]
        self.target_pos = [0, 0]
        self.desired_heading = 0

    def update_state(self, target_pos=None):
        # update my state parameters
        self.current_heading = self.tracker.get_heading(self.id)
        self.pos = self.tracker.get_pos(self.id)

        # update my target's state parmeters
        if (self.target_id != None):
            self.target_pos = self.tracker.get_pos(self.target_id)
        else:
            self.target_pos = target_pos

        if (self.pos and self.target_pos):
            self.desired_heading = self.navigator \
            .get_target_heading(self.pos, self.target_pos)

    def update_action(self):
        if (self.pos and self.target_pos):
            # there is enough information to act on
            self.controller.update_motors(self.current_heading,
                                          self.desired_heading)
        else:
            # no new data (fiducial is not in view)
            self.controller.coat()

    def end(self):
        self.controller.stop()
