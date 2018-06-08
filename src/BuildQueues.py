import asyncio

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

# Features
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Misc. Actions
_NOOP = actions.FUNCTIONS.no_op.id

# Global Tracking vars
num_bases = 1  # how to keep track of?
num_queens = 0
have_hatchery = False
have_roach_warren = False
have_spawning_pool = False
have_hydra_den = False
have_evo = False
have_lair = False
have_hive = False
have_ultra_cavern = False
overlord_counter = 0
num_extractors = 0

# Building Macros
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

# class BuildingQueue
#
# Holds a priority queue of the building order.
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

    # Data structure is two lists:
    # the first list indicates the priority level of the corresponding structures
    # the higher the priority, the more quickly it will be built

    #Constructor 
    #Initializes the queue in the order we want our things built.
    def __init__(self):
        self.BuildQ = [[0 for x in range(11)] for y in range(2)]
        # self.BuildQ[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        # reverse? (above)
        self.queuelimits = [20, 19, 18, 17, 16, 14, 13, 12, 11, 10, 9]
        self.BuildQ[0] = [20, 19, 18, 17, 16, 14, 13, 12, 11, 10, 9]
        # we need several extractors, how to make sure this happens?
        self.BuildQ[1] = [_BUILD_HATCHERY, _BUILD_SPAWNING_POOL, _BUILD_SPINE_CRAWLER, _BUILD_EXTRACTOR,
                          _BUILD_ROACH_WARREN,
                          _BUILD_EVOLUTION_CHAMBER, _BUILD_LAIR, _BUILD_HYDRALISK_DEN,
                          _BUILD_SPORE_CRAWLER, _BUILD_HIVE, _BUILD_ULTRA_CAVERN]

    # agent will handle the actually function call, we are just passing back the function id
    # repeated: hatchery, spine_crawler, spore crawler, extractor
    # everything else just need one of
    # Dequeue: finds the max priority in the list, and returns the associated build, if available
   
    # dequeue(self, obs)
    # @param self Object pointer calling the function.
    # @param obs The observation feature maps.
    # Takes the highest 'value' (thing that needs to be built first) item
    # From the queue, returns the build command for it.
    def dequeue(self, obs):
        global num_bases
        global have_roach_warren
        global have_spawning_pool
        global have_hydra_den
        global have_evo
        global have_lair
        global have_hive
        global have_roach_warren
        global have_ultra_cavern
        global have_hatchery
        global num_extractors

        my_max = 0
        target_build = ''

        for i in range(len(self.BuildQ[0])):
            if my_max < self.BuildQ[0][i]:
                my_max = self.BuildQ[0][i]
                target_build = self.BuildQ[1][i]

        self.update(obs)
        # reset priority once built
        if _BUILD_HATCHERY == target_build:
            have_hatchery = True
            self.BuildQ[0][0] = 0
            num_bases += 1
        if _BUILD_SPAWNING_POOL == target_build:
            have_spawning_pool = True
            self.BuildQ[0][1] = 0
        if _BUILD_ROACH_WARREN == target_build:
            have_roach_warren = True
            self.BuildQ[0][4] = 0
        if _BUILD_EVOLUTION_CHAMBER == target_build:
            have_evo = True
            self.BuildQ[0][5] = 0
        if _BUILD_LAIR == target_build:
            have_lair = True
            self.BuildQ[0][6] = 0
        if _BUILD_HYDRALISK_DEN == target_build:
            have_hydra_den = True
            self.BuildQ[0][7] = 0
        if _BUILD_HIVE == target_build:
            have_hive = True
            self.BuildQ[0][9] = 0
        if _BUILD_ULTRA_CAVERN == target_build:
            have_ultra_cavern = True
            self.BuildQ[0][10] = 0
        
        #Special case: need 2 of these, second one after Evo chamber
        if _BUILD_EXTRACTOR == target_build:
            numextractors += 1
            if numextractors == 1:
                self.BuildQ[0][3] = 15
            else if numextractors > 1:
                self.BuildQ[0][3] = 0
                          
        if _BUILD_SPINE_CRAWLER == target_build:
            self.BuildQ[0][2] = 0
        if _BUILD_SPORE_CRAWLER == target_build:
            self.BuildQ[0][8] = 0
        return target_build

    # Update: if a building does not exist, then push it up in priority
    # ***needs reconfiguring, a more intuitive numbering system***

   # update(self, obs)
   # @param self Object pointer calling the function.
   # @param obs The observation feature maps. 
   # 'Updates' the queue. If a building is found to have been destroyed, it is re-added to the queue.
   def update(self, obs):
        global have_roach_warren
        global have_spawning_pool
        global have_hydra_den
        global have_evo
        global have_lair
        global have_hive
        global have_roach_warren
        global have_ultra_cavern
        global have_hatchery

        # if a building does not exist, and we have the prereqs for it
        # what about extractor, spine crawler, spore crawler?
        # what about expanding beyond one base?
        if not have_hatchery and self.BuildQ[0][0] < self.queuelimits[0]:
            self.BuildQ[0][0] += 1
        if not have_spawning_pool and self.BuildQ[0][1] < self.queuelimits[1]:
            self.BuildQ[0][1] += 1
        if not have_roach_warren and self.BuildQ[0][4] < self.queuelimits[4]:
            self.BuildQ[0][4] += 1
        if not have_evo and self.BuildQ[0][5] < self.queuelimits[5]:
            self.BuildQ[0][5] += 1
        if not have_lair and self.BuildQ[0][6] < self.queuelimits[6]:
            self.BuildQ[0][6] += 1
        if not have_hydra_den and self.BuildQ[0][7] < self.queuelimits[7]:
            self.BuildQ[0][7] += 1
        if not have_hive and self.BuildQ[0][9] < self.queuelimits[9]:
            self.BuildQ[0][9] += 1
        if not have_ultra_cavern and self.BuildQ[0][10] < self.queuelimits[10]:
            self.BuildQ[0][10] += 1
         
        #For extractor, increase if have less than 2
        if numextractors < 1  and self.BuildQ[0][3] < self.queuelimits[3]:
            self.BuildQ[0][3] += 1
        #If have 1 extractor, limit becomes 15
        else if numextractors < 2 and self.BuildQ[0][3] < self.queuelimits[3]:
            self.buildQ[0][3] += 1
        

        #Update spine crawler and spore crawler every time, up to a limit
        if self.BuildQ[0][2] < self.queuelimits[2]:
            self.BuildQ[0][2] += 1
        if self.BuildQ[0][8] < self.queuelimits[8]:
            self.BuildQ[0][8] += 1

        # check for building existence
        # change these to "minimap"?
        # extractor, other buildings?
        unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == 86).nonzero()  # hatchery
        # how to count number of hatcheries?
        if not unit_y.any():  # if it doesn't exist
            have_hatchery = False

        unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == 89).nonzero()  # spawning pool
        if not unit_y.any():  # if it doesn't exist
            have_spawning_pool = False

        unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == 97).nonzero()  # roach warren
        if not unit_y.any():  # if it doesn't exist
            have_roach_warren = False

        unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == 90).nonzero()  # evo
        if not unit_y.any():  # if it doesn't exist
            have_evo = False

        unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == 100).nonzero()  # lair
        if not unit_y.any():  # if it doesn't exist
            have_lair = False

        unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == 91).nonzero()  # hydra den
        if not unit_y.any():  # if it doesn't exist
            have_hydra_den = False

        unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == 101).nonzero()  # hive
        if not unit_y.any():  # if it doesn't exist
            have_hive = False

        unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == 109).nonzero()  # ultra
        if not unit_y.any():  # if it doesn't exist
            have_ultra_cavern = False
            
        unit_type = obs.observation["screen"][_UNIT_TYPE]
        unit_y, unit_x = (unit_type == 88).nonzero()  # extractor
        if not unit_y.any():  # if it doesn't exist
            numextractors = 0


