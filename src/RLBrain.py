import numpy as np
import pandas as pd
import math

##class that holds the reinforcement learning for our program.
#
class RLBrain:
    MIN_EXP = 0.01
    MIN_LEARN = 0.1
    
    ##Constructor:-
    #Takes in the list of actions, and sets the decay, learn, and random rates.
    def __init__(self, reduced_actions=None, decay_rate=0.1):
        """The init method for the brain.
        actions is a list of actions detailed in Botty_McBotface.py
        I am implementing the QTable as a pandas DataFrame. This is to easily index our Q-table with strings.
        """
        self.actions = reduced_actions  # list of actions
        self.QTable = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.learn_rate = self.learning(0)
        self.decay_rate = decay_rate
        self.rand_rate = self.explore(0)
    
    ## Chooses which action to carry out.	
    # @param self Object pointer calling the function.
    # @param state Gamestate information.
    # @return The chosen action.
    def choose_action(self, state):
        """This method chooses which action to do. This method assume check for new states first.
        :returns an action."""
        # .loc constructs a series of action q vales, .idmax() returns the index of the max in a series.
        # The Q values are index by actions in the series, so we return the max action.
        if np.random.uniform() < self.rand_rate:
            return np.random.choice(self.actions)
        else:
            return self.QTable.loc[state, :].idxmax()

    ## Gets a new state + reward.
    # @param self Object pointer calling the function.
    # @param state Gamestate information.
    def add_state(self, state):
        """This method gets new state and reward from the environment """
        if state not in self.QTable.index:
            # appends an empty list of labeled floats to the table
            self.QTable = self.QTable.append(
                pd.Series(data=np.zeros(len(self.actions)), index=self.actions, name=state))

    ## Finds the rate at which random states are chosen.
    # @param self Object pointer calling the function.
    # @param t Number of states explored so far.
    def explore(self, t):
        return max(self.MIN_EXP, min(1.0, 1 - math.log10((t + 1) / 25)))

    ## Finds the rate at which the RL bot learns.
    # @param self Object pointer calling the function.
    # @param t Number of states explored so far.
    def learning(self, t):
        return max(self.MIN_LEARN, min(1.0, 1 - math.log10((t + 1) / 25)))

    ## Learns the value of a state transition, stores it in q-table.
    # @param self Object pointer calling the function.
    # @param state First of the two states in the state transition being learned.
    # @param next_state Second of the two states in the state transition being learned.
    # @param action Action that was taken that transitioned between the two states.
    # @param reward Reward for the action.
    def learn(self, state, next_state, action, reward):
        """This method will use the given information to update the q-table."""
        q_value = self.QTable.at[state, action]
        # using pd.series.max to get q-value.
        q_target = reward + self.decay_rate * self.QTable.loc[next_state, :].max()

        self.QTable.at[state, action] += self.learn_rate * (q_target - q_value)

    ## Reads a QTable from a file for the RL bot.
    # @param self Object pointer calling the function.
    # @filename Name of the file being read from.
    def read_from_file_QT(self, filename):
        self.QTable = pd.read_csv(filename, index_col=0)

    ## Allows us to store a QTable in a file.
    # @param self Object pointer calling the function.
    # @param filename Name of the file being written to.
    def write_to_file_QT(self, filename):
        self.QTable.to_csv(filename)

    ## Gets the size of the current QTable.
    # @param self Object pointer calling the function.
    def get_size(self):
        print(self.QTable.shape)

    def read_from_file_states(self, filename):
        pass

    def write_to_file_states(self, filename):
        pass
