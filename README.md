# Endless Worlds

Building a Roguelike as a client server(s) solution in which the client connection can transfer between servers. This will allow the player character, as well as non-player characters (NPCs), to travel through each world that each server offers.

A server hub will manage the list of servers that provides a starting point for a player.

## Server
A World server:
- must provide a World and maps in which one or more player clients can travel
- must track all player clients travelling the World
- must provide Field of View (FOV) information to a player client
- must be able to provide connections to other World servers
- ...

## Client
A player client:
- must be able to start at any World server that provides a starting point
- must be able to suspend the game under certain circumstances
- must be able to resume the game
- must be able to travel the connected World servers and their maps
- must be able to interact with a World
- must be able to interact with the inhabitants of a World
- ...

## Playable game
The solution must provide a playable game consisting of at least two Worlds, each with several maps.

World 1 will provide:
- a country map with one village and one cave and one portal linked to World 2
- a village map with one house
- a house map
- a cave map with two levels
- a level map for each of the two levels
- the cave inhabitants (TBD)

World 2 will provide:
- a country map with one village and one portal linked to World 1
- a village map with one shop
- a shop map
- the shop keeper
- the shop items (food, torch, ...)

# Design
The design is separated into the server side, the World server hub, and the client side. 

+--------+               +--------+
| World  <------data-----> Player |
| server |               | client |
|        <------+        |        |
+--------+      |        +--------+
              register
+--------+      |        +--------+
|        <------+        |        |
| Hub    |               | Hub    |
| server <--synchronize--> server |
+--------+               +--------+




## Server
Server starts up with loading the World information

###### Server information
A World server may be published as a starting point for players. The World server will then 
Server information are:
- public world:
	- name is the public name of this World server
	- description is the public introduction to this World server
	- host IP used to access this World server
	- port no. used to access this World server

###### World information
World information are:
- X number of maps, where each map contains these sets of information:
	- properties:
		- map no. - unique number of the map in the World
		- x coordinate for a new player
		- y coordinate for a new player
		- width of the map's x axis
		- height of the map's y axis
		- known indicator for whether or not the map is known from the start (0=unknown, 1=known)
	- tiles - a 2D character array of the map
	- connections - a list of connection points on the map that leads to other maps:
		- map no. of the target map
		- x coordinate on the target map
		- y coordinate on the target map
		- host IP (optional) of the World server on which the target map exists
		- port no. (optional) of the World server on which the target map exists

###### World inhabitants
World inhabitants is a list of non-player characters populating the World.
...

## World server hub
A World server hub manages a list of World servers in which players can start. The World server hub also manages a list of other World server hubs in order to synchronze the list of World servers.

The list of World servers contains the following information about each World server:
	- name is the public name of this World server
	- description is the public introduction to this World server
	- host IP used to access the World hub
	- port no. used to access the World hub

The list of World server hubs contains the following information about each other World server hub:
	- host IP used to access the World hub
	- port no. used to access the World hub

###### World server hub interchanges
A World server hub must handle the following requests:
- "ADD" that will add a new World server hub to the list of World server hubs
- "REMOVE" that will remove an existing World server hub from the list of World server hubs
- "CONFIRM" that will ask a World server hub to confirm last request and include the request to confirm

In the case of the "ADD" and "REMOVE" request - they will be replicated to other World server hubs, if and only if they are successfully performed

###### World server hub and World server interchanges
A World server hub must handle the following requests from a World server:
- "ADD" request to add a World server to the list of World servers
- "REMOVE" request to remove a World server from the list of World servers

A World server must handle the following requests from a World server hub:
- "CONFIRM" request to confirm that the last request received (included) is to be performed
