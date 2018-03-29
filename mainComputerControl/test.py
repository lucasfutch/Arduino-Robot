import time

from xbee import XBee
from tracker import Tracker
from controller import Controller
from matlab_port import MatlabPort
from navigator import Navigator

if __name__ == "__main__":
    xBee = XBee()
    tracker = Tracker()
    navigator = Navigator()
    controller = Controller((253.0/360.0)*2.5)

    target_heading = 0
    my_pos = [0, 0]
    target_pos = [0, 0]

    motor_input = 3
    timer = time.time()

    while(True):

        try:
            # update system state
            tracker.update()
            current_heading = tracker.get_my_heading()
            my_pos = tracker.get_my_pos()
            target_pos = tracker.get_target_pos()

            if (current_heading):
                print "Heading: %s; My Pos: (%s, %s)" % (current_heading, my_pos[0], my_pos[1])
            if (target_pos):
                print "Target Pos: (%s, %s)" % (target_pos[0], target_pos[1])



        except (KeyboardInterrupt, SystemExit):
            break
