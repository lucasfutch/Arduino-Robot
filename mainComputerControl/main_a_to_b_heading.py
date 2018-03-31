import time

from tracker import Tracker
from controller import Controller
from matlab_port import MatlabPort
from navigator import Navigator

if __name__ == "__main__":

    from sys import argv
    if (argv[1] == '-p' and argv[4] == '-h'):
        print argv
        target_pos = [argv[2], argv[3]]
        final_heading = argv[5]
    else:
        target_pos = [0.5, 0.5]
        final_heading = 0

    time_step = 0.0001

    tracker = Tracker()
    #matlab_port = MatlabPort()
    pivot_threshold = 30
    forward_speed = 80
    navigator = Navigator()
    controller = Controller(time_step, forward_speed, pivot_threshold)

    target_heading = 0
    my_pos = [0, 0]

    motor_input = 3
    timer = time.time()

    while(not navigator.has_arrived()):

        try:
            # update system state
            tracker.update()
            current_heading = tracker.get_my_heading()
            my_pos = tracker.get_my_pos()

            if ((time.time() - timer) > time_step):
            #if (False):
                timer = time.time()
                navigator.has_arrived()

                if (my_pos and target_pos):
                    target_heading = navigator.get_target_heading(my_pos, target_pos)
                    pass

                    # there is new data (fiducial is in view)
                    port_info = int(current_heading*(255.0/360.0))
                    #matlab_port.send_byte(port_info)

                    controller.update_motors(current_heading, target_heading)

                else:
                    # no new data (fiducial is not in view)
                    controller.coast()

        except (KeyboardInterrupt, SystemExit):
            controller.stop()
            #matlab_port.close()
            break

    # we have arrived
    controller.stop()
    controller.update_pivot_threshold(10)
    controller.update_throttle(0)

    print "Robot has arrived!"

    while (True):
        if ((time.time() - timer) > time_step):
            try:
                tracker.update()
                current_heading = tracker.get_my_heading()
                controller.update_motors(current_heading, final_heading)

            except (KeyboardInterrupt, SystemExit):
                controller.stop()
                #matlab_port.close()
                break
        else:
            # no new data (fiducial is not in view)
            controller.coast()


    ##### END OF PROGRAM ######