# Unit Macros
_TRAIN_QUEEN = actions.FUNCTIONS.Train_Queen_quick.id
_TRAIN_ZERGLING = actions.FUNCTIONS.Train_Zergling_quick.id
_TRAIN_ROACH = actions.FUNCTIONS.Train_Roach_quick.id
_TRAIN_HYDRALISK = actions.FUNCTIONS.Train_Hydralisk_quick.id
_TRAIN_WORKER = actions.FUNCTIONS.Train_Drone_quick.id
_TRAIN_OVERLORD = actions.FUNCTIONS.Train_Overlord_quick.id
_TRAIN_ULTRALISK = actions.FUNCTIONS.Train_Ultralisk_quick.id

# class UnitQueue
#
# Similar to BuildingQueue, except for units instead of buildings.
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

    #Constructor
    #Initializes the queue
    def __init__(self):
        """Set build order"""
        self.UnitQ = [[0 for x in range(7)] for y in range(2)]
        self.UnitQ[0] = [0, 0, 0, 0, 0, 0, 0]
        self.UnitQ[1] = [_TRAIN_QUEEN, _TRAIN_ZERGLING, _TRAIN_ROACH, _TRAIN_HYDRALISK,
                         _TRAIN_WORKER, _TRAIN_OVERLORD, _TRAIN_ULTRALISK]
        #Supply required for each unit
        self.supply = [2, 1, 2, 2, 1, 0, 6]

    # dequeue(self,obs)
    # @param self Object pointer calling the function.
    # @param obs  The observation feature maps.
    # Dequeues the unit with the highest 'priority' and returns it's build command.
    def dequeue(self, obs):
        global num_queens
        global overlord_counter
        # early game: if we dequeue a zergling and we don't have roach warren
        # then keeping enqueuing zerglings
        # mid-game: roaches only when roach warren is present
        # hydralisks?
        # get max priority unit, update list
        # access list like a 2D array
        my_max = 0
        target_unit = ''

        maxindex = 0

        for i in range(len(self.UnitQ[0])):
            if my_max < self.UnitQ[0][i]:
                my_max = self.UnitQ[0][i]
                maxindex = i
                target_unit = self.UnitQ[1][i]

        # Set priority of target unit to 0, then update priorities
        self.UnitQ[0][maxindex] = 0
        self.update(obs)

        if target_unit in obs.observation["available_actions"]:
            if _TRAIN_QUEEN == target_unit:
                num_queens += 1  # why is this throwing an error?
            overlord_counter += 1
            return target_unit
        else:
            return _NOOP

    # update(self,obs)
    # @param self Object pointer calling the function.
    # @param obs  The observation feature maps.
    # If one of the units is killed and it can be remade, then add the unit
    # back to the queue.
    def update(self, obs):
        global num_queens
        global num_bases
        global overlord_counter
        global have_roach_warren
        global have_spawning_pool
        global have_hydra_den
        global have_evo
        global have_lair
        global have_hive
        global have_roach_warren
        global have_ultra_cavern
        global have_hatchery
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
        maxsupply = obs.observation['player'][4]
        currentsupply = obs.observation['player'][3]
        
        #Find supply needed for next unit (to see if overlord is needed)
        
        #Find next unit
        for i in range(len(self.UnitQ[0])):
            if my_max < self.UnitQ[0][i]:
                my_max = self.UnitQ[0][i]
                maxindex = i
        
        #Get supply
        supplyRequired = self.supply[i]
        if (maxsupply - currentsupply) < supplyRequired:
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

