from transition import transition
from node import SearchNode

_ACTIONS = ['u','d','l','r']
_ACTIONS_2 = ['u','d','l','r','ne','nw','sw','se']
_X = 1
_Y = 0


def whca_search(map, currentState, task, revVisited, revFrontier, trueHeur):
    '''
    map             - environment map.  Needed to obtain the manhattan heuristic?
    currentState    - the state the agent is currently at
    task            - the task assigned to the agent, yields dropoff location (goal) as well as some other info
    revVisited      - the list that holds the states the reverse search has already searched
    revFrontier     - the PriorityQ that holds the frontier for the reverse search
    trueHeur        - a dictionary stored in the agent that holds the true heuristic for any node that it has searched for
    '''

    '''
    init_state, f, is_goal, actions, h,
    '''

    # These are set for every search we run
    f = transition
    actions = _ACTIONS

    # Obtain the goal we are working towards
    dropoffState = task.getDropoff()

    pickupState = task.getPickup()     # Add in when we are not starting at the pickup location
    taskStatus = task.getTaskStatus()  # Add in when we are not starting at the pickup location

    # Initialize the first state in the search
    cost = 0
    n0 = SearchNode(currentState, actions, cost=cost)
    frontier = PriorityQ()
    frontier.push(n0, cost)
    visited = {}

    # Until we run out of places to search
    while len(frontier) > 0:
        n_i = frontier.pop()
        if n_i.state in visited:
            if visited[n_i.state] < n_i.cost:
                continue
        if n_i[_X] == dropoffState[_X] and n_i[_Y] == dropoffState[_Y]:
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
            cost_spent = n_i.cost + action_cost # g(s_prime)
            n_prime = SearchNode(s_prime, actions, n_i, a, cost = cost_spent)

            if(trueHeur.has_key(s_prime)):
                h = trueHeur.get(s_prime)
            else:
                whca_reverse(f, dropoffState, actions, map.manhattan_heuristic, revFrontier, revVisited, trueHeur)
                h = trueHeur.get(s_prime)

            # Add the heuristic for the combined cost-spent and cost-to-go
            new_cost = cost_spent + h # f(s_prime)
            if ((s_prime in visited and visited[s_prime] > cost_spent) or
                (s_prime not in visited and s_prime not in frontier)):
                frontier.push(n_prime, new_cost)
            elif s_prime in frontier and new_cost < frontier.get_cost(n_prime):
                frontier.replace(n_prime, new_cost)
    if _DEBUG_END:
        print 'No goal found'
    return None



def whca_reverse(f, desiredLocation, actions, h, frontier, visited, trueHeurDict):
    '''
    init_state - value of the initial state
    f - transition function takes input state (s), action (a), returns s_prime = f(s, a)
        returns s if action is not valid, designed by Paul and found in transition.py
    is_goal - takes state as input returns true if it is a goal state.  In this case, the goal state is if we find the node we want the heuristic for
    actions - list of actions available
    h - heuristic function, takes input s and returns estimated cost, must be manhattan heuristic in this case
    '''
    '''
    None of the following are necessary because the frontier and visited variables will be set up prior to this search
    The frontier should be given the goal with a cost of 0 as init_state and stored in frontier.  The visited List
    should just be initialized
    
    cost = 0
    n0 = SearchNode(init_state, actions, cost=cost)
    frontier = PriorityQ()
    frontier.push(n0, cost)
    visited = {}
    '''

    # Until we reach the end of the frontier, or until we reach the depth/cost we want to stop at
    while len(frontier) > 0 and desiredDepth > frontier.peak.cost:
        n_i = frontier.pop()

        # Check to see if we have already visited this location
        if n_i.state in visited:
            if visited[n_i.state] < n_i.cost:
                continue

        # Add to the revVisited list and trueHeurDict
        visited[n_i.state] = n_i.cost
        trueHeurDict[n_i.state] = n_i.cost


        # Add to the revFrontier before checking the goal.  This will allow us to resume from our current location if we choose to return
        for a in n_i.actions:
            (s_prime, action_cost) = f(n_i.state, a)
            # Add the cost to get here to the previous nodes cost for the true cost to
            # reach the node
            cost_spent = n_i.cost + action_cost # g(s_prime)
            n_prime = SearchNode(s_prime, actions, n_i, a, cost = cost_spent)
            # Add the heuristic (manhattan) for the combined cost-spent and cost-to-go
            new_cost = cost_spent + h(s_prime) # f(s_prime)
            if ((s_prime in visited and visited[s_prime] > cost_spent) or
                (s_prime not in visited and s_prime not in frontier)):
                frontier.push(n_prime, new_cost)
            elif s_prime in frontier and new_cost < frontier.get_cost(n_prime):
                frontier.replace(n_prime, new_cost)

        # Check for the goal
        if n_i[_X] == desiredLocation[_X] and n_i[_Y] == desiredLocation[_Y]:
            if _DEBUG_END:
                print 'true_heuristic found at', n_i.state
                print 'true_heuristic is', n_i.cost
            return n_i.cost # Return the cost.  The visited list and frontier has already been updated, and we don't need the path

        if _DEBUG:
            print 'popped =', n_i.state
            print 'visited =', visited
            print 'frontier =', str(frontier)

    if _DEBUG_END:
        print 'No goal found'
    return None