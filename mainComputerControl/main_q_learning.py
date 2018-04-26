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

    # 4-wheeled vehicle
    evader = Rover(tracker=system_tracker,
                   my_id=2,
                   target_id=1,
                   time_step=system_time_step,
                   max_pivot_input=100,
                   forward_speed=100,
                   pivot_threshold=30,
                   proportional_gain=5,
                   integrator_gain=0,
                   reversed=True,
                   comm_port='COM9')

    while(True):
        try:
            # update system state
            system_tracker.update()
            pursuer.update_state()
            evader.update_state()

            if ((time.time() - timer) > system_time_step):
                # update actions
                timer = time.time()
                pursuer.update_action()
                evader.update_action()

        except (KeyboardInterrupt, SystemExit):
            pursuer.end()
            evader.end()
            break
