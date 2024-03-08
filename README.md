# EndlessWorlds
Roguelike with endless worlds

# Solution model
One server running a world model and allowing one or more clients to communicate with it.

# Client commands
The set of commands a client can send to the server

## FOS - Field of Sense
Ask the server to provide a field of sense based on the provided parameters (x, y, z, r, i) where:
- x, y, z is the coordinates in the world as position x, y in the map z
- r is the radius requested
- i is the unique identifier that the server has granted the client

The server asks the world to provide the FOS information which result in a grid (x - r ... x + r, y - r, y + r) of (v, array of a, array of i) where:
- v is the landscape at the grid coordinate
- array of a is the list of actors at the grid coordinate
- array of i is the list of items at the grid coordinate