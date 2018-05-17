
from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

# Building Macros
_BUILD_HATCHERY = actions.FUNCTIONS.Build_Hatchery_screen.id
_BUILD_SPAWNING_POOL = actions.FUNCTIONS.Build_SpawningPool_screen.id
_BUILD_SPINE_CRAWLER = actions.FUNCTIONS.Build_SpineCrawler_screen.id
_BUILD_EXTRACTOR = actions.FUNCTIONS.Build_Extractor_screen_screen.id
_BUILD_ROACH_WARREN = actions.FUNCTIONS.Build_RoachWarren_screen.id
_BUILD_LAIR = actions.FUNCTIONS.Morph_Lair_quick.id
    #from Hatchery
_BUILD_HYDRALISK_DEN = actions.FUNCTIONS.Build_HydraliskDen_screen.id
_BUILD_SPORE_CRAWLER = actions.FUNCTIONS.Build_SporeCrawler_screen.id


# Building Queue
class BuildingQueue:
    # Build order:
    # Hatchery: return Actions.FunctionCall('Build_Hatchery_screen', cmd_screen, 1152)
    # Spawning Pool
    # Spine crawler
    # Extractor
    # Roach Warren
    # Extractor x3
    # Lair
    # Hydralisk Den
    # Spore Crawler
    # Hatchery

    def _init_(self):
        """Set build order"""

    def dequeue(self):
        """dequeue"""

    def enqueue(self):
        """enqueue"""


# Unit Macros
_TRAIN_QUEEN = actions.FUNCTIONS.Train_Queen_quick.id
_TRAIN_ZERGLING = actions.FUNCTIONS.Train_Zergling_quick.id
_TRAIN_ROACH = actions.FUNCTIONS.Train_Roach_quick.id
_TRAIN_HYDRALISK = actions.FUNCTIONS.Train_Hydralisk_quick.id

# Unit Queue

class UnitQueue:
    # Military Build order:
    # Queen
    # Zerglings
    # Roaches
    # Hydralisks

    def _init_(self):
        """Set build order"""

    def dequeue(self):
        """dequeue"""

    def enqueue(self):
        """enqueue"""


# Research Macros
_RESEARCH_METABOLIC_BOOST = actions.FUNCTIONS.Research_ZerglingMetabolicBoost_quick.id
_RESEARCH_GLIAL = actions.FUNCTIONS.Research_GlialRegeneration_quick.id
    #closest thing I could find to glial reconstitution in the actions list
_RESEARCH_ZERG_MISSILE_WEAPONS = actions.FUNCTIONS.Research_ZergMissileWeapons_quick.id
_RESEARCH_ZERG_MISSILE_LVL1 = actions.FUNCTIONS.Research_ZergMissileWeaponsLevel1_quick.id
_RESEARCH_ZERG_MISSILE_LVL2 = actions.FUNCTIONS.Research_ZergMissileWeaponsLevel2_quick.id
_RESEARCH_GROOVED_SPINES = actions.FUNCTIONS.Research_GroovedSpines_quick.id

# Research Queue

class ResearchQueue:
    # Order:
    # Metabolic Boost
    # Glial reconstitution
    # Zerg Missile Attacks level 1
    # Grooved Spines
    # Zerg Missile Attacks level 2
    def _init_(self):
        """"""

    def dequeue(self):
        """"""

    def enqueue(self):
        """"""
