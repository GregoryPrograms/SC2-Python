# Actions
**Refer to actions.py in pysc2/bin folder.**

Functions IDs 0-11 are essential (UI functions).
## Unit Production

**_Build_** - build buildings (action ID 39-102)

**_Cancel_** - cancel builds (action ID 140-175)

**_Harvest_** - mining minerals, gas, etc. (action ID 264-273)

**_Research_** - unit upgrades to attack, armor, etc.; some concern ability additions (action ID 351-450)

**_Train_** - build units (action ID 457-510)
 
## Move and Attack Controls
**_Attack_** - (action ID 12-18)

**_Halt_** - (action ID 261-263)

**_Move_** - NOT moving units, moving player perspective (action ID 331-332)
 - move_screen or move_minimap
 
**_Patrol_** - might be useful for defensive AI mechanics (action ID 333-334)
 - unit will move between original location and patrol point set by user 
 
**_Rally_** - set rally points (?) (action ID 335-350) Will be hardcoding this in.

**_Smart_** - ?? (action ID 451-452)

**_Stop_** - (action ID 453-456)

## Calling actions for your agent
Format:
```python
# you can declare macros 
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id

#parameter macros
#queued or not queued: do later or do now
_NOT_QUEUED = [0]
_QUEUED = [1]

# function call example: to build barracks now at target location

return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])
#target is the (x,y) location on the map 
```

## More on calling actions for agent
Each action requires a certain number of parameters. For example, looking up the actions
by action ID, we find for Build_Barracks_screen (id = 42):
```python
 Function.ability(42, "Build_Barracks_screen", cmd_screen, 321),
```
The argument `cmd_screen` indicates what kind of parameters are required. 
If we look up `cmd_screen` below, we can find what parameters are needed.
The parameters we need seen above, are `[_NOT_QUEUED, target]`.

```python
FUNCTION_TYPES = {
    no_op: [],
    move_camera: [TYPES.minimap],
    select_point: [TYPES.select_point_act, TYPES.screen],
    select_rect: [TYPES.select_add, TYPES.screen, TYPES.screen2],
    select_unit: [TYPES.select_unit_act, TYPES.select_unit_id],
    control_group: [TYPES.control_group_act, TYPES.control_group_id],
    select_idle_worker: [TYPES.select_worker],
    select_army: [TYPES.select_add],
    select_warp_gates: [TYPES.select_add],
    select_larva: [],
    unload: [TYPES.unload_id],
    build_queue: [TYPES.build_queue_id],
    cmd_quick: [TYPES.queued],
    cmd_screen: [TYPES.queued, TYPES.screen],
    cmd_minimap: [TYPES.queued, TYPES.minimap],
    autocast: [],
}
```
The `TYPES` are detailed above the `FUNCTION_TYPES` in actions.py.



