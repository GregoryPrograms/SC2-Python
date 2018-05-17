import numpy as np
import pandas as pd


class RLBrain:
    def __init__(self, reduced_actions=None, learn_rate=0.1, decay_rate=0.9, rand_rate=0.1):
        """The init method for the brain.
        actions is a list of acitons detailed in botty_mcbotface.py
        I am implementing the QTable as a pandas DataFrame. This is to easily index our Q-table with strings.
        """
        self.actions = reduced_actions  # list of actions
        self.QTable = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.learn_rate = learn_rate
        self.decay_rate = decay_rate
        self.rand_rate = rand_rate

    def choose_action(self, state):
        """This method chooses which action to do. This method assume check for new states first.
        :returns an action."""
        # .loc constructs a series of action q vales, .idmax() returns the index of the max in a series.
        # The Q values are index by actions in the series, so we return the max action.
        return np.random.choice(self.actions) if np.random.uniform() < self.randR else self.QTable.loc[state, :].idmax()

    def add_state(self, state):
        """This method gets new state and reward from the environment """
        if state not in self.QTable.index:
            # appends an empty list of labeled floats to the table
            self.QTable = self.QTable.append(pd.Series(np.zeros(self.actions.len())), index=self.actions,
                                             dytpe=np.float64)

    def learn(self, state, next_state, action, reward):
        """This method will use the given information to update the q-table."""
        q_value = self.QTable.loc(state, action)
        # using pd.series.max to get q-value.
        q_target = reward + self.decay_rate * self.QTable.loc[next_state, :].max()

        self.QTable.loc[state, action] += self.learn_rate * (q_target - q_value)
