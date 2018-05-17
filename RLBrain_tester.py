"""
This is a separate test file for purposed of making sure the RL-brain can solve a problem it easily should be able to.
This is an attempt to solve the cartpole problem, detailed here: https://gym.openai.com/envs/CartPole-v1/

I am using the openAI gym to for the environment.
"""

import gym
import numpy as np
import RLBrain as brain


# actions space is a tuple? I think i want a list
class CartPoleProblem:
    def __init__(self, num_episodes=100):
        self.episodes = num_episodes
        self.env = gym.make('CartPole-v0')
        self.brain = brain.RLBrain(self.env.action_space)
        self.solved = False

    def get_state(self, obs):
        """In the cartpole problem, obs space is continuous. This method makes it discrete."""
        # TODO finish method
        return obs

    def run(self):
        score_list = []
        for e in range(self.episodes):
            current_state = self.get_state(self.env.reset())

            done = False
            i = 0

            while not done:
                if current_state not in self.brain.QTable.index:
                    self.brain.add_state(current_state)
                    action = self.brain.choose_action(current_state)
                else:
                    action = self.brain.choose_action(current_state)

                observation, reward, done, _ = self.env.step(action)
                next_state = self.get_state(observation)
                self.brain.learn(current_state, next_state, action, reward)
                i += 1

            score_list.append(i)
            # TODO exit condition based on the score

        print("Ran {} episodes, solved: {}".format(e, self.solved))


if __name__ == "__main__":
    tester = CartPoleProblem()
    tester.run()
