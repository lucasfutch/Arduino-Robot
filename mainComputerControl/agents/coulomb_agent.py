import numpy as np

class CoulombAgent(object):
    def __init__(self, env):
        self.env = env
        self.pos = [0, 0]
        self.pursuer_pos = None
        self.env_height = env.arena_height
        self.env_width = env.arena_width
        self.evasion_factor = 5000

    def get_target_heading(self):

        fx, fy = self.calculate_forces()

        complementary_angle = np.arctan(abs(fy)/abs(fx))*(180.0/np.pi)

        # Quadrant 1
        if (fx > 0 and fy > 0):
            net_force = 90 - complementary_angle

        # Quadrant 2
        elif (fx > 0 and fy < 0):
            net_force = 90 + complementary_angle

        # Quadrant 3
        elif (fx < 0 and fy < 0):
            net_force =  270 - complementary_angle

        # Quadrant 4
        elif (fx < 0 and fy > 0):
            net_force =  270 + complementary_angle

        else:
            print "Exception time"
            net_force =  270 + complementary_angle

        return net_force

    def calculate_forces(self):
        # get relevant state parameters from environment
        self.pos[0] = self.env.evader.pos[0]
        self.pos[1] = self.env_width - self.env.evader.pos[1]
        self.pursuer_pos = self.env.pursuer.pos

        f_left_wall = self.f_left_wall()
        f_right_wall = self.f_right_wall()
        f_top_wall = self.f_top_wall()
        f_bottom_wall = self.f_bottom_wall()
        f_from_pursuer = self.f_from_pursuer()

        fx = f_left_wall[0] + \
             f_top_wall[0]  + \
             f_right_wall[0] + \
             f_bottom_wall[0] + \
             f_from_pursuer[0]

        fy = f_left_wall[1] + \
             f_top_wall[1]  + \
             f_right_wall[1] + \
             f_bottom_wall[1] + \
             f_from_pursuer[1]

        return fx, fy

    def f_left_wall(self):
        x = np.float64(self.pos[0])
        y = np.float64(self.pos[1])

        return [self.fx(x, y, self.env_height),
                self.fy(x, y, self.env_height)]

    def f_right_wall(self):
        x = np.float64(self. env_width - self.pos[0])
        y = np.float64(self.pos[1])

        return [-1*self.fx(x, y, self.env_height),
                   self.fy(x, y, self.env_height)]

    def f_top_wall(self):
        x_prime = np.float64(self.env_height - self.pos[1])
        y_prime = np.float64(self.pos[0])

        fx_prime = self.fx(x_prime, y_prime, self.env_width)
        fy_prime = self.fy(x_prime, y_prime, self.env_width)

        fx = fy_prime
        fy = -1*fx_prime

        return [fx, fy]

    def f_bottom_wall(self):
        x_prime = np.float64(self.pos[1])
        y_prime = np.float64(self.env_width - self.pos[0])

        fx_prime = self.fx(x_prime, y_prime, self.env_width)
        fy_prime = self.fy(x_prime, y_prime, self.env_width)

        fx = -1*fy_prime
        fy = fx_prime

        return [fx, fy]

    def fx(self, x, y, L):
        start = (-y)/(x*np.sqrt((0-y)**2+x**2))
        end = (L-y)/(x*np.sqrt((L-y)**2+x**2))

        return end-start

    def fy(self, x, y, L):
        start = 1.0/np.sqrt(x**2+y**2)
        end = 1.0/np.sqrt(L**2-2*L*y+x**2+y**2)

        return end-start

    def f_from_pursuer(self):
        dx = np.float64(self.pos[0] - self.pursuer_pos[0])
        dy = np.float64(self.pos[1] - self.pursuer_pos[1])
        r = np.sqrt((dx*dx) + (dy*dy))

        fx = (self.evasion_factor*dx)/np.power(r, 3)
        fy = (self.evasion_factor*dy)/np.power(r, 3)

        return [fx, fy]

if __name__ == '__main__':
    a = CoulombAgent(None)
    a.env_width = 1000
    a.env_length = 1000

    print "\nTOP WALL"
    for i in range(11):
        a.pos = [i*100, 200]
        print a.f_bottom_wall()
