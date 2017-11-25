#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: env.py
Author: Cade Parkison
Email: cadeparkison@gmail.com
Github: c-park
Description:  Environment class GridMap to read in map text files, and animate
              motions of a multi-agent pickup and delivery system

    map_files: text file representing static map before agents are added or
               tasks are assigned
        - x: occupied grid
        - 0: unoccupied grid
        - e: task endpoint, can be either pickup or delivery location

    TODO:
        - add dynamic grid and axis ticks for any sized map, not just warehouse
        - add indicators for task start and end locations, while being able to
        remove once a task is complete
        - add more robust color scheme for more than 7 unique colors.
        - add a way to visualize entire paths in static image
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import heapq
from math import hypot, fabs
import sys


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=1, metadata=dict(artist='Me'), bitrate=1800)


_DEBUG = False
_GOAL_COLOR = 0.45
_INIT_COLOR = 0.25
_ENDPOINT_COLOR = 0.4
_COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

class GridMap:
    def __init__(self, map_path=None, use_cost=False):
        '''
        Constructor. Makes the necessary class variables. Optionally reads in a
        provided map file given by map_path.

        map_path (optional) - a string of the path to the file on disk
        '''
        self.rows = None
        self.cols = None
        self.endpoints = []
        self.tasks = []        # tuples containing pickup and delivery locations
        self.init_agents = []  # agent initial positions (non-task endpoints)
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
            0 - Cell unoccupied
            e - task endpoints (possible pickup or delivery locations)

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

    def display_map(self, paths=[], record=False):
        '''
        Visualize the map read in. Optionally display the resulting plans for
        all agents

        paths - A matrix describing paths taken by all agents. Rows correspond
                to agents, columns correspond to time steps.
                Each matrix element is a tuple of 2d position or a "0" if the
                agent is waiting for that timestep.
        '''

        for i, path in enumerate(paths):
            path = [p[:2] for p in path]
            for j, tuple in enumerate(path):
                transTuple = (tuple[1],tuple[0])
                paths[i][j] = transTuple

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
        agent_ids = []
        for i, path in enumerate(paths):
            agents.append(mpl.patches.Circle(path[0], 0.5,
                                             color=_COLORS[i%len(_COLORS)]))

        for i,path in enumerate(paths):
            plt.plot(*zip(*path), color=_COLORS[i%len(_COLORS)])

        def init():
            """
            Initializes agents to starting position
            """
            for a in range(len(agents)):
                ax.add_patch(agents[a])
            return agents

        def animate(i):
            """
            Iterate agent position by time step. Location of 0 means agent is
            waiting.
            """
            for a in range(len(agents)):
                # If not at end of path, move agent to next position.
                try:
                    # if location is not 0, try to move forward.
                    if paths[a][i]:
                        agents[a].center = paths[a][i]
                    else:
                        pass
                except IndexError:
                    # if at end of path, agent stays.
                    agents[a].center = paths[a][-1]

            return agents

        anim = animation.FuncAnimation(fig, animate,
                                        init_func=init,
                                        frames=15,        # animation frames
                                        interval=1000,    # time between frames (ms)
                                        repeat=False,
                                        blit=True)

        if record:
            anim.save('trial_animation.mp4', writer=writer)

        # ax.set_yticks(np.arange(0,20,5))
        ax.set_xticks(np.arange(-.5, self.cols, 1), minor=True);
        ax.set_yticks(np.arange(-.5, self.rows, 1), minor=True);
        ax.grid(which='minor', color='k', linewidth=0.5)

        plt.show()

def main(args):
    # test path of 4 agents, the zeros represent an agent waiting one time step
    test_paths = [[(1,1),0,0,0,0,(1,2),(2,2),(3,2)],
                  [(5,1),(5,2),0,(5,3),(5,4),(5,5)],
                  [(1,5),(1,6),(1,7),(1,8),(1,9)],
                  [(2,7),(3,7),(3,8),(3,9),0,(3,10)]]

    test = GridMap('env_files/{}'.format(args[1]))
    test.display_map()

if __name__ == "__main__":
    main(sys.argv)


