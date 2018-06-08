# SC2-Python-Bot
## Preface
Team project to implement a full AI for Starcraft II, utilizing reinforcement learning through the use of the Q-Learning Algorithm and a great deal of abstraction. This is accomplished by utilizing DeepMind’s pysc2, the Python component of the StarCraft II Learning Environment, which provides an interface for RL agents to interact with StarCraft II.<br />

PySC2 : https://github.com/deepmind/pysc2<br />
Project Report : https://docs.google.com/document/d/1YQh0klm4oo-cFp7O4mQ0cFkNpNQ-A1dFLH_04aUbi9g/<br />
Final Report: https://docs.google.com/document/d/1YQh0klm4oo-cFp7O4mQ0cFkNpNQ-A1dFLH_04aUbi9g<br />

### Group Members
[Michael Field](https://github.com/mfield4)<br />
[Gregory Dost](https://github.com/GregoryPrograms)<br />
[Christopher De Castro](https://github.com/FuzionLLF)<br />
[Wesley Loo](https://github.com/whloo-rebel-scum)<br />
[Emil Aliyev](https://github.com/EmilAliyev)<br />

### Problem and Contribution Statement

   Starcraft II is an RTS that provides serious issues for AI development. With effectively infinite possible map positions, 56 different units (all with health values, energy, possible actions, costs, etc.), 60 different possible buildings (also all with health values, outputs or inputs, costs), as well as several other factors affecting game state, finding the absolute best move from any game state to the next has a very high complexity. However to compete with a human player any Starcraft II AI would need to be capable of taking actions in real time, requiring the AI to make quick decisions about gamestate. 
	
   This creates a conundrum for Starcraft II AI creators, who need to produce an AI that can compute impossibly complex game states in lightning fast times. As a result of this, AI researchers have a much harder time creating functional and useful AI for Starcraft II than for grid based games such as chess or Go. However, creating an AI that could capably play Starcraft could greatly impact the capabilities of AI to solve real world problems, where complex decisions need to be made in real time.  For example, systems such as fully autonomous cars would greatly benefit from an AI capable of solving problems of similar complexity to those in Starcraft (such as how to most safely avoid a collision with little warning time). 
	
   One common approach is to abstract the data being worked with. In other words, the data sent to the AI is carefully vetted, to reduce the complexity of the current state. Information that is less useful or difficult to fully compute is either completely disregarded by the AI, or simplified in some manner. For example, there are essentially infinite possible locations of units in the Starcraft II map. However, if one was to generalize location by dividing the map into a grid and reporting the location of a unit as being a grid position based on their center of mass, the amount of locations could be reduced to something computable. This approach also benefits learning algorithms, as by reducing the state space they need to search it becomes easier to gather data about the correct path of actions. However, possibly valuable information can be lost through data abstraction, and the AI’s capability of interacting with the environment is limited. To optimize abstraction, one must be careful to abstract data in a way that the minimum possible amount of valuable information is lost, for the greatest performance increase. 
	
   Almost all game AI have some layer of abstraction by nature, whether purposeful or not; For example, AlphaGo does not pre-profile an opponent based on the opponent’s preferred play style. This is an inherent part of every system - there will be some unknown or unprocessable factors, and as there is no method available to the AI to gather data on these factors or recognize their existence, they are abstracted. This system mirrors human intelligence, where people commonly have to make decisions with several unknown factors. When a Starcraft II player makes a decision, they do not know or fully comprehend the exact details of the game state -- If one unit was moved one pixel to the left, it is unlikely they would read the game state differently, and in general the optimal decision to take would be the same. 
	
   Currently several different AI approaches are taken utilizing abstraction.  For instance,  Starcraft tournament bots are usually implemented using rules based expert systems. In this case  bot creators have decided to forgo a Machine Learning approach and rely solely on rules they can create in an effort to reduce the complexity of the bot as well as getting it to work. However, in terms of creating a bot for this project, an expert system would require in depth game knowledge that our team does not possess. 
For this reason,  we decided to use reinforcement learning to research the effects of abstraction on a system to try to create a functional AI for Starcraft II. We will use reinforcement learning to train our bot via minigames, with the goal of creating a bot that manages to play starcraft II. This goal will allow us to address the issue of researching abstraction, as we will need to choose a good model for the information to send to the AI. As well, this will allow us to gather knowledge about how all of the different areas of game AI work, more so than any other approach. With a reinforcement learning bot, it is possible for us to create a functional full bot as a five person team with no prior experience within the time allowed. This allows us to gather information about many areas of AI we would otherwise have to forego -- such as path planning, machine learning, etc. 

   We will be implementing a Q-Learning algorithm as the brain for this bot. This particular algorithm does not require environmental context and is implemented with a nice and simple array, making it very easy to get started. Other RL algorithms may give me more control on predicting future outcomes as well as state and action space, but the price would be a lot of technical debt. 
To do all of this we decided to use PySC2. As a language python is obvious for a project of this scale and timeframe. We need to be able to quickly implement our ideas and get to testing sooner rather than later. While we could use the SC2 C++ api, implementing large programs in C++ can be a pain, even if some of us are more comfortable in it. C++ also doesn’t have the advantage of easy training and testing that PySC2 allows us. 

### Design and Technical Approach 
   Reinforcement learning (RL) is the primary technique by which we will be designing our StarCraft II bot. This will be accomplished by  utilizing DeepMind’s pysc2, the Python component of the StarCraft II Learning Environment, which provides an interface for RL agents to interact with StarCraft II.  The primary focus of our RL agent will be in the Q-Learning RL technique, which relies on mapping state space to action space in a simple array. By abstracting vital gameplay phases and tasks into reduced search spaces, we can experiment with a variety of different mini-games to help our AI learn to play the game. 
   
   Reducing the state space for the RL agent itself will be a for an AI technique. We need to make intelligent decisions about what in the state in important and what is not. To start, instead of considering continuous info about unit position, we can abstract units onto a grid. To take that even further, instead of worrying about individual unit position, it may be smarter to think about total unit position and unit numbers instead. We can make similar assumptions about enemy movement as well, all with the goal of removing state space as much as possible.
   
   Once state is reduced, the RL algorithm can decide what action to do. Because the Q-Learning technique relies on both state and action space, reducing the action space as much as possible it also advantageous. Abstracting actions to a much smaller set of actions allows us to remove much of the context around an action. Without context actions become simple and concise, which heavily reduces action space. The penalty in the technique is of course that we much add the context back in at a later point. For our bot actions will mainly be implemented via expert rules based systems. This allows the easiest and quickest way to issue commands.
   
   Successfully creating our bot will ultimately be about making the correct decisions in the cutoff points in abstraction. If we reduce state too much we may end up with meaningless assumptions. And if we reduce action space too much we may put too much work in the wrong place. This is all about juggling levels of abstraction in various algorithms, with the end goal of creating a functional bot in SC2. To train our bot we will be pitting the bot against ingame AI and eventually real players on the headless SC2. This will speed up training and allow more testing on the best ways to train our bot.
   
   It follows that we have chosen Python as the primary language to use to code our AI. Python and PySC2 allows us to keep everything under the same hood. Because we are working with a problem that is ultimately unsolved, working with a language that won’t bog us down is a huge selling point.
   
   In order to maintain a uniform workflow, all members of the group will use the PyCharm IDE (student edition). For many of us not used to python outside of a scripting setting, the IDE will hopefully keep our build system straight and force everybody to adhere to good style and coding standards. We will also use Pylint, a separate code analysis and QA package for Python, which follows PEP 8, the Python style guide. Primary means of communication will be through a private Discord server.



## Getting Started

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
# @param self:The object pointer calling the function
# @param obs:The observation maps
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
# @param self:The object pointer calling the function
# @param obs:The observation map.
# Takes information about the current game state, creates a 'reward'
# A reward is based on how good the current state is, and it gets passed to the Brain.
def reward_and_learn(self, obs):

# @param self The object pointer calling the function
# @param action_str A string containing one of the actions from those available to the AI.
# @obs The observation maps
# Takes in actions and if an action needs specific parameters, it passes those to it.
def get_action_list(self, action_str, obs):

# @param obs The observation maps
# @param building A macro used to refer to specific buildings.
# Whenever we build a building, we call this function. If it is a 
# building with special requirements, we fullfill those requirements 
# We also use offset to make sure the building does not overlap with any other buildings.
def get_building_target(obs, building):

# @param self The object pointer calling the function
# @param x The initial x
# @param x_distance The distance between the initial and final x
# @param y The initial y
# @param y_distance The distance between the initial and final y
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
# @param self:Object pointer calling the function.
# @param state:Gamestate information.
#This method chooses which action to do and returns that action
def choose_action(self, state):

# @param self:Object pointer calling the function.
# @param state:Gamestate information.
#This method gets new state and reward from the environment
def add_state(self, state):

# @param self:Object pointer calling the function.
# @param t:Number of states explored so far.
# Finds the rate at which random states are chosen.
def explore(self, t):
   
# @param self:Object pointer calling the function.
# @param t:Number of states explored so far.
#returns max value and then it gets passed onto learn_rate
def learning(self, t):

# @param self: Object pointer calling the function.
# @param state: First of the two states in the state transition being learned.
# @param next_state: Second of the two states in the state transition being learned.
# @action action: that was taken that transitioned between the two states.
# @reward reward: for the action.
#This uses given information to update the q-table
def learn(self, state, next_state, action, reward):
```

### [Learner.py](https://github.com/GregoryPrograms/SC2-Python/blob/master/src/Learner.py)
#####  Represent the current state of the game. Takes necessary information from the SC2 API, and shares it with the RL bot.
```Python
class GameState:
```
#### Constructor, initializes the returned list.
```Python
def __init__(self, obs=None):
    self.minerals = None
    self.vespene = None
    self.availFood = None
    self.armyCount = 0
    self.larvaCount = 0
```

#### returns current state of the game
```Python
# @param self: The object pointer
# @param obs: The observation maps
def update(self, obs):
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

# @param drone_func: Function to build a drone from available larvae.
# Makes a new drone.
def build_worker(drone_func):

# @param research_func: Function to start researching
# Starts research on the next thing in the research queue.
def research(research_func):

# chooses x and y location to move to. Allows bot to see more
def moveview(x, y):

# @param obs: The observation maps
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
Implemented using two lists. The first list indicates the priority level of the corresponding structure. The higher the priority, the more quickly it will be built. Some buildings need to be built several times, and buildings must be reconstructed after destruction, so the building queue also updates the priority of each building depending on the situation, i.e. the existence or lack thereof of certain buildings.<br />
Build Order:<br />
 - 1. Hatchery<br />
 - 2. Spawning Pool<br />
 - 3. Spine crawler<br />
 - 4. Extractor<br />
 - 5. Roach Warren<br />
 - 6. Evolution Chamber<br />
 - 7. Extractor <br />
 - 8. Lair<br />
 - 9. Hydralisk Den<br />
 - 10. Spore Crawler<br />
 - 11. Hive<br />
 - 12. Ultralisk cavern<br />
    
```Python
class UnitQueue:
```
Uses a similar method as the building queue but for military units (workers are not included in this queue as they are part of a separate action that specifically trains workers). The priority of each unit is updated each time a unit is dequeued to account for factors such as the availability of the units and the availability of supply (if supply isn't available, the overlord's priority is set very high to ensure it will be the next unit trained). The strategy is for the army to consist entirely of zerglings at the beginning of the game (immediately after the spawning pool is built), transitioning into an army of roaches once the roach warren is built, to an army of roaches and hydralisks in the middle of the game once the hydralisk den is built, and finally adding some ultralisks in the later stages of the game after the ultralisk cavern is built. Queens are trained every time a new base is constructed and overlords are trained whenever they are necessary (when there is less supply available than needed). <br />
Military Build order:<br />
 - 1. Queen (every time a new base is built)<br />
 - 2. Zerglings<br />
 - 3. Roaches<br />
 - 4. Hydralisks<br />
 - 5. Ultralisks<br />
 - 6. Overlord (only when supply is low i.e. max supply - current supply < supply required for next unit)<br />
    

```Python
class ResearchQueue:
```
Implemented using a stack instead of a priority queue for ease of checking availability and pushing. As each upgrade only needs to be researched once, a simple stack is adequate for the task of determining the next upgrade to research. <br />
Order:<br />
 - 1. Metabolic Boost<br />
 - 2. Glial reconstitution<br />
 - 3. Zerg Missile Attacks level 1<br />
 - 4. Grooved Spines<br />
 - 5. Zerg Missile Attacks level 2<br />
 - 6. Zerg Carapace Level 1<br />
 - 7. Zerg Carapace Level 2<br />
 - 8. Zerg Missile Attacks level 3<br />
 - 9. Zerg Carapace Level 3<br />
 - 10. Chitinous Plating<br />
 - 11. Pneumatized Carapace<br />

## Written by us, made better by you
