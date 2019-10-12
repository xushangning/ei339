import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes


class MazeProblem:
    def __init__(self, maze_file=''):
        self.map = self.load_map(maze_file)

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
        n_rows, n_cols = self.map.shape
        plt.figure(figsize=(12.8, 9.6))
        ax = plt.subplot()
        for row in range(n_rows):
            for col in range(n_cols):
                if self.map[row, col] == 2:
                    circle = mpathes.Circle((col + 0.5, row + 0.5), 0.5, color='g')
                    ax.add_patch(circle)
                elif self.map[row,col] == 3:
                    circle = mpathes.Circle((col + 0.5, row + 0.5), 0.5, color='y')
                    ax.add_patch(circle)
                elif self.map[row, col] == 1:
                    rect = mpathes.Rectangle((col, row), 1, 1, color='r')
                    ax.add_patch(rect)
                else:
                    rect = mpathes.Rectangle((col, row), 1, 1, fill=False, edgecolor='0.75')
                    ax.add_patch(rect)
        plt.xlim((0, n_cols))
        plt.ylim((0, n_rows))
        axis = plt.gca()
        axis.xaxis.set_ticks_position('top')
        axis.invert_yaxis()
        plt.savefig('maze.jpg')


if __name__ == "__main__":
    Solution = MazeProblem(maze_file='maze.txt')
    Solution.draw_map()
