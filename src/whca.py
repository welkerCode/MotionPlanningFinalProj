#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: whca.py
Authors: Taylor Welker, Cade Parkison, Paul Wadsworth
Emails: <taylormaxwelker@gmail.com>,  <cadeparkison@gmail.com>, <wadspau2@gmail.com>
Githubs: welkerCode, c-park
Description:
"""


from node import SearchNode
from priorityq import PriorityQ
from global_utility import backpath
from global_utility import manhattan_heuristic

_ACTIONS = ['u','d','l','r','pause']
_ACTIONS_2 = ['u','d','l','r','ne','nw','sw','se','pause']
# _ACTION_1_COST =  {'u':1,'d':1,'l':1,'r':1,'pause':0.5}
# _ACTION_2_COST = {'u':1,'d':1,'l':1,'r':1,'ne':1.5,'nw':1.5,'sw':1.5,'se':1.5,'pause':0.5}

_COL = 1
_ROW = 0
_DEBUG = False
_DEBUG_END = False


def whca_search(currentState, task, trueHeur, reserv_table, currentTime, heuristic):
    '''
    map             - environment map.  Needed to obtain the manhattan heuristic?
    currentState    - the state the agent is currently at
    task            - the task assigned to the agent, yields dropoff location (goal) as well as some other info
    revVisited      - the list that holds the states the reverse search has already searched
    revFrontier     - the PriorityQ that holds the frontier for the reverse search
    trueHeur        - a dictionary stored in the agent that holds the true heuristic for any node that it has searched for
    heuristic       - either use trueHeur or manhattan_heuristic
    '''

    '''
    init_state, f, is_goal, actions, h,
    '''

    # These are set for every search we run
    f = reserv_table.transition3D
    actions = _ACTIONS
    # action_cost = _ACTION_1_COST

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
        if n_i.state[_ROW] == dropoffState[_ROW] and n_i.state[_COL] == dropoffState[_COL]:
            if _DEBUG_END:
                print 'goal found at', n_i.state
                print 'goal cost is', n_i.cost
            path = backpath(n_i)
            reserv_table.resvPath(path, currentTime)
            if _DEBUG:
                print(path)
            return path, n_i.cost
        visited[n_i.state] = n_i.cost
        if _DEBUG:
            print('popped = {}'.format(n_i.state))
            print('visited = {}'.format(visited))
        for a in n_i.actions:
            s_prime, cost = f(n_i.state, a)
            if not reserv_table.checkStateResv(s_prime[:2], s_prime[2]):
                cost_spent = n_i.cost + cost # g(s_prime)
                n_prime = SearchNode(s_prime, actions, n_i, a, cost = cost_spent)
                if heuristic == 'whca':
                    h = trueHeur.get(s_prime[:2])
                elif heuristic == 'manhattan':
                    h = manhattan_heuristic(s_prime[:2], dropoffState)
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
    is_goal - takes state as input returns true if it is a goal state.
              In this case, the goal state is if we find the node we want the
              heuristic for
    actions - list of actions available
    h - heuristic function, takes input s and returns estimated cost,
        must be manhattan heuristic in this case
    '''
    '''
    None of the following are necessary because the frontier and visited
    variables will be set up prior to this search
    The frontier should be given the goal with a cost of 0 as init_state and
    stored in frontier.  The visited List should just be initialized

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


        # Add to the revFrontier before checking the goal.  This will allow us
        # to resume from our current location if we choose to return
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
        if n_i[_COL] == desiredLocation[_COL] and n_i[_ROW] == desiredLocation[_ROW]:
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

