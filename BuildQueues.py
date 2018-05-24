import asyncio

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

# Global Tracking vars
num_bases = 1
num_queens = 0
have_roach_warren = False
have_spawning_pool = False
have_hydra_den = False
have_evo = False
have_lair = False

# Building Macros
_BUILD_HATCHERY = actions.FUNCTIONS.Build_Hatchery_screen.id
_BUILD_SPAWNING_POOL = actions.FUNCTIONS.Build_SpawningPool_screen.id
_BUILD_SPINE_CRAWLER = actions.FUNCTIONS.Build_SpineCrawler_screen.id
_BUILD_EXTRACTOR = actions.FUNCTIONS.Build_Extractor_screen_screen.id
_BUILD_ROACH_WARREN = actions.FUNCTIONS.Build_RoachWarren_screen.id
_BUILD_LAIR = actions.FUNCTIONS.Morph_Lair_quick.id  # the only quick function, keep separate from queue?
# from Hatchery
_BUILD_HYDRALISK_DEN = actions.FUNCTIONS.Build_HydraliskDen_screen.id
_BUILD_SPORE_CRAWLER = actions.FUNCTIONS.Build_SporeCrawler_screen.id
_BUILD_EVOLUTION_CHAMBER = actions.FUNCTIONS.Build_EvolutionChamber_screen.id

# Building Queue # Unit Queue (need list? to change the priorities)
# tuples for buildings:

hatchery = (1, _BUILD_HATCHERY)
spawning_pool = (2, _BUILD_SPAWNING_POOL)
spine_crawler = (3, _BUILD_SPINE_CRAWLER)
extractor = (4, _BUILD_EXTRACTOR)
roach_warren = (5, _BUILD_ROACH_WARREN)
evo = (6, _BUILD_EVOLUTION_CHAMBER)
hydra_den = (8, _BUILD_HYDRALISK_DEN)
spore_crawler = (9, _BUILD_SPORE_CRAWLER)
lair = (7, _BUILD_LAIR)


class BuildingQueue:
    # Build order:
    # Hatchery:
    # Spawning Pool
    # Spine crawler
    # Extractor
    # Roach Warren
    # Evolution Chamber (needed for research)
    # Extractor x3
    # Lair
    # Hydralisk Den
    # Spore Crawler
    # find new base

    def _init_(self):
        # use priority queue? in case buildings are destroyed
        self.BuildQ = [hatchery, spawning_pool, spine_crawler, extractor, roach_warren, evo, lair, hydra_den,
                       spore_crawler]

    def dequeue(self):
        # agent will handle the actually function call, we are just passing back the function id

        # repeated: hatchery, spine_crawler, spore crawler, extractor
        # everything else just need one of
        max = 0
        target_build = ''

        for i in len(self.BuildQ):
            if max < self.BuildQ[i][0]:
                max = self.BuildQ[i][0]
                target_build = self.BuildQ[i][1]

        return target_build

    def update(self):

        if not have_evo:
            self.BuildQ[5][0] = 3
        if not have_roach_warren:
            self.BuildQ[4][0] = 4
        if not have_spawning_pool:
            self.BuildQ[1][0] = 5
        if not have_hydra_den:
            self.BuildQ[7][0] = 1
        if not have_lair:
            self.BuildQ[6][0] = 2

        # update further based on game state


# Unit Macros
_TRAIN_QUEEN = actions.FUNCTIONS.Train_Queen_quick.id
_TRAIN_ZERGLING = actions.FUNCTIONS.Train_Zergling_quick.id
_TRAIN_ROACH = actions.FUNCTIONS.Train_Roach_quick.id
_TRAIN_HYDRALISK = actions.FUNCTIONS.Train_Hydralisk_quick.id
_TRAIN_WORKER = actions.FUNCTIONS.Train_Drone_quick.id
_TRAIN_OVERLORD = actions.FUNCTIONS.Train_Overlord_quick.id

# DO NOT USE TUPLES, THIS IS FOR MODELING PURPOSES ONLY
queen = (0, _TRAIN_QUEEN)
zergling = (0, _TRAIN_ZERGLING)
roach = (0, _TRAIN_ROACH)
hydra = (0, _TRAIN_HYDRALISK)
worker = (0, _TRAIN_WORKER)
overlord = (0, _TRAIN_OVERLORD)


# Unit Queue (need list? to change the priorities)

class UnitQueue:
    # Military Build order:
    # Queen (every time a new base is built)
    # Zerglings
    # Roaches
    # Hydralisks
    # Overlord (only when supply is low i.e. max supply - current supply < supply required for next unit)

    # new Hatchery means build queen
    # queen should be at the top in priority

    # Move military units to top of priority queue as they become available? I.e. zerglings once spawning pool
    # is up, roaches once roach warren is up, hydralisks once hydralisk den is up, etc.

    # Also move queen to top of priority queue when a new hatchery is built, and overlord when more supply is needed.

    # zerglings for early game only
    # roaches only when roach warren achieved
    # interchange roaches and hydralisks depending on strategy

    def _init_(self):
        """Set build order"""
        self.UnitQ = [queen, zergling, roach, hydra, worker, overlord]

    def dequeue(self):

        # early game: if we dequeue a zergling and we don't have roach warren
        # then keeping enqueuing zerglings

        # mid-game: roaches only when roach warren is present

        # hydralisks?

        # get max priority unit, update list

        # access list like a 2D array
        max = 0
        target_unit = ''

        for i in len(self.UnitQ):
            if max < self.UnitQ[i][0]:
                max = self.UnitQ[i][0]
                target_unit = self.UnitQ[i][1]

        return target_unit

    def update(self):
        # need to optimize so one unit does not outpace another
        # queen for every base (running total of num bases)
        if num_bases > num_queens:
            self.UnitQ[0][0] = 100
        # roaches go up with warren built (warren)
        if have_roach_warren:
            self.UnitQ[2][0] += 2
        # same for zergling and hydralisk (spawn pool, hydra den)
        if have_spawning_pool:
            self.UnitQ[1][0] += 1
        if have_hydra_den:
            self.UnitQ[3][0] += 3

        # overlord max if need more supplies, otherwise lowest
        # if max supply - current supply < supply required for next unit:
        # self.BuildQ[5][0] = very high


# Research Macros
_RESEARCH_METABOLIC_BOOST = actions.FUNCTIONS.Research_ZerglingMetabolicBoost_quick.id
_RESEARCH_GLIAL = actions.FUNCTIONS.Research_GlialRegeneration_quick.id
# closest thing I could find to glial reconstitution in the actions list
_RESEARCH_ZERG_MISSILE_WEAPONS = actions.FUNCTIONS.Research_ZergMissileWeapons_quick.id
# I'm assuming this is needed before missile levels can be achieved
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
        self.ResearchQ = asyncio.Queue()
        self.ResearchQ.put(_RESEARCH_METABOLIC_BOOST)
        self.ResearchQ.put(_RESEARCH_GLIAL)
        self.ResearchQ.put(_RESEARCH_ZERG_MISSILE_WEAPONS)
        self.ResearchQ.put(_RESEARCH_ZERG_MISSILE_WEAPONS)
        self.ResearchQ.put(_RESEARCH_ZERG_MISSILE_LVL1)
        self.ResearchQ.put(_RESEARCH_GROOVED_SPINES)
        self.ResearchQ.put(_RESEARCH_ZERG_MISSILE_LVL2)

    def dequeue(self):
        # check if in available actions before dequeuing
        return self.ResearchQ.get_nowait()

    def enqueue(self, order):
        self.ResearchQ.put_nowait(order)
