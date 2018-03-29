from xbee import XBee

class Controller(object):
    def __init__(self, kp, ki, dt):
        self.current_heading = None
        self.target_heading = None
        self.error = None
        self.integrator = 0
        self.max = 100
        self.kp = kp
        self.ki = ki
        self.dt = dt
        self.xBee = XBee()
        self.motor_input = 0

    def update_motors(self, current_heading, target_heading):
        # update state
        self.current_heading = current_heading
        self.target_heading = target_heading

        # calculate error
        self.get_error()

        # calculate motor inputs
        self.get_motor_input()

        # command the motors
        self.command_motors()

    def get_error(self):

        self.error = (self.target_heading - self.current_heading)

        if (abs(self.error) >= 180):
            self.error = (360 + self.target_heading - self.current_heading)

        return self.error

    def get_motor_input(self):
        # update error
        self.get_error(self.current_heading, self.target_heading)

        # update integrator term
        self.update_integrator()

        #   result     proportional gain        integral gain        bias
        motor_input = (self.kp*self.error)+(self.ki*self.integrator)+3

        if (abs(motor_input) > self.max):
            self.motor_input = int(motor_input/abs(motor_input))*self.max
            return

        self.motor_input = motor_input

    def update_integrator(self):
        self.integrator += self.error*self.dt

    def command_motors(self):
        # determine direction
        if (self.motor_input >= 0):
            self.xBee.send_command(1)
        else:
            self.xBee.send_command(2)

        # send motor speed
        self.xBee.send_command(abs(motor_input))

    def coast(self):
        self.motor_input -= 20
        if (self.motor_input < 3):
            self.motor_input = 3;
        self.xBee.send_command(abs(self.motor_input))

    def stop(self):
        self.xBee.send_command(3)
