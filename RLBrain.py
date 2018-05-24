import numpy as np
import pandas as pd
import math


class RLBrain:
    MIN_EXP = 0.01
    MIN_LEARN = 0.1

    def __init__(self, reduced_actions=None, decay_rate=0.1):
        """The init method for the brain.
        actions is a list of acitons detailed in botty_mcbotface.py
        I am implementing the QTable as a pandas DataFrame. This is to easily index our Q-table with strings.
        """
        self.actions = reduced_actions  # list of actions
        self.QTable = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.learn_rate = self.learning(0)
        self.decay_rate = decay_rate
        self.rand_rate = self.explore(0)

    def choose_action(self, state):
        """This method chooses which action to do. This method assume check for new states first.
        :returns an action."""
        # .loc constructs a series of action q vales, .idmax() returns the index of the max in a series.
        # The Q values are index by actions in the series, so we return the max action.
        if np.random.uniform() < self.rand_rate:
            return np.random.choice(self.actions)
        else:
            return self.QTable.loc[state, :].idxmax()

    def add_state(self, state):
        """This method gets new state and reward from the environment """
        if state not in self.QTable.index:
            # appends an empty list of labeled floats to the table
            self.QTable = self.QTable.append(
                pd.Series(data=np.zeros(len(self.actions)), index=self.actions, name=state))

    def explore(self, t):
        return max(self.MIN_EXP, min(1.0, 1 - math.log10((t + 1) / 25)))

    def learning(self, t):
        return max(self.MIN_LEARN, min(1.0, 1 - math.log10((t + 1) / 25)))

    def learn(self, state, next_state, action, reward):
        """This method will use the given information to update the q-table."""
        q_value = self.QTable.at[state, action]
        # using pd.series.max to get q-value.
        q_target = reward + self.decay_rate * self.QTable.loc[next_state, :].max()

        self.QTable.at[state, action] += self.learn_rate * (q_target - q_value)

    def read_from_file(self, filename):
        self.QTable = pd.read_csv(filename, index_col=0)

    def write_to_file(self, filename):
        self.QTable.to_csv(filename)
