from ..robot.navigator import Navigator
from rover_dynamics import RoverDynamics


class SimulatedRover:
    def __init__(self,
                 my_id,
                 target_id,
                 starting_heading,
                 starting_position,
                 max_pivot_input=50,
                 forward_speed=70,
                 pivot_threshold=30,
                 proportional_gain=5,
                 integrator_gain=0):

        # Rover attributes
        self.my_id = my_id
        self.target_id =target_id
        self.max_pivot_input = max_pivot_input
        self.forward_speed = forward_speed
        self.pivot_threshold = pivot_threshold
        self.proportional_gain = proportional_gain
        self.integrator_gain = integrator_gain
        self.navigator = Navigator()

        # rover_dynamics class
        dynamics = RoverDynamics(starting_position, starting_heading)

    def update_state(self,
                     target_pos=None,
                     desired_heading=None,
                     heading_correction=None):

        if (target_pos):
            self.target_pos = target_pos
            self.desired_heading = self.navigator \
            .get_target_heading(self.pos, self.target_pos)
        elif (desired_heading):
            self.desired_heading = desired_heading
            self.target_pos = None
        elif (heading_correction):
            self.desired_heading += heading_correction
            self.target_pos = None
        else:
            self.desired_heading = None

    def update_action(self):
        # Here, we need to update the state parameters of the Rover
        # according to the system dyamics

        # If action is to do nothing, then do nothing
        if (self.desired_heading == None):
            return

        # 1) update current position

        # 2) update current heading
