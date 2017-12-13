#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: global_utility.py
Authors: Taylor Welker, Cade Parkison, Paul Wadsworth
Emails: <taylormaxwelker@gmail.com>,  <cadeparkison@gmail.com>, <wadspau2@gmail.com>
Githubs: welkerCode, c-park
Description: Utility functions to be used in other modules
"""

import numpy as np

_ACTIONS = ['u', 'd', 'l', 'r']

def assignTasks(tasks, agents):
    """
    Given agent list and task list, assigns tasks to agents based on distance
    to task
    """
    for task in tasks:
        shortestDistance = 100000000
        agentToAssign = None
        for agent in agents:
            if agent.isAgentIdle() and task.trueHeurDrop[agent.currentState] < shortestDistance:
                agentToAssign = agent
        if (agentToAssign is not None):
            agentToAssign.assignTask(task)
         #   tasks.remove(task)

def incrementTimestep(agents, reserv_table):
    '''
     increment timestep
        update all agent movements
            timer updated within agent's task
        unassign tasks if goal is reached and add to report

    :return:
    '''
    for agent in agents:
        agent.updateCurrentState(reserv_table)

def incrementTimestepWHCA(busy_agents, idle_agents, reserv_table):
    '''
     increment timestep
        update all agent movements
            timer updated within agent's task
        unassign tasks if goal is reached and add to report

    :return:
    '''
    for agent in idle_agents:
        agent.updateCurrentState(reserv_table)

    for agent in busy_agents:
        agent.updateCurrentState(reserv_table)
        if agent.isAgentIdle():
            busy_agents.remove(agent)
            idle_agents.append(agent)


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
    return path


def bfs_search_map(init_state, f, actions):
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

    from node import SearchNode

    cost = 0
    n0 = SearchNode(init_state, actions, cost=cost)
    Q = [n0]  # Search queue
    visited = set()
    visited.add(init_state)
    trueHeurDict = {}
    trueHeurDict[init_state] = cost
    while len(Q) > 0:
        n_i = Q.pop(0)
        for a in n_i.actions:
            s_prime = f(n_i.state, a)
            new_cost = n_i.cost + 1
            n_prime = SearchNode(s_prime, actions, n_i, a, new_cost)
            if s_prime not in visited:
                Q.append(n_prime)
                visited.add(s_prime)
                trueHeurDict[s_prime] = new_cost
    return trueHeurDict

def bfs_endpoints(init_state, f, actions, endpoints, tasks, agents):
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

    from node import SearchNode

    cost = 0
    n0 = SearchNode(init_state, actions, cost=cost)
    Q = [n0]  # Search queue
    visited = set()
    visited.add(init_state)
    while len(Q) > 0:
        n_i = Q.pop(0)
        if n_i.state in endpoints:
            # Check to see if endpoint is available
            available = True
            for task in tasks:
                if task.getDropoff() == n_i.state:
                    available = False
            for agent in agents:
                if agent.plan is not None:
                    new_plan = [state[:2] for state in agent.plan]
                    if n_i.state in new_plan:
                        available = False
            if available:
                return n_i.state

        for a in n_i.actions:
            s_prime = f(n_i.state, a)
            new_cost = n_i.cost + 1
            n_prime = SearchNode(s_prime, actions, n_i, a, new_cost)
            if s_prime not in visited:
                Q.append(n_prime)
                visited.add(s_prime)
    return None

def a_star_search(init_state, f, is_goal, actions, h):
    '''
    init_state - value of the initial state
    f - transition function takes input state (s), action (a), returns s_prime = f(s, a)
        returns s if action is not valid
    is_goal - takes state as input returns true if it is a goal state
    actions - list of actions available
    h - heuristic function, takes input s and returns estimated cost
    '''

    from node import SearchNode

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
            cost_spent = n_i.cost + action_cost  # g(s_prime)
            n_prime = SearchNode(s_prime, actions, n_i, a, cost=cost_spent)
            # Add the heuristic for the combined cost-spent and cost-to-go
            new_cost = cost_spent + h(s_prime)  # f(s_prime)
            if ((s_prime in visited and visited[s_prime] > cost_spent) or
                    (s_prime not in visited and s_prime not in frontier)):
                frontier.push(n_prime, new_cost)
            elif s_prime in frontier and new_cost < frontier.get_cost(n_prime):
                frontier.replace(n_prime, new_cost)
    if _DEBUG_END:
        print 'No goal found'
    return None



def manhattan_heuristic(s, desiredNode):

    """
    Euclidean heuristic function

    s - tuple describing the state as (row, col) position on the grid.
    desiredNode -
    returns - floating point estimate of the cost to the goal from state s
    """

    h = (abs(s[0] - desiredNode[0]) + abs(s[1] - desiredNode[1]))
    return h
