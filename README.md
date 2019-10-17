# Hive-Map

Communication Agnostic Distributed Pub-Sub Network

## Description

**Hive-map provides a framework to facilitate message publishing between user defined 
locations.**

A **location** is an entity that represents a point on a symbolic map. Locations
are connected to one another through **channels**. Channels are the means in which
locations communicate. Locations publish messages to **destinations**. A destination 
is another location on the symbolic map. A location has subscribers to various message 
types.

![](docs/diagrams/node_interaction_01.png)

In the diagram above, *L<sub>2</sub>* publishes a message to *L<sub>4</sub>*. Upon receiving 
the message, *L<sub>4</sub>* will deliver the message to the appropriate subscribers; an
appropriate subscriber subscribes to that message type. Subscribers are not part of the
diagram: they are language dependent programming constructs.

**Locations with matching destinations can work together to get their messages
to those destinations.**

The user of the framework describes the communication channels, available locations,
and types of messages. Hive-map handles routing published messages to destinations. 


## Goal

A framework to perform distributed routing of subscribable messages from locations to destinations.

## Examples

### Library Occupancy Detection

The goal of library occupancy detection is to get occupancy information from rooms
in the library to a database. Some locations are: *room 1*, *room 2* and 
*occupancy database*. The messages being published are messages that describe 
occupancy. A particular room publishes occupancy messages to the occupancy database. 
The occupancy database (as a location) subscribes to occupancy messages. The user 
describes the communication channels between locations, the available locations and 
message types. Hive-map handles routing occupancy messages from rooms to the 
occupancy database.

## Components

### Node
An entity sampling a location. A node has several attributes: location, goal location, 
communication channels and a state. Location is the place the node resides. Goal location is
the place a node wishes to send all of it's state changes to. A node sends a state change to a
location, not another node. Communication channels are used by a node to interact with other nodes.
State is the measurements of the node's space.
 
#### Assumptions
- node locations are abstract
- node's location is fixed or anonymous
- node's goal location is fixed, anonymous or doesn't exist
- nodes only communicate through channels
- nodes in the same location have dependable FIFO channels of communication
- nodes do not crash
- new nodes can be introduced into the system

### Space
Dimensions used to measure a nodes surroundings

### State
Specific values of the Space that the Node has measured

### Channels
Communication links between nodes

## Libraries
[C](https://github.com/gregjhansell97/hive-map-c/)  

[Python3](https://github.com/gregjhansell97/hive-map-python-3/)

[Cpp](https://github.com/gregjhansell97/hive-map-cpp/)  
  
