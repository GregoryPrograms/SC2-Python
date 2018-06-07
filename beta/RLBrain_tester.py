"""
This is a separate test file for purposed of making sure the RL-brain can solve a problem it easily should be able to.
This is an attempt to solve the cartpole problem, detailed here: https://gym.openai.com/envs/CartPole-v1/

I am using the openAI gym to for the environment.
"""

import gym

import numpy as np

import RLBrain as brain

import math

from time import sleep


# actions space is a tuple? I think i want a list
class CartPoleProblem:
    NUM_BUCKET = [2, 1, 6, 3]
    new_agent = True

    def __init__(self, num_episodes=500):
        self.episodes = num_episodes
        self.env = gym.make('CartPole-v0')
        self.brain = brain.RLBrain([0, 1])
        self.solved = False
        self.state_bounds = list(zip(self.env.observation_space.low, self.env.observation_space.high))
        self.state_bounds[3] = [-math.radians(50), math.radians(50)]
        self.state_bounds[1] = [-0.5, 0.5]
        self.solved_last = False

    def get_state(self, obs):
        """In the cartpole problem, obs space is continuous. This method makes it discrete.
           Used the following reference for reducing state.
           https://medium.com/@tuzzer/cart-pole-balancing-with-q-learning-b54c6068d947 """
        buckets = []
        for i in range(len(obs)):
            if obs[i] <= self.state_bounds[i][0]:
                bucket_index = 0
            elif obs[i] >= self.state_bounds[i][1]:
                bucket_index = self.NUM_BUCKET[i]
            else:
                width = self.state_bounds[i][1] - self.state_bounds[i][0]
                offset = (self.NUM_BUCKET[i]) * self.state_bounds[i][0] / width
                scale = (self.NUM_BUCKET[i]) / width
                bucket_index = int(round(scale * obs[i] - offset))
            buckets.append(bucket_index)
        return buckets

    def run(self):
        if not self.new_agent:
            self.brain.read_from_file_QT('cart_pole.txt')
        score_list = []
        solved = 0
        print(self.brain.QTable.to_string())
        for e in range(self.episodes):

            current_state = str(self.get_state(self.env.reset()))

            done = False
            i = 0

            while not done:
                self.env.render()
                if current_state not in self.brain.QTable.index:
                    self.brain.add_state(current_state)
                    action = self.brain.choose_action(current_state)
                else:
                    action = self.brain.choose_action(current_state)

                observation, reward, done, _ = self.env.step(action)
                next_state = str(self.get_state(observation))

                if next_state not in self.brain.QTable.index:
                    self.brain.add_state(next_state)
                self.brain.learn(current_state, next_state, action, reward)
                current_state = next_state
                i += 1
            self.brain.rand_rate = self.brain.explore(e)
            self.brain.learn_rate = self.brain.learning(e)

            score_list.append(i)
            print("Ran {} episodes, time {}, solved: {}".format(e, i, self.solved))

            if self.solved_last and i > 195:
                solved += 1
            elif i > 195:
                solved = 1
                self.solved_last = True
            else:
                solved = 0
                self.solved_last = 0

            if solved > 100:
                print("Have a Working Agent!")
                self.brain.write_to_file_QT('cart_pole.txt')
                break
            # solved += 1
        print("Ran {} episodes, solved: {}".format(1, self.solved))


if __name__ == "__main__":
    tester = CartPoleProblem()
    tester.run()
