# This file will contain all actions
# ADD SOME ACTIONS
# SHOULD TAKE IN FULL OBSERVATIONS
# move these to an actions.py?
# Maybe these actions should return a list of functions to be called.
# In our agent we can then use a state machine to iterate through the action list.
# Would allow much more dynamic actions I think.

# Nothing
from pysc2.lib import actions
from pysc2.lib import features

import random

from BuildQueues import Zerg, BuildingQueue, UnitQueue, ResearchQueue

_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_SELF = 1
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_NOT_QUEUED = [0]
_SELECT_ALL = [0]
_NO_OP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_BUILD_SUPPLY_DEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_PLAYER_ID = features.SCREEN_FEATURES.player_id.index

_MAP_SIZE = 128


def no_op(obs):
    """THIS IS THE NO OPERATION ACTION"""
    return [actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])]


# Build actions
def build_building(obs):
    """Build next building in build order.
    Actions will be select drone. Build building. """
    building_actions = []

    units = obs.observation['screen'][_UNIT_TYPE]
    drone_x, drone_y = (units == Zerg.Drone).nonzero()
    if drone_y.any():
        i = random.randint(0, len(drone_y) - 1)
        target = [drone_x[i], drone_y[i]]
        building_actions.append(actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target]))
    else:
        # Can't select a drone. A problem.
        pass

    hatch_x, hatch_y = (units == Zerg.Hatchery).nonzero()

    if hatch_y.any():
        target = [hatch_x.mean(), hatch_y.mean()]
        building_actions.append(actions.FunctionCall(BuildingQueue.dequeue(), [_NOT_QUEUED, target]))


def build_units(obs):
    """Build more units. Maybe separate into military and worker?"""



def build_worker(obs):
    """Build a drone. Send it to the nearest available vespene/mineral."""



def research(obs):
    """get upgrades going. Maybe abstract this into build?"""
    # Research next upgrade in research build order


def cancel(obs):
    """Cancel build queue. To free up resources? May be to complicated of action for learner to consider."""


# View control
def move_view(obs):
    """Move screen/ minimap to see more. This is the action that will fuck us."""


# Unit Control
def attack(obs):
    """General Attack Function."""
    # Have army attack enemy base/enemy army
    # If possible, keep roaches and ultralisks at the front of the army and hydralisks at the rear


def defend(obs):
    """Send units to defensive"""
    # Send army to base
    # Move defensive structures up in priority?


def patrol(obs):
    """Make it part of defend?"""


def return_to_base(obs):
    """Go HOME"""
