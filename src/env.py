#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import heapq
from math import hypot, fabs

_DEBUG = False
_DEBUG_END = True
_GOAL_COLOR = 0.45
_INIT_COLOR = 0.25
_ROBOT_COLOR = 0.75
#_PICKUP_COLOR = 0.65
_ENDPOINT_COLOR = 0.4

_COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

class GridMap:
    def __init__(self, map_path=None, use_cost=False):
        '''
        Constructor. Makes the necessary class variables. Optionally reads in a provided map
        file given by map_path.

        map_path (optional) - a string of the path to the file on disk
        '''
        self.rows = None
        self.cols = None
        self.endpoints = []
        self.tasks = []        # tuples containing pickup and delivery locations
        self.init_agents = []  # agent initial positions (i.e. non-task endpoints)
        self.occupancy_grid = None
        self.use_costs = use_cost
        if map_path is not None:
            self.read_map(map_path)

    def read_map(self, map_path):
        '''
        Read in a specified map file of the format described as follows:

        map_path - a string of the path to the file on disk

        txt file consists of a grid system specified as follows:
            x - Cell occupied in grid by an obstacle
            e - task endpoints (possible pickup or delivery locations)
            i - initial locations of agents (i.e. non-task endpoints)

        '''
        map_file = file(map_path,'r')
        lines = [l.rstrip().lower() for l in map_file.readlines()]
        map_file.close()
        self.rows = len(lines)
        self.cols = max([len(l) for l in lines])
        if _DEBUG:
            print 'rows', self.rows
            print 'cols', self.cols
            print lines
        self.occupancy_grid = np.zeros((self.rows, self.cols), dtype=np.bool)
        for r in xrange(self.rows):
            for c in xrange(self.cols):
                if lines[r][c] == 'x':
                    self.occupancy_grid[r][c] = True
                if lines[r][c] == 'e':
                    self.endpoints.append((r,c))

    def display_map(self, paths=[]):
        '''
        Visualize the map read in. Optionally display the resulting plans for all agents

        paths - an array describing paths taken by all agents, where each element is a tuple of 2d position.
                - columns: time steps
                - rows: agents
        '''
        fig, ax = plt.subplots()
        display_grid = np.array(self.occupancy_grid, dtype=np.float32)

        for e in self.endpoints:
            display_grid[e] = _ENDPOINT_COLOR

        # Plot display grid for visualization
        imgplot = ax.imshow(display_grid)
        # Set interpolation to nearest to create sharp boundaries
        imgplot.set_interpolation('nearest')
        imgplot.set_cmap('Greys')

        # create circles to represent each agent in starting position
        agents = []
        for i, path in enumerate(paths):
            agents.append(mpl.patches.Circle(path[0], 0.5, color=_COLORS[i%len(_COLORS)]))

        # Animate paths of agents
        def init():
            for a in range(len(agents)):
                ax.add_patch(agents[a])
            return agents

        def animate(i):
            for a in range(len(agents)):
                try:
                    agents[a].center = paths[a][i]
                except IndexError:
                    agents[a].center = paths[a][-1]

            return agents

        anim = animation.FuncAnimation(fig, animate,
                           init_func=init,
                           frames=10,
                           interval=1000,
                           repeat=False,
                           blit=True)

        ax.set_yticks(np.arange(0,20,5))
        ax.set_xticks(np.arange(-.5, 35, 1), minor=True);
        ax.set_yticks(np.arange(-.5, 21, 1), minor=True);
        ax.grid(which='minor', color='k', linewidth=0.5)

        plt.show()

def main():
    test_paths = [[(1,1),(1,2),(2,2),(3,2)],
                  [(5,1),(5,2),(5,3),(5,4),(5,5)],
                  [(1,5),(1,6),(1,7),(1,8),(1,9)],
                  [(2,7),(3,7),(3,8),(3,9),(3,10)]]
    test = GridMap('env_files/env_warehouse.txt')
    test.display_map(paths=test_paths)

if __name__ == "__main__":
    main()


