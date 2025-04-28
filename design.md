# 1. Introduction
A Roguelike game running a client and connecting to one or more servers.

Each server provides the client with a set of interconnected maps. A server can represent
a world, a continent, a country, an area, a city, a vehicle, a cave tunnel system, a spaceship ... 
you name it!

Each map can not only be interconnected to other maps on the same server, but can also connect to
a map on another server.

With this archictecture, the game may become endless!

# 2. Actor portability
An actor, being a player or an NPC (Non-Player Character), must be constructed in such a way that
the actor can be easily transferred between servers, even if a server does not support the full
definition of an actor.

## 2.1 Actor data structures
Data structures will be used to define all the properties, capabilities, and so on, of the actor.

An actor will have capabilities and these are the first set:
- locomotion
- senses
  - vision
- states
  - health
  - energy

Capabilities are then represented by properties, although not all properties represent a capability:
- name
- position (x, y, z, m) where x, y, z are the actor's coordinate in the map m in the current world
- senses
  - vision
    - range (min, max, current)
  - more to be defined in the future
- states
  - health (min, max, current)
  - energy (min, max, current)
  - more to be defined in the future

# 3. Map simplicity
Currently built on the tile structure defined in the TCOD tutorial with addition for gateways.

The tile structure has the properties:
- Walkable (true/false)
- Transparent (true/false)
- Dark (symbol, foreground colour, background colour)
- Light (symbol, foreground colour, background colour)
- Gateway (true/false) - indicates a gateway tile when true

Gateway tiles are automatic map changes, examples:
- entering an open doorway tile of a house automatically changes the map to the inside of the house.
- entering a cave entrance tile automatically changes the map to the cave tunnel system.

To facilitate the automatic map changes, the world has a gateway list where each entry specifies
the location of the gateway and the target location on a target map.

Not all entries in the gateway list are for automatic map changes. Some will be for stairways, where
the player invokes the map change by going down or up the stairway