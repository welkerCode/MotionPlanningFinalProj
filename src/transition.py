def transition(self, s, a):
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