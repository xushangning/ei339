import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.pyplot import MultipleLocator


class Environment(object):
    def __init__(self, rows=5, cols=8, barrier_num=3, reward_num=5):
        self.rows = rows
        self.cols = cols
        self.barrier_num = barrier_num
        self.reward_num = reward_num
        self.create_env_default()

    def create_env_default(self):
        """
        Create the final matrix of environment in our problem

        start node = 1, terminal node = 2, cliff = -1, barrier = -2, reward = 3

        All grids of type 3 now carry a reward of -1.
        [[1. - 1. - 1. - 1. - 1. - 1. - 1.  2.]
        [0.  0.  0.  0.  0.  0. - 2.  0.]
        [0.  0.  0.  3. - 2.  0.  0.  0.]
        [3.  0.  0.  0. - 2.  0.  0.  3.]
        [0.  0.  3.  0.  0.  0.  0.  0.]]
        """

        self.env = np.zeros([self.rows, self.cols])
        # start node = 1, terminal node = 2, cliff = -1
        self.env[0][0] = 1
        self.env[0][self.cols-1] = 2
        self.env[0][1:self.cols-1] = -1

        # set barrier pos
        barrier_pos = [[3, 4], [2, 4], [1, 6]]
        # set barrier = -2
        for pos in barrier_pos:
            self.env[pos[0]][pos[1]] = -2

        # set reward pos
        reward_pos = [[3, 0], [2, 3], [4, 2], [3, 7]]
        # set reward = 3
        for pos in reward_pos:
            self.env[pos[0]][pos[1]] = 3

    def create_env(self):
        self.env = np.zeros([self.rows, self.cols])
        # start node = 1, terminal node = 2, cliff = -1
        self.env[0][0] = 1
        self.env[0][self.cols-1] = 2
        self.env[0][1:self.cols-1] = -1

        # randomly set barrier pos
        barrier_pos = []
        while(len(barrier_pos) < self.barrier_num):
            i = random.randint(1, self.rows-1)
            j = random.randint(0, self.cols-1)
            if [i, j] not in barrier_pos and [i, j] not in [[1, 0], [1, self.cols-1]]:
                barrier_pos.append([i, j])

        # set barrier = -2
        for pos in barrier_pos:
            self.env[pos[0]][pos[1]] = -2

        # randomly set reward pos
        reward_pos = []
        while (len(reward_pos) < self.reward_num):
            i = random.randint(1, self.rows - 1)
            j = random.randint(0, self.cols - 1)
            if [i, j] not in reward_pos and [i, j] not in barrier_pos:
                reward_pos.append([i, j])

        # set reward = 3
        for pos in reward_pos:
            self.env[pos[0]][pos[1]] = 3

    def plot(self):
        """
        :return: matplotlib.figure.Figure
        """
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.cols)
        ax.set_ylim(0, self.rows)
        # name: start, terminal, cliff, barrier, reward, others
        # number: 1, 2, -1, -2, 3, 0
        # color: yellow, orange, gray, black, red, white
        color_dict = {-1:"gray", 1:"yellow", 2:"orange", -2:"black", 3:"red", 0:"white"}
        my_x_ticks = np.arange(0, self.cols, 1)
        my_y_ticks = np.arange(0, self.rows, 1)
        ax.set_xticks(my_x_ticks)
        ax.set_yticks(my_y_ticks)
        x_major_locator = MultipleLocator(1)
        y_major_locator = MultipleLocator(1)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        ax.xaxis.set_ticks_position('top')
        ax.invert_yaxis()

        ax.grid()
        for i in range(self.rows):
            for j in range(self.cols):
                color = color_dict[int(self.env[i][j])]
                rect = mpatches.Rectangle((j, i), 1, 1, color=color)
                ax.add_patch(rect)

        return fig


class Sarsa():
    def __init__(self, env):
        self.env = env.env
        self.rows = env.rows
        self.cols = env.cols

    # sarsa learning
    def learning(self, max_episode_num, gamma=0.9):
        """
        :param max_episode_num: total episode num
        :param gamma: the discount factor
        """
        print("sarsa learning")


if __name__ == "__main__":
    Env = Environment()
    print("the environment matrix:")
    print(Env.env)
    Env.plot()

    sarsa = Sarsa(Env)
    # sarsa.learning(max_episode_num=300)
