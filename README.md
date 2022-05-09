# Endless Worlds

Building a Roguelike as a client server solution in which the client connection can transfer between servers. This will allow the player character, as well as non-player characters (NPCs), to travel through each world that each server offers.

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
