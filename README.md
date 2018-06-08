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

### [Actions.py](https://github.com/GregoryPrograms/SC2-Python/blob/master/src/actions.py)

### [BuildQueues.py](https://github.com/GregoryPrograms/SC2-Python/blob/master/src/BuildQueues.py)


## Written by us, made better by you
