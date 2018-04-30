from environment import Environment

if __name__ == '__main__':
    time_step = 0.3
    env = Environment(time_step, 'COM5', 'COM9')

    while True:
        a = raw_input('ENTER to reset')
        env.reset([0.8, 0.8], [0.2, 0.8])
        a = raw_input('ENTER to reset')
        env.reset([0.8, 0.2], [0.8, 0.8])
        a = raw_input('ENTER to reset')
        env.reset([0.2, 0.2], [0.8, 0.2])
        a = raw_input('ENTER to reset')
        env.reset([0.2, 0.8], [0.2, 0.2])
