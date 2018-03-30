# Arduino Robot

New York University | Abu Dhabi

Embedded Systems Final Project

By: Daniel Carelli and Lucas Futch

# Assignment

Build an autonomous rover that can successfully accomplish the following challenges:
1. Move from point A to point B
2. Move from point A to point B, then pivot to a desired heading
3. Follow a moving leader until contact is made

This project uses reacTIVision to track fiducial markers placed on the autonomous vehicle as well at the target vehicle. A controller on the main computer is used to dictate movement to the rover.

# Architecture
## Rover
The rover consists of an Arduino UNO with an attached motor shield to control two DC motors in order to steer and move the vehicle. In order to communicate with the main computer, the rover has an XBee module configured to operate at 57600 baud. The vehicle is powered by a single 7.4V NiMH battery. The on board Arduino is programmed to receive single byte commands as follows:
* 0 : Stop the vehicle
* 1 : Pivot right
* 2 : Pivot left
* 3 : Move forward
* 4 : Prelimitor for forward motion throttle packet
* 5 : Postlimitor for forward motion throttle packet
* All others : Throttle values

When in pivot mode, the throttle is sent over as one byte. In forward mode, the throttle is sent over in two byte, where the first is the left throttle and the second is right throttle.

## Main Computer
The main computer controls the rover using a python program. It uses a USB XBee module to communicate with the rover. There are three main's, each one for one of the above challenges. Each main instantiates each of the following helper objects:
* Tracker: This class uses reacTIVision as well as the python library pytuio to get the locations and orientations of the rover and its target (if there is a target).  
* Navigator: This class handles navigation for the rover. It takes information regarding the state of the system and returns desired headings as well as recognizing when a mission is complete.
* Controller: This class controls the rover by receiving information about the current state of the system as well as the desired state. Based on the error between these two, it sends commands to rover using an instantiation of the XBee class.
  * XBee: This class handles the serial communication between the main computer and the rover using the XBee module.
* MatlabPort: This class is optionally instantiated and ports heading data to a Matlab port. This data can be used for analysis and tuning.
