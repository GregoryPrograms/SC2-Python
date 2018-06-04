import asyncio

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

# Misc. Actions
_NOOP = actions.FUNCTIONS.no_op.id

# Global Tracking vars
num_bases = 1
num_queens = 0
have_roach_warren = False
have_spawning_pool = False
have_hydra_den = False
have_evo = False
have_lair = False
have_hive = False
have_ultra_cavern = False

# Building Macros
_BUILD_HATCHERY = actions.FUNCTIONS.Build_Hatchery_screen.id
_BUILD_SPAWNING_POOL = actions.FUNCTIONS.Build_SpawningPool_screen.id
_BUILD_SPINE_CRAWLER = actions.FUNCTIONS.Build_SpineCrawler_screen.id
_BUILD_EXTRACTOR = actions.FUNCTIONS.Build_Extractor_screen_screen.id
_BUILD_ROACH_WARREN = actions.FUNCTIONS.Build_RoachWarren_screen.id
_BUILD_LAIR = actions.FUNCTIONS.Morph_Lair_quick.id  # the only quick function, keep separate from queue?
_BUILD_HYDRALISK_DEN = actions.FUNCTIONS.Build_HydraliskDen_screen.id
_BUILD_SPORE_CRAWLER = actions.FUNCTIONS.Build_SporeCrawler_screen.id
_BUILD_EVOLUTION_CHAMBER = actions.FUNCTIONS.Build_EvolutionChamber_screen.id
_BUILD_HIVE = actions.FUNCTIONS.Morph_Hive_quick.id
_BUILD_ULTRA_CAVERN = actions.FUNCTIONS.Build_UltraliskCavern_screen.id

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

    # Late game:
    # Hive?
    # Ultralisk cavern?

    def _init_(self):
        # use priority queue? in case buildings are destroyed
        self.BuildQ = [[0 for x in range(11)] for y in range(2)]
        self.BuildQ[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.BuildQ[1] = [_BUILD_HATCHERY, _BUILD_SPAWNING_POOL, _BUILD_SPINE_CRAWLER, _BUILD_EXTRACTOR,
                          _BUILD_ROACH_WARREN,
                          _BUILD_EVOLUTION_CHAMBER, _BUILD_LAIR, _BUILD_HYDRALISK_DEN,
                          _BUILD_SPORE_CRAWLER, _BUILD_HIVE, _BUILD_ULTRA_CAVERN]

    def dequeue(self, obs):
        # agent will handle the actually function call, we are just passing back the function id
        # repeated: hatchery, spine_crawler, spore crawler, extractor
        # everything else just need one of
        max = 0
        target_build = ''

        for i in len(self.BuildQ):
            if max < self.BuildQ[0][i]:
                max = self.BuildQ[0][i]
                target_build = self.BuildQ[1][i]

        # if target_build not an available action, then return NO_OP
        if target_build in obs.observations["available_actions"]:
            return target_build
        else :
            return _NOOP

    def update(self):
        # if a building does not exist, then push it up in priority
        # needs reconfiguring, a more intuitive numbering system
        if not have_spawning_pool:
            self.BuildQ[0][1] = 7
        if not have_roach_warren:
            self.BuildQ[0][4] = 6
        if not have_evo:
            self.BuildQ[0][5] = 5
        if not have_lair:
            self.BuildQ[0][6] = 4
        if not have_hydra_den:
            self.BuildQ[0][7] = 3
        if not have_hive:
            self.BuildQ[0][9] = 2
        if not have_ultra_cavern:
            self.BuildQ[0][10] = 1


# Unit Macros
_TRAIN_QUEEN = actions.FUNCTIONS.Train_Queen_quick.id
_TRAIN_ZERGLING = actions.FUNCTIONS.Train_Zergling_quick.id
_TRAIN_ROACH = actions.FUNCTIONS.Train_Roach_quick.id
_TRAIN_HYDRALISK = actions.FUNCTIONS.Train_Hydralisk_quick.id
_TRAIN_WORKER = actions.FUNCTIONS.Train_Drone_quick.id
_TRAIN_OVERLORD = actions.FUNCTIONS.Train_Overlord_quick.id
_TRAIN_ULTRALISK = actions.FUNCTIONS.Train_Ultralisk_quick.id

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

    # Late game ultralisks? (Basic strategy is to have a few ultralisks backed up by a large number of hydralisks)

    def _init_(self):
        """Set build order"""
        self.UnitQ = [[0 for x in range(7)] for y in range(2)]
        self.UnitQ[0] = [0, 0, 0, 0, 0, 0, 0]
        self.UnitQ[1] = [_TRAIN_QUEEN, _TRAIN_ZERGLING, _TRAIN_ROACH, _TRAIN_HYDRALISK,
                         _TRAIN_WORKER, _TRAIN_OVERLORD, _TRAIN_ULTRALISK]

    def dequeue(self, obs):

        # early game: if we dequeue a zergling and we don't have roach warren
        # then keeping enqueuing zerglings
        # mid-game: roaches only when roach warren is present
        # hydralisks?
        # get max priority unit, update list
        # access list like a 2D array
        max = 0
        target_unit = ''

        maxindex = 0

        for i in len(self.UnitQ):
            if max < self.UnitQ[0][i]:
                max = self.UnitQ[0][i]
                maxindex = i
                target_unit = self.UnitQ[1][i]

        # Set priority of target unit to 0, then update priorities
        self.UnitQ[0][maxindex] = 0
        self.update()

        if target_unit in obs.observations["available_actions"]:
            return target_unit
        else :
            return _NOOP

        return target_unit

    def update(self):
        # need to optimize so one unit does not outpace another
        # queen for every base (running total of num bases)
        if num_bases > num_queens:
            self.UnitQ[0][0] = 100
        # roaches go up with warren built (warren)
        if have_roach_warren:
            self.UnitQ[0][2] += 2
        # same for zergling, hydralisk and ultralisk (spawn pool, hydra den, ultralisk cavern)
        if have_spawning_pool:
            self.UnitQ[0][1] += 1
        if have_hydra_den:
            self.UnitQ[0][3] += 4
        if have_ultra_cavern:
            self.UnitQ[0][6] += 1

        # overlord max if need more supplies, otherwise lowest
        if max supply - current supply < supply required for next unit:
            self.BuildQ[0][5] = 5000


# Research Macros
_RESEARCH_METABOLIC_BOOST = actions.FUNCTIONS.Research_ZerglingMetabolicBoost_quick.id
_RESEARCH_GLIAL = actions.FUNCTIONS.Research_GlialRegeneration_quick.id
_RESEARCH_ZERG_MISSILE_WEAPONS = actions.FUNCTIONS.Research_ZergMissileWeapons_quick.id
_RESEARCH_ZERG_MISSILE_LVL1 = actions.FUNCTIONS.Research_ZergMissileWeaponsLevel1_quick.id
_RESEARCH_ZERG_MISSILE_LVL2 = actions.FUNCTIONS.Research_ZergMissileWeaponsLevel2_quick.id
_RESEARCH_ZERG_MISSILE_LVL3 = actions.FUNCTIONS.Research_ZergMissileWeaponsLevel2_quick.id
_RESEARCH_GROOVED_SPINES = actions.FUNCTIONS.Research_GroovedSpines_quick.id
_RESEARCH_ZERG_CARAPACE_LVL1 = actions.FUNCTIONS.Research_ZergGroundArmorLevel1_quick.id
_RESEARCH_ZERG_CARAPACE_LVL2 = actions.FUNCTIONS.Research_ZergGroundArmorLevel2_quick.id
_RESEARCH_ZERG_CARAPACE_LVL3 = actions.FUNCTIONS.Research_ZergGroundArmorLevel3_quick.id
_RESEARCH_CHITINOUS_PLATING = actions.FUNCTIONS.Research_ChitinousPlating_quick.id
_RESEARCH_PNEUMATIZED_CARAPACE = actions.FUNCTIONS.Research_PneumatizedCarapace_quick.id


# Research Queue

class ResearchQueue:
    # Order:
    # Metabolic Boost
    # Glial reconstitution
    # Zerg Missile Attacks level 1
    # Grooved Spines
    # Zerg Missile Attacks level 2
    # Zerg Carapace Level 1
    # Zerg Carapace Level 2
    # Zerg Missile Attacks level 3
    # Zerg Carapace Level 3
    # Chitinous Plating
    # Pneumatized Carapace

    def _init_(self):
        self.ResearchQ = asyncio.Stack()
        self.ResearchQ.append(_RESEARCH_PNEUMATIZED_CARAPACE)
        self.ResearchQ.append(_RESEARCH_CHITINOUS_PLATING)
        self.ResearchQ.append(_RESEARCH_ZERG_CARAPACE_LVL3)
        self.ResearchQ.append(_RESEARCH_ZERG_MISSILE_LVL3)
        self.ResearchQ.append(_RESEARCH_ZERG_CARAPACE_LVL2)
        self.ResearchQ.append(_RESEARCH_ZERG_CARAPACE_LVL1)
        self.ResearchQ.append(_RESEARCH_ZERG_MISSILE_LVL2)
        self.ResearchQ.append(_RESEARCH_GROOVED_SPINES)
        self.ResearchQ.append(_RESEARCH_ZERG_MISSILE_LVL1)
        self.ResearchQ.append(_RESEARCH_ZERG_MISSILE_WEAPONS)
        self.ResearchQ.append(_RESEARCH_GLIAL)
        self.ResearchQ.append(_RESEARCH_METABOLIC_BOOST)


    def dequeue(self, obs):
        # check if in available actions before dequeuing
        # change to a list as well? or use a stack?
        # pop, check for viability; if not, push it back on
        target_research = self.ResearchQ.pop()
        if target_research in obs.observations["available_actions"]:
            return target_research
        else :
            return _NOOP

    def enqueue(self, order):
        self.ResearchQ.put_nowait(order)


class Zerg():
    """Zerg units."""
    Baneling = 9
    BanelingBurrowed = 115
    BanelingCocoon = 8
    BanelingNest = 96
    BroodLord = 114
    BroodLordCocoon = 113
    Broodling = 289
    BroodlingEscort = 143
    Changeling = 12
    ChangelingMarine = 15
    ChangelingMarineShield = 14
    ChangelingZealot = 13
    ChangelingZergling = 17
    ChangelingZerglingWings = 16
    Corruptor = 112
    CreepTumor = 87
    CreepTumorBurrowed = 137
    CreepTumorQueen = 138
    Drone = 104
    DroneBurrowed = 116
    Cocoon = 103
    EvolutionChamber = 90
    Extractor = 88
    GreaterSpire = 102
    Hatchery = 86
    Hive = 101
    Hydralisk = 107
    HydraliskBurrowed = 117
    HydraliskDen = 91
    InfestationPit = 94
    InfestedTerran = 7
    InfestedTerranBurrowed = 120
    InfestedTerranCocoon = 150
    Infestor = 111
    InfestorBurrowed = 127
    Lair = 100
    Larva = 151
    Locust = 489
    LocustFlying = 693
    Lurker = 502
    LurkerBurrowed = 503
    LurkerDen = 504
    LurkerCocoon = 501
    Mutalisk = 108
    NydusCanal = 142
    NydusNetwork = 95
    Overlord = 106
    OverlordTransport = 893
    OverlordTransportCocoon = 892
    Overseer = 129
    OverseerCocoon = 128
    OverseerOversightMode = 1912
    Queen = 126
    QueenBurrowed = 125
    Ravager = 688
    RavagerBurrowed = 690
    RavagerCocoon = 687
    Roach = 110
    RoachBurrowed = 118
    RoachWarren = 97
    SpawningPool = 89
    SpineCrawler = 98
    SpineCrawlerUprooted = 139
    Spire = 92
    SporeCrawler = 99
    SporeCrawlerUprooted = 140
    SwarmHost = 494
    SwarmHostBurrowed = 493
    Ultralisk = 109
    UltraliskBurrowed = 131
    UltraliskCavern = 93
    Viper = 499
    Zergling = 105
    ZerglingBurrowed = 119
