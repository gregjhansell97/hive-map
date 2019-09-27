# Hive-Map

Distributed state communication library

## Description

Locations have attributes. For example: various points on a car engine have 
different temperatures; a room in the library is either occupied or unoccupied; 
a garbage can on the side of the road has various trash levels. These
attributes change over time: a car warming up on a cold day, a person entering
an empty study room, garbage being emptied on a monday morning. These changes
often go unnoticed, but they are the key to solving many problems: what part of
your engine broke? What rooms are available to study in? Did we miss the garbage
truck? The goal of Hive-Map is to provide the framework needed to tackle these
problems.

**Hive-map gets changes in attribute information from one location to another.**

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

## Terminology

|Term    |Explanation                                                          |
|--------|---------------------------------------------------------------------|
|Node    |An entity sampling a location. A node can be represented by software used on everything from microcontrollers with sensor information, to python scripts running on computers                     |
|Space   |Dimensions used to measure a nodes surroundings                      |
|State   |Specific values of the Space that the Node has measured              |
|Channels|Communication links between nodes                                    |

## Libraries
[C](https://github.com/gregjhansell97/hive-map-c/)  
[python3](https://github.com/gregjhansell97/hive-map-python-3/)
  
