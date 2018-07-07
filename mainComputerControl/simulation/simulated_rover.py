from robot.navigator import Navigator
from rover_dynamics import RoverDynamics
from simulated_xbee import SimulatedXbee
from robot.controller import Controller


class SimulatedRover:
    def __init__(self,
                 time_step,
                 starting_heading,
                 starting_position,
                 max_pivot_input=50,
                 forward_speed=70,
                 pivot_threshold=30,
                 proportional_gain=5,
                 integrator_gain=0):

        # rover_dynamics class
        self.dynamics = RoverDynamics(10,
                                      20,
                                      starting_position,
                                      starting_heading)
        self.xbee = SimulatedXbee(self.dynamics)
        self.controller = Controller(time_step,
                                     max_pivot_input,
                                     forward_speed,
                                     pivot_threshold,
                                     proportional_gain,
                                     integrator_gain,
                                     reversed,
                                     self.xbee)

        self.navigator = Navigator()
        self.navigator.arrival_distance = 10

        # state parameters
        self.current_heading = 0
        self.pos = [0, 0]
        self.target_pos = [0, 0]
        self.desired_heading = 0

        # target
        self.target = None

    def set_target(self, target_system):
        self.target = target_system

    def update_state(self,
                     target_pos=None,
                     desired_heading=None,
                     heading_correction=None):

        # update my state parameters
        self.current_heading = self.dynamics.get_heading()
        self.pos = self.dynamics.get_position()

        if (self.target):
            self.desired_heading = self.navigator \
            .get_target_heading(self.pos, self.target.pos)
        elif (desired_heading):
            self.desired_heading = desired_heading
            self.target_pos = None
        elif (heading_correction):
            self.desired_heading = self.desired_heading+(heading_correction%360)
        else: # (target pos)
            self.desired_heading = self.navigator \
            .get_target_heading(self.pos, target_pos)


    def update_action(self):
        if (self.target_pos and self.navigator.has_arrived()):
            # we have arrived at our destination
            self.controller.coast()
        else:
            # we are given a target heading
            self.controller.update_motors(self.current_heading,
                                          self.desired_heading)

    def stop(self):
        self.controller.stop()

    def coast(self):
        self.controller.coast()

    def end(self):
        self.controller.close()
