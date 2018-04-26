import time

from tracker import Tracker
from rover import Rover

if __name__ == "__main__":

    system_time_step = 0.0001
    system_tracker = Tracker()
    timer = time.time()

    # tricicle -- default conotroller is for this guy
    pursuer = Rover(tracker=system_tracker,
                    my_id=0,
                    target_id=2,
                    time_step=system_time_step,
                    comm_port='COM5')

    while(True):
        try:
            # update system state
            system_tracker.update()
            pursuer.update_state()

            if ((time.time() - timer) > system_time_step):
                # update actions
                timer = time.time()
                pursuer.update_action()

        except (KeyboardInterrupt, SystemExit):
            pursuer.end()
            break
