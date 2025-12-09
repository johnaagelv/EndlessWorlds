# World generator for Endless Worlds
The generator makes it easier to build a World consisting of one or more maps, where a map may be whatever you wish it to be!

# Generator build definitions
The build definition is a dictionary of world information and map build instructions.

## World information
The world information are:
- id, unique identified of this world
- name, the name of this world
- entry, is a list of map coordinates where the player may be starting from
- maps, is a list of all the map build instructions

## Map build instructions
The map build instructions each starts with a build instruction number, where:
- 0 is the instruction that defines the map name, size, default tile to use, visibility (known from the start or not), and an optional seed
- 1 is the instruction to build a square/rectangle at coordinates x, y with a width and height, a tile to use, and to fill the square/rectangle or not
- 2 is the instruction to build a circle at coordinates x, y with a radius, a tile to use, to fill it or not, and a thickness used when fill is false
- 3 is the instruction to build an automatic map shifting tile at coordinates x, y, a tile to use, the target coordinates x, y, the altitude, and target map number
- 4 is the instruction to build an action activated map shifting tile at coordinates x, y, a tile to use, the target coordinates x, y, the altitude, target map number, and an action (up/down)
- 5 is the instruction to build an area at coordinates x, y with a width and height, using two or three tiles randomly
- 6 is the instruction to build a trail at coordinates x1, y1 with a target of coordinates x2, y2 and the trail width between two values
- 7 is the instruction to build an area at coordinates x, y with a width and height filled with a specified symbol (ie. a new tile will be created)

Whenever a 0 build instruction number is read, a new map is started and every higher build instruction number is applied to that map.

# Preconditions
Using the "redjack17.png" tilesheet (16 x 16) with charmap CP437 - which define codepoints as follows:

  0:    0, 9786, 9787, 9829, 9830, 9827, 9824, 8226, 9688, 9675, 9689, 9794, 9792, 9834, 9835, 9788,
 16: 9658, 9668, 8597, 8252,  182,  167, 9644, 8616, 8593, 8595, 8594, 8592, 8735, 8596, 9650, 9660,
 32:   32,   33,   34,   35,   36,   37,   38,   39,   40,   41,   42,   43,   44,   45,   46,   47,
 48:   48,   49,   50,   51,   52,   53,   54,   55,   56,   57,   58,   59,   60,   61,   62,   63,
 64:   64,   65,   66,   67,   68,   69,   70,   71,   72,   73,   74,   75,   76,   77,   78,   79,
 80:   80,   81,   82,   83,   84,   85,   86,   87,   88,   89,   90,   91,   92,   93,   94,   95,
 96:   96,   97,   98,   99,  100,  101,  102,  103,  104,  105,  106,  107,  108,  109,  110,  111,
112:  112,  113,  114,  115,  116,  117,  118,  119,  120,  121,  122,  123,  124,  125,  126, 8962,
128:  199,  252,  233,  226,  228,  224,  229,  231,  234,  235,  232,  239,  238,  236,  196,  197,
144:  201,  230,  198,  244,  246,  242,  251,  249,  255,  214,  220,  162,  163,  165, 8359,  402,
160:  225,  237,  243,  250,  241,  209,  170,  186,  191, 8976,  172,  189,  188,  161,  171,  187,
176: 9617, 9618, 9619, 9474, 9508, 9569, 9570, 9558, 9557, 9571, 9553, 9559, 9565, 9564, 9563, 9488,
192: 9492, 9524, 9516, 9500, 9472, 9532, 9566, 9567, 9562, 9556, 9577, 9574, 9568, 9552, 9580, 9575,
208: 9576, 9572, 9573, 9561, 9560, 9554, 9555, 9579, 9578, 9496, 9484, 9608, 9604, 9612, 9616, 9600,
224:  945,  223,  915,  960,  931,  963,  181,  964,  934,  920,  937,  948, 8734,  966,  949, 8745,
240: 8801,  177, 8805, 8804, 8992, 8993,  247, 8776,  176, 8729,  183, 8730, 8319,  178, 9632,  160

# Items
Played around with ECS on the client side to identify if and how this could be used on the server side.
The client side can use the ECS, but the server side has no need to be burdened with this additional
feature.

## Consumables
- type, "consumable"
- name, food parcel, food ration, ...
- position, location on the map/world (x, y, z, m)
- value, the energy that it contains for consumption by an actor
- weight, the burden carrying this item

## Equippables
- type, "equippable"
- name, boots, gloves, helmet, jacket, trousers, ...
- position, location on the map/world (x, y, z, m)
- location, the body part(s) that will use this item (hands, arms, legs, feet, back, torso, head, neck, )
- weight, the burden carrying this item
- protection, the protection this item provides

## Weapons
- type, "weapon"
- name, gun, rifle, shotgun, bow, axe, spear, club, staff, knife, sword, taser, shield, armour, ...
- position, location on the map/world (x, y, z, m)
- location, the body part(s) that will use this item
- weight, the burden carrying this item
- defense, the strength with which this weapon will absorb a hit
- attack, the strength with which this weapon will apply to an opponent on a 100% hit

## Equipments, handheld
- type, "handheld"
- name, "drill", "tablet", "scanner", "medkit", "
- position, location on the map/world (x, y, z, m)
- weight, the burden carrying this item

## Equipments, operational
- type, "operational"
- name, car, plane, bicycle, motorcycle, ...
- position, location on the map/world (x, y, z, m)
- energy usage

## Equipments, static
- type, "static"
- name, food dispencer, computer, energy generator, ...
- position, location on the map/world (x, y, z, m)
- operations, 
