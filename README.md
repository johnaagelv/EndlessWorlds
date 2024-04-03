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

# Application layer protocol
Using TCP socket which is like reading from a file on a disk, but there is no option to reposition the socket pointer.

When bytes arrive at the socket, there are network buffers involved. Once the bytes are read, they need to be saved somewhere, else they will have been dropped!

Reading from a socket will be in chunks so read will have to be called and saved in the data buffer until a full message has been read.
To keep track of the message boundaries a application layer protocol needs to be defined.

## Application protocol header
The protocol header consists of a fixed length header and a variable length header.

Fixed header:
- Variable header length	2 byte integer

Variable header:
- Variable length text
- Unicode with the encoding UTF-8
- A Python dictionary serialized using JSON

The required headers in the protocol header's dictionary are as follows:

| Name | Description |
| ---------------- | ------------------------------------------------- | 
| byteorder | The byte order of the machine (uses sys.byteorder) |
| content-length | The length of the content in bytes |
| content-type | The type of content in the payload, for example, text/json or binary/my-binary-type |
| content-encoding | The encoding used by the content, for example, utf-8 for Unicode text or binary for data |

## Application protocol
Application protocol defines the information transferred between the client and the server

### Field of Sense - OP_FOS
Client sends this operation every X seconds with the following properties:
- x, y, z coordinates - this is the x, y coordinates in the z map of the world
- r - the radius of the field of sense

### Attack - OP_ATTACK
Client sends this operation when the character is performing an attack in a specific direction
- x, y, z coordinates - this is the x, y coordinates in the z map of the world
- dx, dy directions - this is the relative direction that the attack is directed from the x, y coordinate
- s - the strength of the attack

### Attack - OP_ATTACK
Client sends this operation when the character is performing an attack on a specific character
- x, y, z coordinates - this is the x, y coordinates in the z map of the world
- cuid - the unique ID of the character being attacked
- s - the strength of the attack

