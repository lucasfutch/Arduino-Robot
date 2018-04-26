import time

from tracker import Tracker
from controller import Controller
from matlab_port import MatlabPort
from navigator import Navigator

if __name__ == "__main__":

    from sys import argv
    if (len(argv) == 4):
        if (argv[1] == '-p'):
            try:
                x = float(argv[2])
                y = float(argv[3])
                if (x > 0 and x < 1 and y > 0 and y < 1):
                    target = [x, y]
                else:
                    # Default
                    target = [0.5, 0.5]
            except ValueError:
                # Default
                target = [0.5, 0.5]
        else:
            # Default
            target = [0.5, 0.5]
    else:
        # Default
        target = [0.5, 0.5]


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
            pursuer.update_state(target_pos=target)

            if ((time.time() - timer) > system_time_step):
                # update actions
                timer = time.time()
                pursuer.update_action()

        except (KeyboardInterrupt, SystemExit):
            controller.stop()
            #matlab_port.close()
            break

    # we have arrived
    pursuer.end()
    print "Robot has arrived!"

    ##### END OF PROGRAM ######
