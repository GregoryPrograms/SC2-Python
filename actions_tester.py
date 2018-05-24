# A file for agents to test particular actions


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

import numpy as np

import actions


class ActionTester(base_agent.BaseAgent):
    """"Another bot that will be used to test actions. Probably run in mini-games and whatnot."""

    def __init__(self):
        super(ActionTester, self).__init__()

    def step(self, obs):
        super(ActionTester, self).step(obs)
