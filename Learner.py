import asyncio

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features


## class GameState
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

    ##Constructor, initializes the returned list.
    def __init__(self, obs=None):
        self.creep = obs.observation.feature_screen.creep
        self.unit_type = obs.observation.feature_screen.unit_type
        self.selected = obs.observation.feature_screen.selected
        self.minerals = obs.player_common.minerals
        self.vespene = obs.player_common.vespene
        self.availFood = obs.player_common.food_cap
        self.armyCount = 0
        self.larvaCount = 0
        self.state = [self.creep, self.unit_type, self.selected,
                      self.minerals, self.vespene, self.availFood, self.armyCount, self.larvaCount]

    ## update(self,obs)
    # @param self The object pointer
    # @param obs The observation maps
    def update(self, obs):
        self.creep = obs.observation.feature_screen.creep
        self.unit_type = obs.observation.feature_screen.unit_type
        self.selected = obs.observation.feature_screen.selected
        self.minerals = obs.player_common.minerals
        self.vespene = obs.player_common.vespene
        self.availFood = obs.player_common.food_cap - obs.player_common.food_used
        self.armyCount = obs.player_common.army_count
        self.larvaCount = obs.player_common.larva_count
        self.state = [self.creep, self.player_relative, self.unit_type, self.selected,
                      self.minerals, self.vespene, self.availFood, self.armyCount, self.larvaCount]


def point_val(self):
    a = self.unit_type.iteritems[]
