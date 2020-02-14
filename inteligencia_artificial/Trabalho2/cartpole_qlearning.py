# Author: gabri
# File: cartpole_qlearning
# Date: 23/10/2019
# Made with PyCharm

# Standard Library
from random import randint
import json
import time
import threading

# Third party modules
import requests
import numpy as np
import gym
import matplotlib.pyplot as plt


class CartPoleQLearning:
    def __init__(self, num_actions=2, alpha=0.9, gamma=0.95,
                 epsilon=1.0, epsilon_decay_rate=0.99, min_epsilon=0.05):
        self.states_ranges = [
            (-2.4, 2.4, 4),
            (-3.0, 3.0, 5),
            (0.20943951, -0.20943951, 7),
            (-3.0, 4.0, 5)
        ]

        self.discr_states = [
            np.linspace(min_value, max_value, n)
            for min_value, max_value, n in self.states_ranges
        ]

        self.max_states = max(len(state_range) for state_range in self.discr_states)
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay_rate = epsilon_decay_rate
        self.control_url = "http://localhost:8081/?control="

    def reward(self):
        if self.done and not self.steps == self.max_steps:
            return -1
        else:
            return 0

    def get_state_position(self, state):
        state_pos = sum([np.digitize([state[i]], self.discr_states[i]) * (self.max_states + 1) ** i
                      for i in range(len(state))])
        return state_pos

    def init_q(self):
        self.num_states = (self.max_states + 1) ** len(self.discr_states)
        self.q = np.zeros((self.num_states, self.num_actions))

    def init_state(self):
        response = requests.get(url="http://localhost:8081/?state=0").json()
        print(response['state'])
        self.cont_s = response['state']
        self.done = False

    def act(self):
        explore = (1 - self.epsilon) <= np.random.uniform(0, 1)
        if explore:
            self.a = np.random.randint(0, self.num_actions)
        else:
            self.a = np.argmax(self.q[self.s, :])

        response = requests.get(url=self.control_url + str(self.a)).json()
        self.cont_s_ = response['state']
        self.done = response['done']

    def update_utility(self):
        r = self.reward()
        self.q[self.s, self.a] = self.q[self.s, self.a] + self.alpha * \
                                 (r + self.gamma * self.q[self.s_, self.a_] - self.q[self.s, self.a])
        self.cont_s, self.a = self.cont_s_, self.a_

    def learn(self, episodes=5000, steps_per_episode=1000):
        self.init_q()
        self.max_steps = steps_per_episode
        self.init_state()
        # plt.ion()
        # plt.show()
        self.last_steps = 0
        for episode in range(episodes):
            self.steps = 0
            while self.steps < steps_per_episode:
                # Escolher uma acao a no estado s'
                self.s = self.get_state_position(self.cont_s)
                self.act()
                self.s_ = self.get_state_position(self.cont_s_)
                self.a_ = np.argmax(self.q[self.s_, :])
                self.update_utility()
                self.steps += 1
                if self.done:
                    print(f"{self.steps} steps in episode {episode} | "
                          f"epsilon: {self.epsilon}")
                    # plt.plot([episode, episode + 1], [self.last_steps, self.steps], 'b')
                    # plt.show()
                    # plt.pause(0.001)
                    self.last_steps = self.steps
                    if self.epsilon >= self.min_epsilon:
                        self.epsilon *= self.epsilon_decay_rate
                    break
        # plt.ioff()
        # plt.show()

    def test(self, episodes=100, steps_per_episode=1000):
        self.epsilon = 0
        self.max_steps = steps_per_episode
        self.init_q()
        self.init_state()
        plt.ion()
        plt.show()
        self.last_steps = 0
        for episode in range(episodes):
            self.steps = 0
            while self.steps < steps_per_episode:
                # Escolher uma acao a no estado s'
                self.act()
                self.a_ = np.argmax(self.q[self.s_, :])
                self.steps += 1
                if self.done:
                    print(f"{self.steps} steps in episode {episode} | "
                          f"epsilon: {self.epsilon}")
                    plt.plot([episode, episode + 1], [self.last_steps, self.steps], 'b')
                    plt.show()
                    plt.pause(0.001)
                    self.last_steps = self.steps
                    if self.epsilon >= self.min_epsilon:
                        self.epsilon *= self.epsilon_decay_rate
                    break
        plt.ioff()
        plt.show()


def main():
    env = CartPoleQLearning()
    env.learn()
    env.test()


if __name__ == "__main__":
    main()
