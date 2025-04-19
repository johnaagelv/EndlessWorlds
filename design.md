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

Assumptions:
- Properties are the unchangeable definitions of the actor.
- Capabilities are the changeable definitions of the actor.

# 3. ...
