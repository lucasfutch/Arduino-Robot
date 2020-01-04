import time

from ..robot.tracker import Tracker
from ..robot.controller import Controller
from ..robot.matlab_port import MatlabPort
from ..robot.navigator import Navigator
from ..robot.rover import Rover

if __name__ == "__main__":

    from sys import argv
    if (len(argv) == 6):
        if (argv[1] == '-p' and argv[4] == '-h'):
            try:
                x = float(argv[2])
                y = float(argv[3])
                h = float(argv[5])

                if (x > 0 and x < 1 and y > 0 and y < 1):
                    target_position = [x, y]
                    if (h > 0 and h < 360):
                        final_heading = h
                    else:
                        final_heading = 0
                else:
                    # Default
                    target_position = [0.5, 0.5]
                    final_heading = 0
            except ValueError:
                # Default
                target_position = [0.5, 0.5]
                final_heading = 0

        else:
            # Default
            target_position = [0.5, 0.5]
            final_heading = 0
    else:
        # Default
        target_position = [0.5, 0.5]
        final_heading = 0

    system_time_step = 0.0001
    system_tracker = Tracker()
    timer = time.time()

    # tricicle -- default conotroller is for this guy
    pursuer = Rover(tracker=system_tracker,
                    my_id=0,
                    target_id=None,
                    time_step=system_time_step,
                    comm_port='COM5')

    while(not pursuer.navigator.has_arrived()):

        try:
            # update system state
            system_tracker.update()
            pursuer.update_state(target_pos=target_position)

            if ((time.time() - timer) > system_time_step):
                # update actions
                timer = time.time()
                pursuer.update_action()

        except (KeyboardInterrupt, SystemExit):
            pursuer.stop()
            #matlab_port.close()
            break


    # we have arrived
    pursuer.controller.update_pivot_threshold(10)
    pursuer.controller.update_throttle(0)

    print "Robot has arrived!"

    while(not pursuer.navigator.has_arrived()):

        try:
            # update system state
            system_tracker.update()
            pursuer.update_state(desired_heading=final_heading)

            if ((time.time() - timer) > system_time_step):
                # update actions
                timer = time.time()
                pursuer.update_action()

        except (KeyboardInterrupt, SystemExit):
            pursuer.end()
            break


    ##### END OF PROGRAM ######
