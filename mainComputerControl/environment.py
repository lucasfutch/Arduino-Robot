import time
import random

from rover import Rover
from tracker import Tracker

import numpy as np

class Environment():
    def __init__(self, system_time_step):
        # system
        self.system_tracker = Tracker()
        self.timer = time.time()
        self.system_time_step = system_time_step
        self.pursuer_id = 0
        self.evader_id = 2

        # robots
        self.pursuer = Rover(tracker=self.system_tracker,
                             my_id=self.pursuer_id,
                             target_id=self.evader_id,
                             time_step=self.system_time_step,
                             comm_port='COM5')

        self.evader = Rover(tracker=self.system_tracker,
                            my_id=self.evader_id,
                            target_id=None,
                            time_step=self.system_time_step,
                            max_pivot_input=100,
                            forward_speed=100,
                            pivot_threshold=30,
                            proportional_gain=5,
                            integrator_gain=0,
                            reversed=True,
                            comm_port='COM9')

    def getSystemState(self):
        self.system_tracker.update()
                
        # return the system state
        evader_x = self.system_tracker.get_pos(self.evader_id)[0]
        evader_y = self.system_tracker.get_pos(self.evader_id)[1]
        evader_heading = self.system_tracker.get_heading(self.evader_id)
        pursuer_x = self.system_tracker.get_pos(self.pursuer_id)[0]
        pursuer_y = self.system_tracker.get_pos(self.pursuer_id)[1]
        pursuer_heading = self.system_tracker.get_heading(self.pursuer_id)

        # Round Positions to the Centimeter and directions to full degrees
        system_state_array = np.array((np.round(evader_x, 2), np.round(evader_y, 2), np.round(evader_heading), np.round(pursuer_x, 2), np.round(pursuer_y), np.round(pursuer_heading)))
        return system_state_array

        
    def step(self, target_heading=None, target_position=None):
        # update environmate state
        self.system_tracker.update()

        if ((target_heading==None) and (target_position == None)):
            return None

        # update system state
        elif (target_heading):
            self.pursuer.update_state()
            self.evader.update_state(desired_heading=target_heading)

        # update system state
        elif(target_position):
            self.pursuer.update_state()
            self.evader.update_state(target_pos=target_position)

        # update actions
        self.pursuer.update_action()
        self.evader.update_action()

        # wait for there to be information to report and update
        time.sleep(self.system_time_step)
        return getSystemState()
        
        
    def reset(self):
        # generate a random starting position
        pursuer_x = random.randrange(20, 800, 1)/1000.0
        pursuer_y = random.randrange(20, 800, 1)/1000.0
        evader_x = random.randrange(20, 800, 1)/1000.0
        evader_y = random.randrange(20, 800, 1)/1000.0

        pursuer_target = [pursuer_x, pursuer_y]
        evader_target = [evader_x, evader_y]

        # tell robots to go to their reset locations
        self.pursuer.update_state(target_pos=pursuer_target)
        self.evader.update_state(target_pos=evader_target)

        # wait until they have arrived
        while ((not self.pursuer.navigator.has_arrived()) and
               (not self.evader.navigator.has_arrived())):
            # keep moving toward the targets
            self.system_tracker.update()
            self.pursuer.update_action()
            self.evader.update_action()
            time.sleep(0.001)
