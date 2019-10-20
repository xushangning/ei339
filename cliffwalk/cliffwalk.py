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
        fig, ax = plt.subplots(figsize=(8, 6))
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

    def valid_position(self, x, y):
        """(x, y) can't be outside the environment or on a barrier"""
        return 0 <= x < self.cols and 0 <= y < self.rows and self.env[y][x] != -2


class Sarsa():
    def __init__(self, env):
        self.env = env
        self.map = env.env
        self.rows = env.rows
        self.cols = env.cols
        self.fig = env.plot()

    # sarsa learning
    def learning(self, n_episodes, gamma=0.9):
        """
        :param n_episodes: total episode num
        :param gamma: the discount factor
        """
        ax = self.fig.axes[0]
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.map[i][j]:
                    ax.add_patch(mpatches.Polygon(
                        ((j, i), (j + 0.5, i + 0.5), (j + 1, i)),
                        fill=False,
                        color='black'
                    ))
                    ax.add_patch(mpatches.Polygon(
                        ((j + 1, i), (j + 1, i + 1), (j + 0.5, i + 0.5)),
                        fill=False,
                        color='black'
                    ))
                    ax.add_patch(mpatches.Polygon(
                        ((j + 1, i + 1), (j, i + 1), (j + 0.5, i + 0.5)),
                        fill=False,
                        color='black'
                    ))
                    ax.add_patch(mpatches.Polygon(
                        ((j, i), (j + 0.5, i + 0.5), (j, i + 1)),
                        fill=False,
                        color='black'
                    ))

        eta = 0.5
        q_values = np.zeros((self.rows, self.cols, 4), np.float64)

        for _ in range(n_episodes):
            prev_action = random.randrange(4)
            prev_x, prev_y = 0, 0
            while True:
                x, y = self.walk_one_step(prev_x, prev_y, prev_action)
                if not self.env.valid_position(x, y):
                    x, y = prev_x, prev_y

                state_type = self.map[y][x]
                reward = 0
                if state_type == -1:
                    reward = -100
                elif state_type == 3:
                    reward = -1
                elif state_type == 2:
                    reward = 10

                action = random.randrange(4)
                q_values[prev_y][prev_x][prev_action] = (
                        (1 - eta) * q_values[prev_y][prev_x][prev_action]
                    + eta * (reward + gamma * q_values[y][x][action])
                )

                if state_type == 2 or state_type == -1:
                    break
                prev_x, prev_y, prev_action = x, y, action

        for i in range(self.rows):
            for j in range(self.cols):
                if not self.map[i][j]:
                    ax.text(j + 0.3, i + 0.25, '{:.1f}'.format(q_values[i][j][0]))
                    ax.text(j + 0.6, i + 0.55, '{:.1f}'.format(q_values[i][j][1]))
                    ax.text(j + 0.3, i + 0.95, '{:.1f}'.format(q_values[i][j][2]))
                    ax.text(j + 0.03, i + 0.55, '{:.1f}'.format(q_values[i][j][3]))
        self.fig.show()

    @staticmethod
    def walk_one_step(x, y, direction):
        """Walk one step in one of four directions"""
        if direction == 0:      # up
            return x, y - 1
        elif direction == 1:    # right
            return x + 1, y
        elif direction == 2:    # down
            return x, y + 1
        else:                   # left
            return x - 1, y


if __name__ == "__main__":
    Env = Environment()
    sarsa = Sarsa(Env)
    sarsa.learning(5000)
