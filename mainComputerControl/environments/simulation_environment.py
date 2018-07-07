import time
from simulation.simulated_rover import SimulatedRover
from simulation.render import RoverRender

class SimulationEnvironment:
    def __init__(self, render=True):
        self.render = render
        self.simulated_pursuer = SimulatedRover(time_step=0.1,
                                           starting_heading=0,
                                           starting_position=[20, 20],
                                           max_pivot_input=50,
                                           forward_speed=70,
                                           pivot_threshold=30,
                                           proportional_gain=5,
                                           integrator_gain=0)

        if (render):
            from simulation.render import RoverRender
            self.rover_rendering = RoverRender(
                                   self.simulated_pursuer.dynamics.position,
                                   self.simulated_pursuer.dynamics.heading)

    def get_system_state(self):
        pass

    def step(self):
        self.simulated_pursuer.update_state(target_pos=[400, 400])
        self.simulated_pursuer.update_action()

        if (self.render):
            self.rover_rendering.render(self.simulated_pursuer.dynamics.position,
                                        self.simulated_pursuer.dynamics.heading)

    def reset(self):
        pass

if __name__ == '__main__':

    env = SimulationEnvironment()

    for i in range(1000):
        env.step()
        time.sleep(0.1)
