# Hive-Map

Communication Agnostic Distributed Pub-Sub Network

## Description

Locations have attributes. For example: various points on a car engine have 
different temperatures; a room in the library is either occupied or unoccupied; 
a garbage can on the side of the road has various trash levels. These
attributes change over time: a car warming up on a cold day, a person entering
an empty study room, garbage being emptied on a monday morning. These changes
often go unnoticed, but they are the key to solving many problems: what part of
your engine broke? What rooms are available to study in? Did we miss the garbage
truck? The goal of Hive-Map is to provide the framework needed to tackle these
problems in a distributed setting.

**Hive-map gets messages about attribute information from one location to another.**

A **location** is an entity that represents a point in the hive-map space. Locations
are connected to one another through **channels**. Channels are the means in which
locations communicate. Locations publish messages to **destinations**. A destination 
is another location in the hive-map space. A location subscribes callbacks to desired
message types. 




In a library, "room 3" (a location) is detecting a
student in the room, so it periodically publishes an occupancy message to a library
occupancy database (destination). 


In the world of hive-map, a **node** is an entity sampling a location. The 
**space** of a node is the dimensions measured. The **state** of a node
is the current space values measured. For example, a node in "room 3" of the 
library has a space of occupancy which can either measure "True" or "False". The 
"room 3" node has a state of "True" because there is a student in the room. The 
node's state becomes "False" when the student leaves. The "room 3" node needs to
get the updated state to a location that can publish the information to a
database. Neighboring nodes (in other rooms) have the same objective.
**Nodes with matching goal locations can work together to get their updated 
states to that location** 

The user of the framework describes how individual nodes should behave: their
space, location, goal location, communication means, and callbacks. Hive-Map 
handles routing state changes to that goal location. The goal location can be 
an intermediate node that propogates its state to other locations.

## Goal

A library that performs distributed routing of states for a set of uniquely characterized nodes

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
  
