# This file will contain all actions
# ADD SOME ACTIONS
# SHOULD TAKE IN FULL OBSERVATIONS
# move these to an actions.py?
# Maybe these actions should return a list of functions to be called.
# In our agent we can then use a state machine to iterate through the action list.
# Would allow much more dynamic actions I think.


# Nothing
def no_op(obs):
    """THIS IS THE NO OPERATION ACTION"""
    return  # Something not zero?


# Build actions
def build_building(obs):
    """Build next building in build order"""


def build_units(obs):
    """Build more units. Maybe separate into military and worker?"""


def research(obs):
    """get upgrades going. Maybe abstract this into build?"""


def cancel(obs):
    """Cancel build queue. To free up resources? May be to complicated of action for learner to consider."""


# View control
def move_view(obs):
    """Move screen/ minimap to see more. This is the action that will fuck us."""


# Unit Control
def attack(obs):
    """General Attack Function."""


def defend(obs):
    """Send units to defensive"""


def patrol(obs):
    """Make it part of defend?"""


def return_to_base(obs):
    """Go HOME"""
