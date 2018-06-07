# import asyncio

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

import math

import numpy as np

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_SELF = 1
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_MAP_SIZE = 128


# class GameState
#
#  Used to represent the current state of the game.
#  Takes necessary information from the SC2 API,
#  and shares it with the RL bot.
class GameState:
    # creep
    # player_relative
    # unit_type
    # selected
    # unit_density
    # minerals
    # vespene
    # availFood
    # armyCount
    # larvaCount
    # state

    # Constructor, initializes the returned list.
    def __init__(self, obs=None):
        self.minerals = None
        self.vespene = None
        self.availFood = None
        self.armyCount = 0
        self.larvaCount = 0

    #  update(self,obs)
    # @param self The object pointer
    # @param obs The observation maps
    def update(self, obs):
        enemy_x, enemy_y = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_HOSTILE).nonzero()
        ally_x, ally_y = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_FRIENDLY).nonzero()

        # Nothing is 0. Enemies only is 1. Allies only is 2. Both is 3.
        squares = np.zeros(16)
        for i in range(len(enemy_y)):
            e_y = int(math.ceil((enemy_y[i] + 1) / (_MAP_SIZE / 4))) - 1
            e_x = int(math.ceil((enemy_x[i] + 1) / (_MAP_SIZE / 4))) - 1

            squares[(e_y * 4) + e_x] += 1

        for i in range(len(ally_y)):
            a_y = int(math.ceil((ally_y[i] + 1) / (_MAP_SIZE / 4))) - 1
            a_x = int(math.ceil((ally_x[i] + 1) / (_MAP_SIZE / 4))) - 1

            squares[(a_y * 4) + a_x] += 2

        self.minerals = obs.observation['player'][1]
        self.vespene = obs.observation['player'][2]
        self.availFood = obs.observation['player'][4] - obs.observation['player'][3]
        self.armyCount = obs.observation['player'][8]
        self.larvaCount = obs.observation['player'][10]
        return [squares,
                self.minerals, self.vespene, self.availFood, self.armyCount, self.larvaCount]


def point_val(self):
    # a = self.unit_type.iteritems[]
    pass
