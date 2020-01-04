from environments.simulation_environment import SimulationEnvironment
from agents.coulomb_agent import CoulombAgent
import numpy as np

ROUNDS = 10
EPISODES = 500

if __name__ == '__main__':

    # Create the simulation environment
    env = SimulationEnvironment(render=True)

    # Create the evading agent
    evader_agent = CoulombAgent(env)

    for round in range(ROUNDS):
        # generate starting positions
        evader_start = list(np.random.random_integers(1000, size=2))
        pursuer_start = list(np.random.random_integers(1000, size=2))

        # reset environment
        env.reset(evader_start, pursuer_start)

        # Play the game
        for episode in range(EPISODES):
            evader_target = evader_agent.get_target_heading()
            env.step(evader_desired_heading=evader_target)

            state, done = env.system_state()
            print state

            if done:
                print "GAME OVER"
                break
