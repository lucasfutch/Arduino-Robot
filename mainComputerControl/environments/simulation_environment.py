import time
from simulation.simulated_rover import SimulatedRover
from simulation.render import RoverRender
from agents.coulomb_agent import CoulombAgent


class SimulationEnvironment:
    def __init__(self, render=True):
        self.render = render
        self.arena_height = 1000
        self.arena_width = 1000

        self.evader = SimulatedRover(time_step=0.1,
                                     starting_heading=0,
                                     starting_position=[300, 500],
                                     max_pivot_input=50,
                                     forward_speed=100,
                                     pivot_threshold=30,
                                     proportional_gain=5,
                                     integrator_gain=0)

        self.pursuer = SimulatedRover(time_step=0.1,
                                      starting_heading=0,
                                      starting_position=[700, 500],
                                      max_pivot_input=50,
                                      forward_speed=70,
                                      pivot_threshold=30,
                                      proportional_gain=5,
                                      integrator_gain=0)

        self.evader_agent = CoulombAgent(self)

        self.pursuer.target = self.evader

        if (render):
            from simulation.render import RoverRender
            self.rover_rendering = RoverRender(self.arena_height, self.arena_width)

    def get_system_state(self):
        pass

    def step(self):
        self.evader.update_state(desired_heading=self.evader_agent.get_target_heading())
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

    def reset(self):
        pass

if __name__ == '__main__':

    env = SimulationEnvironment()

    for i in range(10000):
        env.step()
        time.sleep(0.02)
