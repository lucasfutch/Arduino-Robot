import time

from tracker import Tracker
from rover import Rover

if __name__ == "__main__":

    system_time_step = 0.0001
    system_tracker = Tracker()
    timer = time.time()

    pursuer = Rover(time_step = system_time_step,
                    forward_speed = 120,
                    pivot_threshold = 30,
                    tracker = system_tracker,
                    my_id = 0,
                    target_id = 2):)

    while(True):
        try:
            # update system state
            tracker.update()
            pursuer.update_state()

            if ((time.time() - timer) > time_step):
                # update actions
                timer = time.time()
                pursuer.update_action()

        except (KeyboardInterrupt, SystemExit):
            pursuer.end()
            break
