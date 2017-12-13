#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: reserv_table.py
Authors: Taylor Welker, Cade Parkison, Paul Wadsworth
Emails: <taylormaxwelker@gmail.com>,  <cadeparkison@gmail.com>, <wadspau2@gmail.com>
Githubs: welkerCode, c-park
Description: Reservation Table class that holds reserved states in Space-Time
"""

from itertools import groupby

class Reserv_Table:
    '''
    The reservation table is a dictionary of dictionaries. The outer dictionary
    uses X values as the key to accessing Y values and their occupation status
    over time. The inner dictionary uses the Y values as the key, and they yield
    another dictionary. This dictionary uses the timestep as the key, and the
    occupation status of that position at the desired timestep is returned
    '''

    def __init__(self, occupancyGrid = [], rows = 0, cols = 0):
        self.res_table = {}
        self.staticObstacle = {}
        self.rows = rows
        self.cols = cols
        for r in xrange(rows):
            for c in xrange(cols):
                if occupancyGrid[r][c] == True:
                    self.staticObstacle[(r,c)] = True

    def display(self, env):
        """
        Prints a formatted version of the reservation table at each timestep
        """
        sorted_keys = sorted(self.res_table.iterkeys(), key = lambda x: x[2])

        time_steps = [list(j) for i, j in groupby(sorted_keys, key=lambda x:x[2])]

        print('\nReservation Table:')
        for t in range(len(time_steps)):
            table = ''
            for i in range(env.rows):
                row = ''
                for j in range(env.cols):
                    if (i,j,t) in time_steps[t]:
                        row+='x'
                    else:
                        row+='0'
                table += row
                table += '\n'
            print('------------')
            print('Timestep: {}\n'.format(t))
            print(table)

    def checkStateResv(self, state, time):
        """
        Returns True if state is reserved in table
        """
        return self.res_table.has_key((state[0], state[1], time))

    def resvState(self, state):
        """
        Reserves a single state in table
        """
        self.res_table[state] = True

    def resvPath(self, pathList, init_timestep):
        """
        Reserves Paths in table
        """
        currentTimestep = init_timestep
        for time, state in enumerate(pathList):
            self.res_table[(state[0], state[1], time+currentTimestep)] = True
            self.res_table[(state[0], state[1], time+currentTimestep+1)] = True

    def resvAgentInit(self, agents):
        """
        Reserves agents initial state in table
        """
        for agent in agents:
            self.res_table[agent.currentState[0], agent.currentState[1], 0] = True
            self.res_table[agent.currentState[0], agent.currentState[1], 1] = True

    def resvAgentInitWHCA(self, agents, currentTimestep):
        """
        Reserves agents initial state in table
        """
        for agent in agents:
            self.res_table[agent.currentState[0], agent.currentState[1], currentTimestep] = True
            # self.res_table[agent.currentState[0], agent.currentState[1], 1] = True

    def clearPlan(self, agent_plan):
        """
        """
        for state in agent_plan:
            self.res_table.pop(state)

    def transition3D(self, s, a):
        '''
        Transition function for the current grid map.

        s - tuple describing the state as (row, col, t) position in the reservation table.
        a - the action to be performed from state s

        returns - s_prime (row', col', t+1), the state transitioned to by taking
        action a in state s. If the action is not valid (e.g. moves off the grid
        or into an obstacle) returns the current state with t+1.
        '''
        new_pos = list(s[:])
        _COL = 1  # Index of s for col
        _ROW = 0  # Index of s for row
        _t = 2  # Index of s for time

        # Ensure action stays on the board
        cost = 0.
        if a == 'u':
            if s[_ROW] > 0:
                new_pos[_ROW] -= 1
                cost = 1.
                new_pos[_t] = s[_t] + 1
        elif a == 'd':
            if s[_ROW] < self.rows - 1:
                new_pos[_ROW] += 1
                cost = 1.
                new_pos[_t] = s[_t] + 1
        elif a == 'l':
            if s[_COL] > 0:
                new_pos[_COL] -= 1
                cost = 1.
                new_pos[_t] = s[_t] + 1
        elif a == 'r':
            if s[_COL] < self.cols - 1:
                new_pos[_COL] += 1
                cost = 1.
                new_pos[_t] = s[_t] + 1
        elif a == 'ne':
            if s[_COL] < self.cols - 1 and s[_ROW] > 0:
                new_pos[_COL] += 1
                new_pos[_ROW] -= 1
                cost = 1.5
                new_pos[_t] = s[_t] + 1
        elif a == 'nw':
            if s[_ROW] > 0 and s[_COL] > 0:
                new_pos[_ROW] -= 1
                new_pos[_COL] -= 1
                cost = 1.5
                new_pos[_t] = s[_t] + 1
        elif a == 'sw':
            if s[_ROW] < self.rows - 1 and s[_COL] > 0:
                new_pos[_ROW] += 1
                new_pos[_COL] -= 1
                cost = 1.5
                new_pos[_t] = s[_t] + 1
        elif a == 'se':
            if s[_ROW] < self.rows - 1 and s[_COL] < self.cols - 1:
                new_pos[_ROW] += 1
                new_pos[_COL] += 1
                cost = 1.5
                new_pos[_t] = s[_t] + 1
        elif a == 'pause':
            new_pos[_ROW] = s[_ROW]
            new_pos[_COL] = s[_COL]
            new_pos[_t] = s[_t] + 1
            cost = 0.5
        else:
            print 'Unknown action:', str(a)

        # Test if new position is clear of obstacle
        if self.staticObstacle.has_key((new_pos[_ROW], new_pos[_COL])):
            s_prime = (s[_ROW], s[_COL], new_pos[_t])
            cost = 0.5

        # Test if new position is clear in reservation table
        elif (self.res_table.has_key((new_pos[_ROW], new_pos[_COL], new_pos[_t]))
              or self.res_table.has_key((new_pos[_ROW], new_pos[_COL], new_pos[_t] - 1))
              or self.res_table.has_key((new_pos[_ROW], new_pos[_COL], new_pos[_t] + 1))):

            s_prime = (s[_ROW], s[_COL], new_pos[_t])
            cost = 1

        # If position is free
        else:
            s_prime = (new_pos[_ROW], new_pos[_COL], new_pos[_t])   # s_prime will be the new state

        return s_prime, cost

    def transition2D(self, s, a):
        '''
        Transition function for the current grid map.

        s - tuple describing the state as (row, col) position on the grid.
        a - the action to be performed from state s

        returns - s_prime, the state transitioned to by taking action a in state s.
        If the action is not valid (e.g. moves off the grid or into an obstacle)
        returns the current state.
        '''
        new_pos = list(s[:])
        _COL = 1  # Index of s for col
        _ROW = 0  # Index of s for row
        _t = 2  # Index of s for time

        # Ensure action stays on the board
        cost = 0.
        if a == 'u':
            if s[_ROW] > 0:
                new_pos[_ROW] -= 1
                cost = 1.
        elif a == 'd':
            if s[_ROW] < self.rows - 1:
                new_pos[_ROW] += 1
                cost = 1.
        elif a == 'l':
            if s[_COL] > 0:
                new_pos[_COL] -= 1
                cost = 1.
        elif a == 'r':
            if s[_COL] < self.cols - 1:
                new_pos[_COL] += 1
                cost = 1.
        elif a == 'ne':
            if s[_COL] < self.cols - 1 and s[_ROW] > 0:
                new_pos[_COL] += 1
                new_pos[_ROW] -= 1
                cost = 1.5
        elif a == 'nw':
            if s[_ROW] > 0 and s[_COL] > 0:
                new_pos[_ROW] -= 1
                new_pos[_COL] -= 1
                cost = 1.5
        elif a == 'sw':
            if s[_ROW] < self.rows - 1 and s[_COL] > 0:
                new_pos[_ROW] += 1
                new_pos[_COL] -= 1
                cost = 1.5
        elif a == 'se':
            if s[_ROW] < self.rows - 1 and s[_COL] < self.cols - 1:
                new_pos[_ROW] += 1
                new_pos[_COL] += 1
                cost = 1.5
        else:
            print 'Unknown action:', str(a)

        # Test if new position is clear
        if self.staticObstacle.has_key((new_pos[_ROW], new_pos[_COL])):
            s_prime = tuple(s)
            cost = 0.
        else:
            s_prime = tuple(new_pos)
        return s_prime

