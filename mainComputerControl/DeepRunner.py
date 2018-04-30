# -*- coding: utf-8 -*-
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

# Custom Robotic Chaser RL environment
import environment

EPISODES = 5000


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    def _huber_loss(self, target, prediction):
        # sqrt(1+error^2)-1
        error = prediction - target
        return K.mean(K.sqrt(1+K.square(error))-1, axis=-1)

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss=self._huber_loss,
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.model.get_weights())

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
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                a = self.model.predict(next_state)[0]
                t = self.target_model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * t[np.argmax(a)]
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

# A Function Which Determines the 
def getReward(next_state):
    # Get the important distances
    pos_runner = np.array(next_state[0:2])
    pos_center = np.array((0.5, 0.5))
    pos_chaser = np.array(next_state[3:5])
    dist_from_center = np.linalg.norm(pos_center-pos_runner)
    dist_from_chaser = np.linalg.norm(pos_chaser-pos_runner)
    # Perform our pseudo-Couloumbs law
     # Avoid blowing up massive rewards with constant 1 in the denominator and shrink the function significantly in the X direction
    central_reward = 2/(1+(dist_from_center*50)**2)
    # Again using distance squared, but inverting to reward greater distances rather than closer
    distance_reward = 10*dist_from_chaser**2
    return central_reward + distance_reward

if __name__ == "__main__":
    env = environment.Environment(0.04) # Our time step is slightly greater than the time it takes to send a single frame
    state_size = 6 # 6 length array - ChaserX, ChaserY, RunnerX, RunnerY, CurrentRunnerHeading, CurrentChaserHeading
    action_size = 4 # 4 actions - turn left, turn right, continue straight, do nothing
    agent = DQNAgent(state_size, action_size)
    done = False
    batch_size = 32

    for e in range(EPISODES):
        state = env.getSystemState()
        state = np.reshape(state, [1, state_size])
        for time in range(1000): # Max time of roughly 30 seconds
            action = agent.act(state)
            current_heading_in_360 = state[2] + 180
            if action != 3: # 3 action is do nothing
                if action != 2: # 2 is subtract from heading
                    # Either go straight or right
                    direct_action = (current_heading_in_360 + (5*action)) % 360
                else:
                    # Go Left
                    direct_action = (current_heading_in_360 - 5) % 360
            else:
                # Do Nothing
                direct_action = None
            next_state = env.step(target_heading=direct_action)
            done = bool(next_state[0] == next_state[3] and next_state[1] == next_state[4])
            reward = getReward(next_state) if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done or time == 999:
                env.reset()
                agent.update_target_model()
                print("episode: {}/{}, Time Survived: {}, e: {:.2}"
                      .format(e, EPISODES, time, agent.epsilon))
                break
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
            #agent.save("./running-agent-ddqn.h5")
