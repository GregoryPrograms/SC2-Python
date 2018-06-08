# SC2-Python-Bot
## Preface
Team project to implement a full AI for Starcraft II, utilizing reinforcement learning through the use of the Q-Learning Algorithm and a great deal of abstraction. This is accomplished by utilizing DeepMind’s pysc2, the Python component of the StarCraft II Learning Environment, which provides an interface for RL agents to interact with StarCraft II.<br />

PySC2 : https://github.com/deepmind/pysc2<br />
Project Report : https://docs.google.com/document/d/1YQh0klm4oo-cFp7O4mQ0cFkNpNQ-A1dFLH_04aUbi9g/<br />

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.



### Prerequisites

What things you need to install the software and how to install them

```
Install Starcraft 2
Install the latest version of python
Install Pycharm
Install PySC2
```

### Installing

#### Follow the procedure laid out in Deepmind's documentation to run PySC2
https://github.com/deepmind/pysc2

#### Clone our repository

```
$ git clone https://github.com/GregoryPrograms/SC2-Python.git
```

#### Once Everything is downloaded, you can run our bot

## Bot Overview

### [Botty_McBotface.py](https://github.com/GregoryPrograms/SC2-Python/blob/master/src/Botty_McBotface.py)

#### Controls what information is passed to and from the AI.
```Python
class Botty(base_agent.BaseAgent):
```

##### Constructor for our bot. It initializes the AI, passes it actions and gamestate
```Python
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
```
##### Initializes the base location of our bot
```Python
def init_base(self, obs):
```
##### This step function will:
1. Reduce state.
2. Allow brain to learn based on previous actions, states, & rewards
3. Choose an action based on current state.
4. Update the previous actions & state.
5. Do action.
```Python
def step(self, obs):
```
##### Makes it so that building will not be built directly near each other
```Python
building_offsets = {...}
```

##### Methods
```Python
# Takes information about the current game state, creates a 'reward'
# A reward is based on how good the current state is, and it gets passed to the Brain.
def reward_and_learn(self, obs):

# Takes in actions and if an action needs specific parameters, it passes those to it.
def get_action_list(self, action_str, obs):

# Whenever we build a building, we call this function. If it is a 
# building with special requirements, we fullfill those requirements 
# We also use offset to make sure the building does not overlap with any other buildings.
def get_building_target(obs, building):

# Called in order to move a set of coordinates by some distance, depending
# on whether the base is on the right or left side of the map. 
def transform_location(self, x, x_distance, y, y_distance):
```


### [RLBrain.py](https://github.com/GregoryPrograms/SC2-Python/blob/master/src/RLBrain.py)
#### Q-Learning attempts to learn the value of being in a given state, and taking a specific action there. This was implemented with the help of panda(open-source library that provides easy-to-use data structures and data analysis tools) and numpy(undamental package for scientific computing)
```Python
class RLBrain:
```

#### The init method for the brain.
```Python
def __init__(self, reduced_actions=None, decay_rate=0.1):
        self.actions = reduced_actions  # list of actions
        self.QTable = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.learn_rate = self.learning(0)
        self.decay_rate = decay_rate
        self.rand_rate = self.explore(0)
```
#### Methods
```Python
#This method chooses which action to do and returns that action
def choose_action(self, state):

#This method gets new state and reward from the environment
def add_state(self, state):

#finds a max value and then it gets passed onto rand_rate
def explore(self, t):

#returns max value and then it gets passed onto learn_rate
def learning(self, t):

#This uses given information to update the q-table
def learn(self, state, next_state, action, reward):
```
### [Actions.py](https://github.com/GregoryPrograms/SC2-Python/blob/master/src/actions.py)
#### Actions that are used by our bot
```Python

#no operational action
def no_op():

# @param obs: The observation map
# @param building: The building being built
# @param target: The location that the building is being built at
#builds the next building determined by the build order
def build_building(obs, building, target):

# @param unit: The unit being built
# Takes a unit from the build queue and builds that unit.
def build_units(unit):

# @param drone_func Function to build a drone from available larvae.
# Makes a new drone.
def build_worker(drone_func):


# research
# @param research_func Function to start researching
# Starts research on the next thing in the research queue.
def research(research_func):

# View control

# chooses x and y location to move to. Allows bot to see more
def moveview(x, y):

# @param obs The observation maps
# Looks for enemies, and attacks them.
def attack(obs):

# check to see if enemy units are too close. As such, this function is a simpler version of attack.
def defend(x_defend, y_defend):

# @param rally_x x location for the units to move to.
# @param rally_y y location for the units to move to.
# Takes in some point on the map, and moves army to that point. Can also be used to move army anywhere
def return_to_base(rally_x, rally_y):
```

### [BuildQueues.py](https://github.com/GregoryPrograms/SC2-Python/blob/master/src/BuildQueues.py)
```Python
class BuildingQueue:
```
Implemented using two lists. The first list indicates the priority level of the corresponding structure. The higher the priority, the more quickly it will be built.
Build Order:
    1. Hatchery:
    2. Spawning Pool
    3. Spine crawler
    4. Extractor
    5. Roach Warren
    6. Evolution Chamber
    7. Extractor 
    8. Lair
    9. Hydralisk Den
    10. Spore Crawler
    11. Hive
    12. Ultralisk cavern
    
```Python
class UnitQueue:
```
Uses same method as building queue but for units.
Military Build order:
    1. Queen (every time a new base is built)
    2. Zerglings
    3. Roaches
    4. Hydralisks
    5. Overlord (only when supply is low i.e. max supply - current supply < supply required for next unit)
    

```Python
class ResearchQueue:
```
Implemented using a stack instead of a priority queue for ease of checking availability and pushing
Order:
    1. Metabolic Boost
    2. Glial reconstitution
    3. Zerg Missile Attacks level 1
    4. Grooved Spines
    5. Zerg Missile Attacks level 2
    6. Zerg Carapace Level 1
    7. Zerg Carapace Level 2
    8. Zerg Missile Attacks level 3
    9. Zerg Carapace Level 3
    10. Chitinous Plating
    11. Pneumatized Carapace

## Written by us, made better by you
