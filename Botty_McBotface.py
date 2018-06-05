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

import actions as our_actions
from RLBrain import RLBrain
from Learner import GameState
from BuildQueues import BuildingQueue, UnitQueue, ResearchQueue

smart_actions = [
    'no_op',
    'build_building',
    'build_units',
    'build_workers',
    'research',
    'cancel',
    'move_view',
    'attack',
    'defend',
    'patrol',
    'return_to_base'
]

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_SELF = 1
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_NOT_QUEUED = [0]
_SELECT_ALL = [0]

_MAP_SIZE = 128


class Botty(base_agent.BaseAgent):
    def __init__(self):
        super(Botty, self).__init__()
        self.strategy_manager = RLBrain(smart_actions)  # keeping default rates for now.
        self.state = GameState()

        # if we want to have predefined initialization actions, we can hard code values in here.
        self.action_list = []
        self.prev_action = None
        self.prev_state = None
        self.base = 'right'
        self.building_queue = BuildingQueue()
        self.unit_queue = UnitQueue()
        self.research_queue = ResearchQueue()

    def step(self, obs):
        """
        1. reduce state.
        2. Allow brain to learn based prev action, state, & rewards
        3. Choose action based on current state.
        4. Update prev actions & state.
        5. Do action. My current idea is to store many actions in an action list.
           This will allow our abstracted actions to do a lot more per action.
        :param obs: The observation of current step.
        :return: A function ID for SC2 to call.
        """
        super(Botty, self).step(obs)

        # gives us info about where our base is. Left side or right side. Works for 2 base pos maps.
        if not self.prev_state and not self.prev_action:
            self.init_base(obs)

        if self.action_list:
            return self.action_list.pop()

        self.state.update(obs)
        self.reward_and_learn()

        if self.state not in self.strategy_manager.QTable.index:
            self.strategy_manager.add_state(self.state)
            action = self.strategy_manager.choose_action(self.state)
        else:
            action = self.strategy_manager.choose_action(self.state)

        self.prev_state, self.prev_action = self.state, action

        # Gets the abstracted action functions out the actions.py (as our_actions) file.
        action_function = getattr(our_actions, action)

        self.action_list = self.get_action_list(action_function, action, obs)
        return self.action_list.pop()

    def init_base(self, obs):
        """method to set the location of the base."""
        x, y = (obs.observation['minimap'][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()

        if y.any() and y.mean() <= _MAP_SIZE // 2:
            self.base = 'left'
        else:
            self.base = 'right'

    def reward_and_learn(self):
        if self.prev_action and self.prev_state:
            # Update the reward, we going to need to give it to Brain/
            reward = 0

            # Todo finish reward stuff
            self.strategy_manager.learn(self.prev_state, self.state, self.prev_action, reward)

    def transform_location(self, x, x_distance, y, y_distance):
        if self.base == 'right':
            return [x - x_distance, y - y_distance]

        return [x + x_distance, y + y_distance]

    def get_action_list(self, action_function, name, obs):
        """ This function will set up the appropriate args for the various actions."""
        if name == 'no_op':
            return action_function()
        elif name == 'build_building':
            x, y = 0, 0  # TODO Where to put a building
            return action_function(self.building_queue.dequeue(obs), x, y)
        elif name == 'build_units':
            return action_function(self.unit_queue.dequeue(obs))
        elif name == 'build_worker':
            return action_function(actions.FUNCTIONS.Train_Drone_quick.id)
        elif name == 'research':
            return action_function(self.research_queue.dequeue(obs))
        elif name == 'cancel':
            return action_function()  # TODO arg
        elif name == 'move_view':
            pass
        elif name == 'attack':
            return action_function(obs)
        elif name == 'defend':
            pass
        elif name == 'patrol':
            pass
        elif name == 'return_to_base':
            # Need to calc rally_x & rally_y
            pass

        return []


# I FIGURED THIS PAGE WOULD BLOAT DUE TO BOT ANYWAYS SO I'VE MOVED ACTIONS INTO A SEPARATE FILE
# THERE IS ALSO A FILE FOR TESTING ACTIONS. THIS WILL BE A COMPLETELY SEPARATE AGENT.


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
