import time

from tracker import Tracker
from rover import Rover

if __name__ == "__main__":

    system_time_step = 0.0001
    system_tracker = Tracker()
    timer = time.time()

    pursuer = Rover(time_step = system_time_step,
                    forward_speed = 255,
                    pivot_threshold = 30,
                    tracker = system_tracker,
                    my_id = 2,
                    comm = 'COM9',
                    target_id = None,
                    reversed=True)

    target_heading = 90

    while(True):
        try:
            # update system state
            system_tracker.update()
            pursuer.update_state(desired_heading=target_heading)

            if ((time.time() - timer) > system_time_step):
                # update actions
                timer = time.time()
                pursuer.update_action()

        except (KeyboardInterrupt, SystemExit):
            pursuer.end()
            break
