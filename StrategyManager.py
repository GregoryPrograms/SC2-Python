import numpy as np


class stratBrain:
    def __init__(self, num_states, num_actions, learn_rate, loss_rate, rand_rate, decay):
        self.QTable = np.zeros([num_states, num_actions])
        self.learnR = learn_rate
        self.lossR = loss_rate
        self.randR = rand_rate
        self.Decay = decay

    def choose_action(self, state):
        """This method chooses which action to do."""

    def add_state(self,state):
        """This method gets new state and reward from the environment """

    def learn(self, state,next_state, action, reward):
        """This method will call the action function and use reward to update table."""
