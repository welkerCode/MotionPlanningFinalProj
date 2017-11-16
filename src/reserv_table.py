class Reserv_Table:
    '''
    The reservation table is a dictionary of dictionaries.  The outer dictionary uses x values as the key to accessing
    y values and their occupation status over time.  The inner dictionary uses the y values as the key, and they yield
    another dictionary.  This dictionary uses the timestep as the key, and the occupation status of that position at the
    desired timestep is returned
    '''

    res_table = {}

    def __init__(self, occupancyGrid = []):

        self.res_table = {}

        staticObstacle = []

        '''
        self.res_table = {}                     # Create the outer dictionary
        for i in range(0, env_x, 1):            # For all of the x's in the environment
            d = {}                              # Create a second dictionary for each y
            for j in range(0, env_y, 1):        # For all of the y's in the environment
                d[j] = {0 : occupancyGrid[2]}   # Fill the second dictionary with the third dictionary (1 = obstacle)
            self.res_table[i] = d               # Tie three dictionaries together
        '''


    # Simply prints the table.  Might be good to format for easy debugging?
    def showTable(self):
        print(self.res_table)

    # This is Paul's updated 3D transition function
    def transition3D(self, s, a):
        '''
        Transition function for the current grid map.

        s - tuple describing the state as (row, col, t) position in the reservation table.
        a - the action to be performed from state s

        returns - s_prime (row', col', t+1), the state transitioned to by taking action a in state s.
        If the action is not valid (e.g. moves off the grid or into an obstacle)
        returns the current state with t+1.
        '''
        new_pos = list(s[:])
        _X = 1  # Index of s for col
        _Y = 0  # Index of s for row
        _t = 2  # Index of s for time

        # Ensure action stays on the board
        cost = 0.
        if a == 'u':
            if s[_Y] > 0:
                new_pos[_Y] -= 1
                cost = 1.
                new_pos[_t] = s[_t] + 1
        elif a == 'd':
            if s[_Y] < self.rows - 1:
                new_pos[_Y] += 1
                cost = 1.
                new_pos[_t] = s[_t] + 1
        elif a == 'l':
            if s[_X] > 0:
                new_pos[_X] -= 1
                cost = 1.
                new_pos[_t] = s[_t] + 1
        elif a == 'r':
            if s[_X] < self.cols - 1:
                new_pos[_X] += 1
                cost = 1.
                new_pos[_t] = s[_t] + 1
        elif a == 'ne':
            if s[_X] < self.cols - 1 and s[_Y] > 0:
                new_pos[_X] += 1
                new_pos[_Y] -= 1
                cost = 1.5
                new_pos[_t] = s[_t] + 1
        elif a == 'nw':
            if s[_Y] > 0 and s[_X] > 0:
                new_pos[_Y] -= 1
                new_pos[_X] -= 1
                cost = 1.5
                new_pos[_t] = s[_t] + 1
        elif a == 'sw':
            if s[_Y] < self.rows - 1 and s[_X] > 0:
                new_pos[_Y] += 1
                new_pos[_X] -= 1
                cost = 1.5
                new_pos[_t] = s[_t] + 1
        elif a == 'se':
            if s[_Y] < self.rows - 1 and s[_X] < self.cols - 1:
                new_pos[_Y] += 1
                new_pos[_X] += 1
                cost = 1.5
                new_pos[_t] = s[_t] + 1
        elif a == 'pause':
            new_pos[_Y] = s[_Y]
            new_pos[_X] = s[_X]
            new_pos[_t] = s[_t] + 1
        else:
            print 'Unknown action:', str(a)

        # Test if new position is clear of obstacle
        if self.occupancy_grid[new_pos[_Y]][new_pos[_X]]:
            s_prime = (s[_Y], s[_X], new_pos[_t])
            cost = 0.

        # Test if new position is clear in reservation table
        elif self.RES_TABLE[new_pos[_Y]][new_pos[_X]][new_pos[_t]]:  # Fix RES_TABLE reference
            s_prime = (s[_Y], s[_X], new_pos[_t])
            cost = 0.

        # If position is free
        else:
            s_prime = (new_pos[_Y], new_pos[_X], new_pos[_t])

        # Return s_prime
        if self.use_costs:
            return s_prime, cost
        else:
            return s_prime

    # This is the original transition function from the gridmap class
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

    def checkStateResv(self, state, time):
        if self.res_table.has_key([state[0], state[1], time]):
            return True
        else:
            return False
    # A function to reservePaths in table
    def resvPath(self, pathList, init_timestep):
        currentTimestep = init_timestep
        for time, state in enumerate(pathList):
            res_table[(state[0], state[1], time+currentTimestep)] = True
            res_table[(state[0], state[1], time+currentTimestep+1)] = True

'''
List of static obstacle locations
occupancy grid during initialization makes the list above
every new timestep requires going through the obstacle location list and adding reservations very first thing.
if a reservation is made, it will exist in the dictionary.  To check if a state has been reserved, simply search the dictionary using the state as a key.  If it exists already, then the state has been reserved, otherwise it must be open, and can be reserved
Transition function may be an element of this class.  The transition function checks the reservation table to make sure no collisions occur using the method above

'''