

import gym
import RLBrain as brain

#actions space is a tuple? I think i want a list
class CartPoleProblem:
    def __init__(self, num_episodes):
        self.episodes = num_episodes
        self.env = gym.make('CartPole-v0')
        self.brain = brain.RLBrain(self.env.action_space)


    def run(self):
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







if __name__ == "__main__":
    tester = CartPoleProblem()
    tester.run()