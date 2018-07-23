import numpy as np

class CoulombAgent(object):
    def __init__(self, env):
        self.env = env
        self.pos = [0, 0]
        self.pursuer_pos = None
        self.env_height = env.arena_height
        self.env_width = env.arena_width
        self.evasion_factor = 5
        self.obstacles = []
        self.build_arena_walls()

    def build_arena_walls(self):

        # build left wall
        left_wall = []
        for i in range(self.env_height+1):
            left_wall.append([0, i])
        self.obstacles.append(left_wall)

        # build right wall
        right_wall = []
        for i in range(self.env_height+1):
            right_wall.append([self.env_width+1, i])
        self.obstacles.append(right_wall)

        # build bottom wall
        bottom_wall = []
        for i in range(self.env_width+1):
            bottom_wall.append([i, 0])
        self.obstacles.append(bottom_wall)

        # build top wall
        top_wall = []
        for i in range(self.env_width+1):
            top_wall.append([i, self.env_height+1])
        self.obstacles.append(top_wall)


    def calc_net_force(self):
        fx_net = 0
        fy_net = 0
        for obstacle in self.obstacles:
            fx_obstacle = 0
            fy_obstacle = 0
            for point in obstacle:
                dx = np.float64(self.pos[0] - point[0])
                dy = np.float64(self.pos[1] - point[1])
                r = np.sqrt((dx*dx) + (dy*dy))

                fx_obstacle -= (self.evasion_factor*dx)/np.power(r, 1.5)
                fy_obstacle -= (self.evasion_factor*dy)/np.power(r, 1.5)

            fx_net += fx_obstacle
            fy_net += fy_obstacle

        return [fx_net, fy_net]


    def get_target_heading(self):
        # get relevant state parameters from environment
        self.pos[0] = self.env.evader.pos[0]
        self.pos[1] = self.env_width - self.env.evader.pos[1]
        self.pursuer_pos = self.env.pursuer.pos

        net_force = self.calc_net_force()

        desired_heading = self.calculate_heading(net_force[0], net_force[1])

        return desired_heading

    def calculate_heading(self, fx, fy):

        complementary_angle = np.arctan(abs(fy)/abs(fx))*(180.0/np.pi)

        # Quadrant 1
        if (fx > 0 and fy > 0):
            desired_heading = 90 - complementary_angle

        # Quadrant 2
        elif (fx > 0 and fy < 0):
            desired_heading = 90 + complementary_angle

        # Quadrant 3
        elif (fx < 0 and fy < 0):
            desired_heading =  270 - complementary_angle

        # Quadrant 4
        else:
            desired_heading =  270 + complementary_angle

        return desired_heading

    def f_from_pursuer(self):
        dx = np.float64(self.pos[0] - self.pursuer_pos[0])
        dy = np.float64(self.pos[1] - self.pursuer_pos[1])
        r_squared = np.float64((dx*dx) + (dy*dy))

        fx = (self.evasion_factor*dx)/r_squared
        fy = (self.evasion_factor*dy)/r_squared

        return [fx, fy]

if __name__ == '__main__':
    a = CoulombAgent(None)
    a.env_width = 1000
    a.env_length = 1000

    print "\nTOP WALL"
    for i in range(11):
        a.pos = [i*100, 200]
        print a.f_bottom_wall()
