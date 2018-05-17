import asyncio

from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

class gamestate():
    visibility;
    creep;
    player_relative;
    unit_type;
    selected;
    unit_density;
    minerals;
    vespene;
    availFood;
    armyCount;
    larvaCount;
    state;

    def __init__(self):
        self.visibility = obs.observation.feature_screen.visibility_map
	self.creep = obs.observation.feature_screen.creep
        self.player_relative = obs.observation.feature_screen.player_relative;
        self.unit_type = obs.observation.feature_screen.unit_type;
	self.selected = obs.observation.feature_screen.selected;
	self.unit_density = obs.observation.feature_screen.unit_density;
	self.minerals = obs.player_common.minerals
	self.vespene = obs.player_common.vespene
	self.availFood = obs.player_common.food_cap
	self.armyCount = 0;
        self.larvaCount = 0;
        self.state = [self.visibility, self.creep, self.player_relative, self.unit_type, self.selected, self.unit_density, self.minerals,			  self.vespene, self.availFood, self.armyCount, self.larvaCount];

    def update(self):
	self.visibility = obs.observation.feature_screen.visibility_map
        self.creep = obs.observation.feature_screen.creep
        self.player_relative = obs.observation.feature_screen.player_relative;
        self.unit_type = obs.observation.feature_screen.unit_type;
        self.selected = obs.observation.feature_screen.selected;
        self.unit_density = obs.observation.feature_screen.unit_density;
        self.minerals = obs.player_common.minerals
        self.vespene = obs.player_common.vespene
        self.availFood = obs.player_common.food_cap - obs.player_common.food_used;
        self.armyCount = obs.player_common.army_count;
        self.larvaCount = obs.player_common.larva_count;
        self.state = [self.visibility, self.creep, self.player_relative, self.unit_type, self.selected, self.unit_density, self.minerals,                         self.vespene, self.availFood, self.armyCount, self.larvaCount];

    
