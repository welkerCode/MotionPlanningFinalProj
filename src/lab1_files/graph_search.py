#!/usr/bin/env python
'''
Package providing helper classes and functions for performing graph search operations for planning.
'''
import numpy as np
import heapq
import matplotlib.pyplot as plotter
from math import hypot, fabs

_DEBUG = False
_DEBUG_END = True
_ACTIONS = ['u','d','l','r']
_ACTIONS_2 = ['u','d','l','r','ne','nw','sw','se']
_X = 1
_Y = 0
_GOAL_COLOR = 0.75
_INIT_COLOR = 0.25
_PATH_COLOR_RANGE = _GOAL_COLOR-_INIT_COLOR
_VISITED_COLOR = 0.9
cost_map = {'u': 1,'d': 1,'l': 1,'r': 1,'ne': 1.5,'nw': 1.5,'sw': 1.5,'se': 1.5}

class GridMap:
    '''
    Class to hold a grid map for navigation. Reads in a map.txt file of the format
    0 - free cell, x - occupied cell, g - goal location, i - initial location.
    Additionally provides a simple transition model for grid maps and a convience function
    for displaying maps.
    '''
    def __init__(self, map_path=None, use_cost=False):
        '''
        Constructor. Makes the necessary class variables. Optionally reads in a provided map
        file given by map_path.

        map_path (optional) - a string of the path to the file on disk
        '''
        self.rows = None
        self.cols = None
        self.goals = []
        self.init_pos = None
        self.occupancy_grid = None
        self.use_costs = use_cost
        if map_path is not None:
            self.read_map(map_path)

    def read_map(self, map_path):
        '''
        Read in a specified map file of the format described in the class doc string.

        map_path - a string of the path to the file on disk
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
                if lines[r][c] == 'g':
                    self.goals.append((r,c))
                elif lines[r][c] == 'i':
                    self.init_pos = (r,c)

    def is_goal(self,s):
        '''
        Test if a specifid state is the goal state

        s - tuple describing the state as (row, col) position on the grid.

        Returns - True if s is the goal. False otherwise.
        '''
        for g in self.goals:
            if (s[_X] == g[_X] and
                s[_Y] == g[_Y]):
                return True
        return False

    def transition(self, s, a):
        '''
        Transition function for the current grid map.

        s - tuple describing the state as (row, col) position on the grid.
        a - the action to be performed from state s

        returns - s_prime, the state transitioned to by taking action a in state s.
        If the action is not valid (e.g. moves off the grid or into an obstacle)
        returns the current state.
        '''
        new_pos = list(s[:])
        # Ensure action stays on the board
        cost = 0.
        if a == 'u':
            if s[_Y] > 0:
                new_pos[_Y] -= 1
                cost = 1.
        elif a == 'd':
            if s[_Y] < self.rows - 1:
                new_pos[_Y] += 1
                cost = 1.
        elif a == 'l':
            if s[_X] > 0:
                new_pos[_X] -= 1
                cost = 1.
        elif a == 'r':
            if s[_X] < self.cols - 1:
                new_pos[_X] += 1
                cost = 1.
        elif a == 'ne':
            if s[_X] < self.cols - 1 and s[_Y] > 0:
                new_pos[_X] += 1
                new_pos[_Y] -= 1
                cost = 1.5
        elif a == 'nw':
            if s[_Y] > 0 and s[_X] > 0:
                new_pos[_Y] -= 1
                new_pos[_X] -= 1
                cost = 1.5
        elif a == 'sw':
            if s[_Y] < self.rows - 1 and s[_X] > 0:
                new_pos[_Y] += 1
                new_pos[_X] -= 1
                cost = 1.5
        elif a == 'se':
            if s[_Y] < self.rows - 1 and s[_X] < self.cols - 1:
                new_pos[_Y] += 1
                new_pos[_X] += 1
                cost = 1.5
        else:
            print 'Unknown action:', str(a)

        # Test if new position is clear
        if self.occupancy_grid[new_pos[0], new_pos[1]]:
            s_prime = tuple(s)
            cost = 0.
        else:
            s_prime = tuple(new_pos)
        if self.use_costs:
            return s_prime, cost
        else:
            return s_prime

    def display_map(self, path=[], visited={}):
        '''
        Visualize the map read in. Optionally display the resulting plan and visisted nodes

        path - a list of tuples describing the path take from init to goal
        visited - a set of tuples describing the states visited during a search
        '''
        display_grid = np.array(self.occupancy_grid, dtype=np.float32)

        # Color all visited nodes if requested
        for v in visited:
            display_grid[v] = _VISITED_COLOR
        # Color path in increasing color from init to goal
        for i, p in enumerate(path):
            disp_col = _INIT_COLOR + _PATH_COLOR_RANGE*(i+1)/len(path)
            display_grid[p] = disp_col

        display_grid[self.init_pos] = _INIT_COLOR
        for goal in self.goals:
            display_grid[goal] = _GOAL_COLOR

        # Plot display grid for visualization
        imgplot = plotter.imshow(display_grid)
        # Set interpolation to nearest to create sharp boundaries
        imgplot.set_interpolation('nearest')
        # Set color map to diverging style for contrast
        imgplot.set_cmap('spectral')
        plotter.show()

    def euclidean_heuristic(self, s):
        '''
        Euclidean heuristic function

        s - tuple describing the state as (row, col) position on the grid.

        returns - floating point estimate of the cost to the goal from state s
        '''
        h = []
        for goal in self.goals:
            h.append(hypot(s[0]-goal[0],s[1]-goal[1]))
        return min(h)

    def manhattan_heuristic(self, s):
        '''
        Euclidean heuristic function

        s - tuple describing the state as (row, col) position on the grid.

        returns - floating point estimate of the cost to the goal from state s
        '''
        h = []
        for goal in self.goals:
            h.append(fabs(s[0]-goal[0]) + fabs(s[1]-goal[1]))
        return min(h)

    def uninformed_heuristic(self, s):
        '''
        Example of how a heuristic may be provided. This one is admissable, but dumb.

        s - tuple describing the state as (row, col) position on the grid.

        returns - floating point estimate of the cost to the goal from state s
        '''
        return 0.0


class SearchNode:
    def __init__(self, s, A, parent=None, parent_action=None, cost=0, depth=0):
        '''
        s - the state defining the search node
        A - list of actions
        parent - the parent search node
        parent_action - the action taken from parent to get to s
        '''
        self.parent = parent
        self.cost = cost
        self.parent_action = parent_action
        self.state = s[:]
        self.actions = A[:]
        self.depth = depth

    def __str_full__(self):
        return str(self.state) + ' ' + str(self.actions)+' '+str(self.parent)+' '+str(self.parent_action)
    def __str__(self):
        return str(self.state) + ' ' + str(self.cost)

class PriorityQ:
    '''
    Priority queue implementation with quick access for membership testing
    Setup currently to only with the SearchNode class
    '''
    def __init__(self):
        '''
        Initialize an empty priority queue
        '''
        self.l = [] # list storing the priority q
        self.s = set() # set for fast membership testing

    def __contains__(self, x):
        '''
        Test if x is in the queue
        '''
        return x in self.s

    def push(self, x, cost):
        '''
        Adds an element to the priority queue.
        If the state already exists, we update the cost
        '''
        if x.state in self.s:
            return self.replace(x, cost)
        heapq.heappush(self.l, (cost, x))
        self.s.add(x.state)

    def pop(self):
        '''
        Get the value and remove the lowest cost element from the queue
        '''
        x = heapq.heappop(self.l)
        self.s.remove(x[1].state)
        return x[1]

    def peak(self):
        '''
        Get the value of the lowest cost element in the priority queue
        '''
        x = self.l[0]
        return x[1]

    def __len__(self):
        '''
        Return the number of elements in the queue
        '''
        return len(self.l)

    def replace(self, x, new_cost):
        '''
        Removes element x from the q and replaces it with x with the new_cost
        '''
        for y in self.l:
            if x.state == y[1].state:
                self.l.remove(y)
                self.s.remove(y[1].state)
                break
        heapq.heapify(self.l)
        self.push(x, new_cost)

    def get_cost(self, x):
        for y in self.l:
            if x.state == y[1].state:
                return y[0]

    def __str__(self):
        s = ''
        for n in self.l:
            s += '('+str(n[0])+', '+str(n[1])+')' + ', '
        s = '['+s[:-2]+']'
        return s

def backpath(node):
    '''
    Function to determine the path that lead to the specified search node

    node - the SearchNode that is the end of the path

    returns - a tuple containing (path, action_path) which are lists respectively of the states
    visited from init to goal (inclusive) and the actions taken to make those transitions.
    '''
    path = []
    action_path = []
    while node.parent is not None:
        path.append(node.state)
        action_path.append(node.parent_action)
        node = node.parent
    path.reverse()
    action_path.reverse()
    return (path, action_path)

def bfs_search_map(init_state, f, is_goal, actions):
    '''
    Perform breadth first search on a grid map.

    init_state - the intial state on the map
    f - transition function of the form s_prime = f(s,a)
    is_goal - function taking as input a state s and returning True if its a goal state
    actions - set of actions which can be taken by the agent

    returns - ((path, action_path), visited) of None if no path can be found
    path - a list of tuples. The first element is the initial state followed by all states 
    traversed until the final goal state
    action_path - the actions taken to transition from the initial state to goal state
    '''
    n0 = SearchNode(init_state, actions)
    Q = [n0]  # Search queue
    visited = set()
    visited.add(init_state)
    while len(Q) > 0:
        n_i = Q.pop(0)
        for a in n_i.actions:
            s_prime = f(n_i.state, a)
            n_prime = SearchNode(s_prime, actions, n_i, a)
            if is_goal(s_prime):
                if _DEBUG_END:
                    print 'goal found at', s_prime
                return (backpath(n_prime), visited)
            elif s_prime not in visited:
                Q.append(n_prime)
                visited.add(s_prime)
    if _DEBUG_END:
        print 'No goal found'
    return None

def uniform_cost_search(init_state, f, is_goal, actions):
    cost = 0
    n0 = SearchNode(init_state, actions, cost=cost)
    frontier = PriorityQ()
    frontier.push(n0, cost)
    visited = set()
    while len(frontier) > 0:
        n_i = frontier.pop()
        if is_goal(n_i.state):
            if _DEBUG_END:
                print 'goal found at', n_i.state
                print 'cost to goal', n_i.cost
            return backpath(n_i), visited
        visited.add(n_i.state)
        for a in n_i.actions:
            s_prime, action_cost = f(n_i.state, a)
            new_cost = n_i.cost + action_cost
            n_prime = SearchNode(s_prime, actions, n_i, a, cost = new_cost)
            if s_prime not in visited and s_prime not in frontier:
                frontier.push(n_prime, new_cost)
            elif s_prime in frontier and new_cost < frontier.get_cost(n_prime):
                frontier.push(n_prime, new_cost)
                # frontier.replace(n_prime, new_cost)
    if _DEBUG_END:
        print 'No goal found'
    return None, visited

def a_star_search(init_state, f, is_goal, actions, h):
    '''
    init_state - value of the initial state
    f - transition function takes input state (s), action (a), returns s_prime = f(s, a)
        returns s if action is not valid
    is_goal - takes state as input returns true if it is a goal state
    actions - list of actions available
    h - heuristic function, takes input s and returns estimated cost
    '''
    cost = 0
    n0 = SearchNode(init_state, actions, cost=cost)
    frontier = PriorityQ()
    frontier.push(n0, cost)
    visited = {}
    while len(frontier) > 0:
        n_i = frontier.pop()
        if n_i.state in visited:
            if visited[n_i.state] < n_i.cost:
                continue
        if is_goal(n_i.state):
            if _DEBUG_END:
                print 'goal found at', n_i.state
                print 'goal cost is', n_i.cost
            return backpath(n_i), visited
        visited[n_i.state] = n_i.cost
        if _DEBUG:
            print 'popped =', n_i.state
            print 'visited =', visited
            print 'frontier =', str(frontier)
        for a in n_i.actions:
            (s_prime, action_cost) = f(n_i.state, a)
            # Add the cost to get here to the previous nodes cost for the true cost to
            # reach the node
            cost_spent = n_i.cost + action_cost # g(s_prime)
            n_prime = SearchNode(s_prime, actions, n_i, a, cost = cost_spent)
            # Add the heuristic for the combined cost-spent and cost-to-go
            new_cost = cost_spent + h(s_prime) # f(s_prime)
            if ((s_prime in visited and visited[s_prime] > cost_spent) or
                (s_prime not in visited and s_prime not in frontier)):
                frontier.push(n_prime, new_cost)
            elif s_prime in frontier and new_cost < frontier.get_cost(n_prime):
                frontier.replace(n_prime, new_cost)
    if _DEBUG_END:
        print 'No goal found'
    return None

def best_first_search(init_state, f, is_goal, actions, h):
    '''
    init_state - value of the initial state
    f - transition function takes input state (s), action (a), returns s_prime = f(s, a)
        returns s if action is not valid
    is_goal - takes state as input returns true if it is a goal state
    actions - list of actions available
    h - heuristic function, takes input s and returns estimated cost
    '''
    cost = 0
    n0 = SearchNode(init_state, actions, cost=cost)
    frontier = PriorityQ()
    frontier.push(n0, cost)
    visited = set()
    while len(frontier) > 0:
        n_i = frontier.pop()
        if is_goal(n_i.state):
            if _DEBUG_END:
                print 'goal found at', n_i.state
            return backpath(n_i), visited
        visited.add(n_i.state)
        for a in n_i.actions:
            s_prime, action_cost = f(n_i.state, a)
            new_cost = h(s_prime)
            n_prime = SearchNode(s_prime, actions, n_i, a, cost = new_cost)
            if s_prime not in visited and s_prime not in frontier:
                frontier.push(n_prime, new_cost)
            elif s_prime in frontier and new_cost < frontier.get_cost(n_prime):
                frontier.replace(n_prime, new_cost)
    if _DEBUG_END:
        print 'No goal found'
    return None

def dfs_search_map(init_state, f, is_goal, actions):
    '''
    Function to implement depth first search
    '''
    K = [] # Search stack
    n0 = SearchNode(init_state, actions)
    visited = set()
    K.append(n0)
    while len(K) > 0:
        n_i = K.pop()
        if n_i.state not in visited:
            visited.add(n_i.state)
            if is_goal(n_i.state):
                if _DEBUG_END:
                    print 'goal found at', n_i.state
                return (backpath(n_i), visited)
            for a in actions:
                s_prime = f(n_i.state, a)
                n_prime = SearchNode(s_prime, actions, n_i, a, depth=n_i.depth+1)
                K.append(n_prime)
    if _DEBUG_END:
        print 'No goal found'
    return None

def dfs_depth_limited(init_state, f, is_goal, actions, max_depth = None):
    '''
    A second implementation of depth first search, where we have a state-action stack,
    instead of a state stack, this allows us to branch less. Also limits the search depth
    for use with IDDFS
    '''
    K = [] # Search stack
    n0 = SearchNode(init_state, actions)
    visited = {}
    visited[init_state] = 0
    K.append(n0)
    while len(K) > 0:
        # Peak last element
        n_i = K[-1]
        a = n_i.actions.pop(0)
        # Only pop if 0 actions left
        if len(n_i.actions) == 0:
            K.pop()
        s_prime = f(n_i.state, a)
        n_prime = SearchNode(s_prime, actions, n_i, a, depth=n_i.depth+1)
        if is_goal(s_prime):
            if _DEBUG_END:
                print 'goal found at', s_prime
                # print 'visited',len(visited), visited
            return (backpath(n_prime), visited)
        elif s_prime not in visited and (max_depth is None or n_prime.depth < max_depth):
            K.append(n_prime)
            visited[s_prime] = n_prime.depth
        elif n_prime.depth <= max_depth:
            if s_prime in visited:
                if visited[s_prime] > n_prime.depth:
                    K.append(n_prime)
                    visited[s_prime] = n_prime.depth
            else:
                K.append(n_prime)
                visited[s_prime] = n_prime.depth
    return None

def iterative_deepening(init_state, f, is_goal, actions, max_depth = 10000):
    for i in range(1, max_depth):
        result = dfs_depth_limited(init_state[:], f, is_goal, actions[:], i)
        if result is not None:
            if _DEBUG_END:
                print 'Found result at depth', i
            return result
    if _DEBUG_END:
        print 'No goal found'
    return None

def true_cost(plan):
    cost = 0
    for a in plan:
        cost += cost_map[a]
    return cost
