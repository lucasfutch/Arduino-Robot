import time
from simulation.simulated_rover import SimulatedRover
from simulation.render import RoverRender
from agents.coulomb_agent import CoulombAgent


class SimulationEnvironment:
    def __init__(self,
                 render=True,
                 evader_start=[300, 500],
                 pursuer_start=[700,500]):

        self.render = render
        self.arena_height = 1000
        self.arena_width = 1000

        self.evader = SimulatedRover(time_step=0.1,
                                     starting_heading=0,
                                     starting_position=evader_start,
                                     max_pivot_input=50,
                                     forward_speed=100,
                                     pivot_threshold=30,
                                     proportional_gain=5,
                                     integrator_gain=0)

        self.pursuer = SimulatedRover(time_step=0.1,
                                      starting_heading=0,
                                      starting_position=pursuer_start,
                                      max_pivot_input=50,
                                      forward_speed=70,
                                      pivot_threshold=30,
                                      proportional_gain=5,
                                      integrator_gain=0)

        self.pursuer.target = self.evader

        if (render):
            from simulation.render import RoverRender
            self.rover_rendering = RoverRender(self.arena_height, self.arena_width)

    def system_state(self):
        return [self.evader.pos[0],
                self.evader.pos[1],
                self.evader.current_heading,
                self.pursuer.pos[0],
                self.pursuer.pos[1],
                self.pursuer.current_heading], self.pursuer.navigator.has_arrived()

    def step(self,
             evader_target_pos=None,
             evader_desired_heading=None,
             evader_heading_correction=None):

        self.evader.update_state(target_pos=evader_target_pos,
                                 desired_heading=evader_desired_heading,
                                 heading_correction=evader_heading_correction)
        self.pursuer.update_state()

        self.evader.update_action()
        self.pursuer.update_action()

        if (self.render):
            self.rover_rendering.clear()
            self.rover_rendering.draw(self.pursuer.dynamics.position,
                                      self.pursuer.dynamics.heading,
                                      (0,0,255)) # blue)
            self.rover_rendering.draw(self.evader.dynamics.position,
                                      self.evader.dynamics.heading,
                                      (255,0,0)) # red)
            self.rover_rendering.render()

    def reset(self, evader_starting_position, pursuer_starting_position):
        self.__init__(render=self.render,
                      evader_start=pursuer_starting_position,
                      pursuer_start=evader_starting_position)
