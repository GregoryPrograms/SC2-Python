import asyncio

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

unitIDS = [(311, "Adept"), (141, "Archon"), (9, "Baneling"), (55, "Banshee"), (57, "Battlecruiser"),
           (114, "Brood Lord"), (79, "Carrier"), (4, "Colossus"), (112, "Corruptor"), (692, "Cyclone"),
           (76, "Dark Templar"), (694, "Disruptor"), (104, "Drone"), (50, "Ghost"), (, "Hellbat"), (53, "Hellion"),
           (75, "High Templar"), (107, "Hydralisk"), (83, "Immortal"), (111, "Infestor"), (85, "Interceptor"),
           (151, "Larva"), (689, "Liberator"), (502, "Lurker"), (51, "Marauder"), (48, "Marine"), (54, "Medivac"),
           (10, "Mothership"), (108, "Mutalisk"), (, "Nydus Worm"), (82, "Observer"), (495, "Oracle"),
           (106, "Overlord"), (129, "Overseer"), (78, "Phoenix"), (84, "Probe"), (126, "Queen"), (688, "Ravager"),
           (56, "Raven"), (49, "Reaper"), (110, "Roach"), (45, "SCV"), (77, "Sentry"), (33, "Siege Tank"),
           (74, "Stalker"), (494, "Swarm Host"), (496, "Tempest"), (52, "Thor"), (109, "Ultralisk"), (35, "Viking"),
           (499, "Viper"), (80, "Void Ray"), (81, "Warp Prism"), (498, "Widow Mine"), (73, "Zealot"), (105, "Zergling")]


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

    def __init__(self, obs=None):
        self.creep = obs.observation.feature_screen.creep
        self.player_relative = obs.observation.feature_screen.player_relative
        self.unit_type = obs.observation.feature_screen.unit_type
        self.selected = obs.observation.feature_screen.selected
        self.minerals = obs.player_common.minerals
        self.vespene = obs.player_common.vespene
        self.availFood = obs.player_common.food_cap
        self.armyCount = 0
        self.larvaCount = 0
        self.state = [self.creep, self.player_relative, self.unit_type, self.selected,
                      self.minerals, self.vespene, self.availFood, self.armyCount, self.larvaCount]

    def update(self, obs):
        self.creep = obs.observation.feature_screen.creep
        self.player_relative = obs.observation.feature_screen.player_relative
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
