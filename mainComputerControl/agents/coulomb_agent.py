import numpy as np

class CoulombAgent(object):
    def __init__(self, env):
        self.env = env
        self.pos = self.env.pursuer.pos
        self.pursuer_pos = None
        self.env_length = env.arena_length
        self.env_width = env.arena_width

    def get_target_heading(self):
        # get relevant state parameters from environment
        self.pos = self.env.evader.pos
        self.pursuer_pos = self.env.pursuer.pos

        f_left_wall = self.f_left_wall()
        f_right_wall = self.f_right_wall()
        f_top_wall = self.f_top_wall()
        f_bottom_wall = self.f_bottom_wall()


        fx = f_left_wall[0] + \
             f_right_wall[0] + \
             f_top_wall[0] + \
             f_bottom_wall[0]

        fy = f_left_wall[1] + \
             f_right_wall[1] + \
             f_top_wall[1] + \
             f_bottom_wall[1]

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
        else:
            net_force =  270 + complementary_angle

        print net_force
        return net_force

    def f_left_wall(self):
        x = np.float64(self.pos[0])
        y = np.float64(self.pos[1])

        return [self.fx(x, y, self.env_width),
                self.fy(x, y, self.env_width)]

    def f_right_wall(self):
        x = np.float64(self.env_length - self.pos[0])
        y = np.float64(self.pos[1])

        return [-1*self.fx(x, y, self.env_width),
                   self.fy(x, y, self.env_width)]

    def f_top_wall(self):
        x = np.float64(self.pos[1])
        y = np.float64(self.pos[0])

        return [self.fy(x, y, self.env_length),
                -1*self.fx(x, y, self.env_length)]

    def f_bottom_wall(self):
        x = np.float64(self.env_width-self.pos[1])
        y = np.float64(self.pos[0])

        return [self.fy(x, y, self.env_length),
                self.fx(x, y, self.env_length)]

    def fx(self, x, y, L):
        start = np.arctan(-y/x)
        end = np.arctan((L-y)/x)

        return end-start

    def fy(self, x, y, L):
        start = -0.5*np.log((x*x)+(y*y))
        end = -0.5*np.log((L*L)-(2*L*y)+(x*x)+(y*y))

        return end-start

if __name__ == '__main__':
    a = CoulombAgent(None)
    a.env_width = 1000
    a.env_length = 1000

    print "\nTOP WALL"
    for i in range(11):
        a.pos = [i*100, 200]
        print a.f_bottom_wall()
