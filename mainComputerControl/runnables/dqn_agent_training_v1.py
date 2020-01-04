import random
from environments.simulation_environment import SimulationEnvironment
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from agents.coulomb_agent import CoulombAgent


ROUNDS = 1000
EPISODES = 1000

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(50, input_dim=self.state_size, activation='relu'))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

if __name__ == "__main__":
    env = SimulationEnvironment(render=False)
    state_size = 6
    action_size = 36
    agent = DQNAgent(state_size, action_size)
    # agent.load("./save/cartpole-dqn.h5")
    done = False
    batch_size = 100

    # I am creating a coulomb agent for calculating the reward
    coulomb_agent = CoulombAgent(env)

    for round in range(ROUNDS):
        # generate starting positions
        evader_start = list(np.random.random_integers(1000, size=2))
        pursuer_start = list(np.random.random_integers(1000, size=2))

        # reset environment
        env.reset(evader_start, pursuer_start)
        state, done = env.system_state()
        state = np.reshape(state, [1, state_size])

        for episode in range(EPISODES):
            # Get evader action
            action = agent.act(state)
            correction = (action-18)*5

            # Update the environment
            env.step(evader_heading_correction=correction)
            next_state, done = env.system_state()
            next_state = np.reshape(next_state, [1, state_size])

            # Calculate the reward
            fx, fy = coulomb_agent.calculate_forces()
            reward = 0.01/np.sqrt(np.power(fx, 2) + np.power(fy, 2))

            agent.remember(state, action, reward, next_state, done)
            state = next_state

            if done:
                print("Round: {}/{}, score: {}, e: {:.2}"
                      .format(round, ROUNDS, episode, agent.epsilon))
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")
