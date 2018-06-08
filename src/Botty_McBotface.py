# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Scripted agents."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

import numpy as np
import math
import random

import src.actions as our_actions
from src.RLBrain import RLBrain
from src.Learner import GameState
from src.BuildQueues import BuildingQueue, UnitQueue, ResearchQueue, Zerg

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_SELF = 1
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_NEUTRAL_VESPENE_GEYSER = 342
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_BUILD_EXTRACTOR = actions.FUNCTIONS.Build_Extractor_screen.id
_NOT_QUEUED = [0]
_SELECT_ALL = [0]

_MAP_SIZE = 128
# Size will depend on screen size.
_SIZE_VESPENE = 97

#List of actions that we pass to the AI, reduces state by minimizing # of actions
smart_actions = [
    'no_op',
    'build_building',
    'build_units',
    'build_worker',
    'research',
    'attack',
    'defend',
    'return_to_base'
]

#Map is reduced to squares, equal to size of screen. AI can switch between squares to view different parts of the map.
# Want a Square * Square move view action space.
_SQUARE = 64 / 8
for move_view_x in range(64):
    for move_view_y in range(64):
        if move_view_x % _SQUARE == 0 and move_view_y % _SQUARE == 0:
            smart_actions.append('moveview_' + str(move_view_x) + '_' + str(move_view_y))

# Put in offsets for where to store buildings. Extractor is a special case.
_BUILD_HATCHERY = actions.FUNCTIONS.Build_Hatchery_screen.id
_BUILD_SPAWNING_POOL = actions.FUNCTIONS.Build_SpawningPool_screen.id
_BUILD_SPINE_CRAWLER = actions.FUNCTIONS.Build_SpineCrawler_screen.id
_BUILD_EXTRACTOR = actions.FUNCTIONS.Build_Extractor_screen.id
_BUILD_ROACH_WARREN = actions.FUNCTIONS.Build_RoachWarren_screen.id
_BUILD_LAIR = actions.FUNCTIONS.Morph_Lair_quick.id  # the only quick function, keep separate from queue?
_BUILD_HYDRALISK_DEN = actions.FUNCTIONS.Build_HydraliskDen_screen.id
_BUILD_SPORE_CRAWLER = actions.FUNCTIONS.Build_SporeCrawler_screen.id
_BUILD_EVOLUTION_CHAMBER = actions.FUNCTIONS.Build_EvolutionChamber_screen.id
_BUILD_HIVE = actions.FUNCTIONS.Morph_Hive_quick.id
_BUILD_ULTRA_CAVERN = actions.FUNCTIONS.Build_UltraliskCavern_screen.id

building_offsets = {
    _BUILD_HATCHERY: [0, 0],
    _BUILD_SPAWNING_POOL: [0, 5],
    _BUILD_SPINE_CRAWLER: [6, 0],
    _BUILD_EXTRACTOR: [0, 0],
    _BUILD_ROACH_WARREN: [-4, 1],
    _BUILD_LAIR: [-3, -4],
    _BUILD_HYDRALISK_DEN: [7, -8],
    _BUILD_SPORE_CRAWLER: [6, -4],
    _BUILD_EVOLUTION_CHAMBER: [-4, 3],
    _BUILD_HIVE: [-3, -9],
    _BUILD_ULTRA_CAVERN: [3, -9]
}