# class ResearchQueue
#
# Holds the queue for what research to do.
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

    #Constructor
    #Initializes the constructor queue.
    def __init__(self):
        self.ResearchQ = [_RESEARCH_PNEUMATIZED_CARAPACE, _RESEARCH_CHITINOUS_PLATING, _RESEARCH_ZERG_CARAPACE_LVL3,
                          _RESEARCH_ZERG_MISSILE_LVL3, _RESEARCH_ZERG_CARAPACE_LVL2, _RESEARCH_ZERG_CARAPACE_LVL3,
                          _RESEARCH_GROOVED_SPINES, _RESEARCH_ZERG_MISSILE_LVL1, _RESEARCH_ZERG_MISSILE_WEAPONS,
                          _RESEARCH_GLIAL, _RESEARCH_METABOLIC_BOOST]
    # dequeue(self,obs)
    # @param self The object pointer calling the function.
    # @param obs The observation feature maps.
    # Removes the highest 'priority' research from the queue, returning 
    # the command to start the research.
    def dequeue(self, obs):
        # pop, check for viability; if not, push it back on
        if self.ResearchQ[-1] in obs.observation['available_actions']:
            return self.ResearchQ.pop()
        else:
            return _NOOP

    # do we even need this?
    def enqueue(self, order):
        self.ResearchQ.append(order)

# class Zerg
#
# A "dictionary" of the unit ID's of the different zerg units.
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
