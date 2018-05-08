# Observations

Most observations are done using map layers, that hold an array of positions on the map. For each of these positions, a value is set based on the map layer.

## Important maps: 

### height\_map 
  
  (try to abstract using a simpler map)
   
  Denotes height of terrain. Has 256 values. If we can not fully abstract with 
   a flat map, values will be simplified via only being inputted as comparison -   if a tile has too much height difference to walk up or down, we will specify    that the tile is too high or low for it's neighbours, using bitmapping. 

### visibility\_map 
   
  Denotes whether terrain is visible, not visible but has been revealed, or 
   hasn't been revealed (Not entirely sure what 'Full Hidden' means).
   
  Hidden = 0,
  Fogged = 1,
  Visible = 2,
  FullHidden = 3 

### creep
   
 Denotes whether this portion of the map is covered in zerg creep (Zerg can 
   only build structures on zerg creep)
   
 No Creep = 0,
 Creep = 1

### player\_relative

 Denotes whether units are friendly vs hostile
 
 Background = 0
 Self = 1
 Ally = 2
 Neutral = 3
 Enemy = 4

### unit\_type 
 
 Returns the unit type ID

 Will need to be abstracted; Use of power values to denote different units 
   (An ultralisk might be worth 2 megalisks, for example). Will also make it 
   easy to make judgements about whether fights are winnable. 

### selected 

 Which units are selected

   Not selected = 0
   Selected = 1

### unit\_density 
    How many units are in this pixel (might need this to calculate 
    center of mass)
  