## Our 'main'.
# Controls what information is passed to and from the AI.
#
class Botty(base_agent.BaseAgent):

    ##Constructor :- 
    #Initializes the RL brain and the game state
    def __init__(self):
        super(Botty, self).__init__()
        self.strategy_manager = RLBrain(smart_actions)  # keeping default rates for now.
        self.state = GameState()

        # if we want to have predefined initialization actions, we can hard code values in here.
        self.action_list = []
        self.prev_action = None
        self.prev_state = None
        self.prev_killed_units = 0
        self.prev_value_units = 0
        self.prev_mineral_rate = 0
        self.prev_vespene_rate = 0
        self.base = 'right'
        self.building_queue = BuildingQueue()
        self.unit_queue = UnitQueue()
        self.research_queue = ResearchQueue()

    ## Sets the location of the base for use by the AI.
    #  @param self The object pointer calling the function
    #  @param obs The observation maps
    def init_base(self, obs):
        x, y = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()

        if y.any() and y.mean() <= _MAP_SIZE // 2:
            self.base = 'left'
        else:
            self.base = 'right'


    ##  1. Reduce state.
    #   2. Allow brain to learn based prev action, state, & rewards
    #   3. Choose action based on current state.
    #   4. Update prev actions & state.
    #   5. Do action. My current idea is to store many actions in an action list.
    #      This will allow our abstracted actions to do a lot more per action.
    #   @param self The object pointer calling the function.
    #   @param obs The observation of current step.
    #   @return A function ID for SC2 to call.
    def step(self, obs):
        super(Botty, self).step(obs)

        # gives us info about where our base is. Left side or right side. Works for 2 base pos maps.
        if not self.prev_state and not self.prev_action:
            self.init_base(obs)

        if self.action_list:
            turn_action = self.action_list.pop()

            if turn_action in obs.observation['available_actions']:
                return turn_action
            else:
                return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])

        self.state.update(obs)
        self.reward_and_learn(obs)

        if self.state not in self.strategy_manager.QTable.index:
            self.strategy_manager.add_state(self.state)
            action = self.strategy_manager.choose_action(self.state)
        else:
            action = self.strategy_manager.choose_action(self.state)

        self.prev_state, self.prev_action = self.state, action

        # Gets the abstracted action functions out the actions.py (as our_actions) file.

        self.action_list = self.get_action_list(action, obs)
        turn_action = self.action_list.pop()

        if turn_action in obs.observation['available_actions']:
            return turn_action
        else:
            return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])

    ## Takes information about the current game state, creates a 'reward'
    #  based on how good the current state is, and passes the reward to Brain.
    #  @param self The object pointer calling the function
    #  @param obs The observation map.
    def reward_and_learn(self, obs):
        if self.prev_action and self.prev_state:
            # Update the reward, we going to need to give it to Brain/
            killed_units = obs.observation['score_cumulative'][5]
            value_units = obs.observation['player'][4]
            mineral_rate = obs.observation['score_cumulative'][9]
            vespene_rate = obs.observation['score_cumulative'][9]

            reward = 0
            if killed_units > self.prev_killed_units:
                reward += 0.25
            if value_units > self.prev_value_units:
                reward += 0.5
            if mineral_rate > self.prev_mineral_rate:
                reward += -.1
            if vespene_rate > self.prev_vespene_rate:
                reward += 0.15

            self.prev_killed_units = killed_units
            self.prev_value_units = vespene_rate
            self.prev_mineral_rate = mineral_rate
            self.prev_vespene_rate = vespene_rate

            # Todo finish reward stuff
            self.strategy_manager.learn(self.prev_state, self.state, self.prev_action, reward)

    ##Takes in actions, and if the action is one that needs specific parameters, it passes those to it.
    # @param self The object pointer calling the function
    # @param action_str A string containing one of the actions from those available to the AI.
    # @obs The observation maps
    def get_action_list(self, action_str, obs):
        """ This function will set up the appropriate args for the various actions."""
        if 'moveview' in action_str:
            funcall, x, y = action_str.split('_')
            action_function = getattr(our_actions, funcall)
            return action_function(int(x), int(y))

        action_function = getattr(our_actions, action_str)

        if action_str == 'no_op':
            return action_function()
        elif action_str == 'build_building':
            building = self.building_queue.dequeue(obs)
            target = self.get_building_target(obs, building)
            return action_function(obs, building, target)
        elif action_str == 'build_units':
            return action_function(self.unit_queue.dequeue(obs))
        elif action_str == 'build_worker':
            return action_function(actions.FUNCTIONS.Train_Drone_quick.id)
        elif action_str == 'research':
            return action_function(self.research_queue.dequeue(obs))
        elif action_str == 'attack':
            return action_function(obs)
        elif action_str == 'defend':
            unit_type = obs.observation['screen'][_UNIT_TYPE]
            hatchery_x, hatchery_y = (unit_type == Zerg.Hatchery).nonzero()
            return action_function(hatchery_x.mean() + 10, hatchery_y.mean() + 10)
        elif action_str == 'return_to_base':
            unit_type = obs.observation['screen'][_UNIT_TYPE]
            hatchery_x, hatchery_y = (unit_type == Zerg.Hatchery).nonzero()
            return action_function(hatchery_x + 10, hatchery_y + 10)

        return [actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])]

    ## Whenever we build a building, we call this function. If it is a 
    # building with special requirements, we fullfill those. 
    # We also use offset to make sure the building does not overlap with any other buildings.
    # @param obs The observation maps
    # @param building A macro used to refer to specific buildings.
    # @return The location where we are building.
    @staticmethod
    def get_building_target(obs, building):
        unit_type = obs.observation['screen'][_UNIT_TYPE]
        if building == _BUILD_EXTRACTOR:
            vespene_y, vespene_x = (unit_type == _NEUTRAL_VESPENE_GEYSER).nonzero()
            # Two options. Use a classifier to group vespene coordinates,
            # OR we can choose randomly and hope we don't get a unit.
            # For now I will do the later.
            i = random.randint(0, len(vespene_y) - 1)
            return [vespene_x[i], vespene_y[i]]
        else:
            # Building may not pass into dict correctly as a key.
            x_offset, y_offset = building_offsets[building]
            hatchery_x, hatchery_y = (unit_type == Zerg.Hatchery).nonzero()
            return [hatchery_x.mean() + x_offset, hatchery_y.mean() + y_offset]

    ## Called in order to move a set of coordinates by some distance, depending
    # on whether the base is on the right or left side of the map.
    # @param self The object pointer calling the function
    # @param x The initial x
    # @param x_distance The distance between the initial and final x
    # @param y The initial y
    # @param y_distance The distance between the initial and final y
    # @return The transformed x and y.
    def transform_location(self, x, x_distance, y, y_distance):
        if self.base == 'right':
            return [x - x_distance, y - y_distance]

        return [x + x_distance, y + y_distance]


