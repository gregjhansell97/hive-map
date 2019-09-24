========
hive-map
========


API that makes retrieving live sensor data from a map simple. Hardware is
abstracted so you can focus on the software.


Description
===========

The hive_map module is used to help alleviate data retrevial in a distributed 
sensor network. The hive_map module handles the middle ground between the 
software and hardware. 

The software developer defines a state and location based on metrics provided 
by the hive_map module. Metrics, from the hive_map module, are used so the 
developer doesn't have to worry about serialization to the hardware.

The hive-map module is only one part of the HiveMap ecosystem. There are 
hardware modules too. These hardware modules communicate information from
sensors and neighboring modules serially to a developers module which then
decides its current state based on information provided. 

Installation Instructions
=========================

Doesn't work yet lol

Note
====

This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
