import time

from tracker import Tracker
from controller import Controller
from matlab_port import MatlabPort
from navigator import Navigator

if __name__ == "__main__":

    time_step = 0.0001

    tracker = Tracker()

    pivot_threshold = 30
    forward_speed = 120



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

            if ((time.time() - timer) > time_step):
            #if (False):
                timer = time.time()
                navigator_pursuer.has_arrived()

                if (my_pos and target_pos):
                    target_heading = navigator_pursuer.get_target_heading(my_pos, target_pos)
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