# I FIGURED THIS PAGE WOULD BLOAT DUE TO BOT ANYWAYS SO I'VE MOVED ACTIONS INTO A SEPARATE FILE

class DefeatRoaches(base_agent.BaseAgent):
    """An agent specifically for solving the DefeatRoaches map."""

    def step(self, obs):
        super(DefeatRoaches, self).step(obs)
        if _ATTACK_SCREEN in obs.observation["available_actions"]:
            player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
            roach_y, roach_x = (player_relative == _PLAYER_HOSTILE).nonzero()
            if not roach_y.any():
                return actions.FunctionCall(_NO_OP, [])
            index = np.argmax(roach_y)
            target = [roach_x[index], roach_y[index]]
            return actions.FunctionCall(_ATTACK_SCREEN, [_NOT_QUEUED, target])
        elif _SELECT_ARMY in obs.observation["available_actions"]:
            return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
        else:
            return actions.FunctionCall(_NO_OP, [])


class MoveToBeacon(base_agent.BaseAgent):
    """An agent specifically for solving the MoveToBeacon map."""

    def step(self, obs):
        super(MoveToBeacon, self).step(obs)
        if _MOVE_SCREEN in obs.observation["available_actions"]:
            player_relative = obs.observation["screen"][_PLAYER_RELATIVE]
            neutral_y, neutral_x = (player_relative == _PLAYER_NEUTRAL).nonzero()
            if not neutral_y.any():
                return actions.FunctionCall(_NO_OP, [])
            target = [int(neutral_x.mean()), int(neutral_y.mean())]
            return actions.FunctionCall(_MOVE_SCREEN, [_NOT_QUEUED, target])
        else:
            return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])
