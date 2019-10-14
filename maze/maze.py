from collections import deque
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class MazeProblem:
    """
    Coordinate System

    The x-axis is vertical and going downwards, the y-axis is horizontal and
    going left.

    A square at (x, y) means that its upper left corner's coordinate is (x, y).

    If the 2D-array A stores information associated with the maze, then the
    square (x, y)'s information is stored at A[x][y]. Examples of such arrays
    are _map, _patches and _discovered.
    """
    def __init__(self, maze_file=''):
        self._map = self.load_map(maze_file)
        self._fig = plt.figure(figsize=(12.8, 9.6))

        # Contains all the squares and circles created by mpatches so that
        # the rectangle patch corresponding to square (x, y) can be accessed
        # with _patches[x][y]
        self._patches = []

        self._discovered = np.zeros(self._map.shape, np.bool)

        # For a square at (x, y), _predecessors record (x, y)'s predecessor's
        # position relative to (x, y).
        # _predecessors[x, y] == 0 => predecessor is (x - 1, y)
        # _predecessors[x, y] == 1 => predecessor is (x, y + 1)
        # _predecessors[x, y] == 2 => predecessor is (x + 1, y)
        # _predecessors[x, y] == 3 => predecessor is (x, y - 1)
        self._predecessors = np.zeros(self._map.shape)
        self._predecessors[0, 0] = -1   # the entrance has no predecessor

    @staticmethod
    def load_map(file):
        """
        Load map txt as matrix.

        0: path, 1: obstacle, 2: start point, 3: end point
        :1 file: str
        :return: np.ndarray
        """
        return_map = []
        with open(file) as f:
            for line in f:
                row = [int(x) for x in line.rstrip('\n').split(' ')]
                return_map.append(row)
        return_map = np.array(return_map)
        return return_map

    def draw_map(self):
        """
        Visualize the maze map.

        Draw obstacles(1) as red rectangles. Draw path(0) as white rectangles.
        Draw starting point(2) and ending point(3) as circles.
        """
        n_rows, n_cols = self._map.shape
        ax = self._fig.subplots()
        for row in range(n_rows):
            patches_row = []
            for col in range(n_cols):
                if self._map[row, col] == 2:
                    circle = mpatches.Circle((col + 0.5, row + 0.5), 0.5, color='g')
                    patches_row.append(circle)
                    ax.add_patch(circle)
                elif self._map[row, col] == 3:
                    circle = mpatches.Circle((col + 0.5, row + 0.5), 0.5, color='y')
                    patches_row.append(circle)
                    ax.add_patch(circle)
                elif self._map[row, col] == 1:
                    rect = mpatches.Rectangle((col, row), 1, 1, color='r')
                    patches_row.append(rect)
                    ax.add_patch(rect)
                else:
                    rect = mpatches.Rectangle((col, row), 1, 1, fill=False, edgecolor='0.75')
                    patches_row.append(rect)
                    ax.add_patch(rect)
            self._patches.append(patches_row)
        ax.set_xlim(0, n_cols)
        ax.set_ylim(0, n_rows)
        ax.xaxis.set_ticks_position('top')
        ax.invert_yaxis()

    def bfs(self):
        if not os.path.exists('output'):
            os.mkdir('output')

        max_x, max_y = self._map.shape
        self._discovered[0, 0] = True
        queue = deque(((0, 0, 0),))
        axes = self._fig.axes[0]
        frontier_distance = 0
        while len(queue):
            x, y, distance = queue.popleft()
            if distance != frontier_distance:
                self._fig.savefig('output/maze-{}.png'.format(frontier_distance))
                frontier_distance = distance

            self._patches[x][y].set_facecolor('orange')
            self._patches[x][y].set_fill(True)
            # add offset to center the text in the square
            axes.text(y + 0.25, x + 0.75, str(distance), color='w')

            if x + 1 < max_x and not self._discovered[x + 1, y] and self._map[x + 1, y] != 1:
                self._discovered[x + 1, y] = True
                queue.append((x + 1, y, distance + 1))
                self._predecessors[x + 1, y] = 0
            if y + 1 < max_y and not self._discovered[x, y + 1] and self._map[x, y + 1] != 1:
                self._discovered[x, y + 1] = True
                queue.append((x, y + 1, distance + 1))
                self._predecessors[x, y + 1] = 3
            if x - 1 >= 0 and not self._discovered[x - 1, y] and self._map[x - 1, y] != 1:
                self._discovered[x - 1, y] = True
                queue.append((x - 1, y, distance + 1))
                self._predecessors[x - 1, y] = 2
            if y - 1 >= 0 and not self._discovered[x, y - 1] and self._map[x, y - 1] != 1:
                self._discovered[x, y - 1] = True
                queue.append((x, y - 1, distance + 1))
                self._predecessors[x, y - 1] = 1

            if x == max_x - 1 and y == max_y - 1:
                break
        self.print_path()

    def print_path(self):
        x = self._map.shape[0] - 1
        y = self._map.shape[1] - 1
        p = self._predecessors[x, y]
        while p != -1:
            self._patches[x][y].set_facecolor('magenta')

            if p == 0:
                x -= 1
            elif p == 1:
                y += 1
            elif p == 2:
                x += 1
            else:
                y -= 1
            p = self._predecessors[x, y]
        self._fig.savefig('output/path.png')


if __name__ == "__main__":
    Solution = MazeProblem(maze_file='maze.txt')
    Solution.draw_map()
    Solution.bfs()
