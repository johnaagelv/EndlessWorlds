# EndlessWorlds

Building a client server(s) Roguelike, but with a ticking clock running.

A World server:
- must provide a World and maps in which one or more player clients can travel
- must track all player clients travelling the World
- must provide Field of View (FOV) information to a player client
- ...


A player client:
- must be able to start at any World server that provides a starting point
- must be able to suspend the game under certain circumstances
- must be able to resume the game
- must be able to travel the connected World servers and their maps
- must be able to interact with a World
- must be able to interact with the inhabitants of a World
- ...
