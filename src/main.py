#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: global_utility.py
Authors: Taylor Welker, Cade Parkison, Paul Wadsworth
Emails: <taylormaxwelker@gmail.com>,  <cadeparkison@gmail.com>, <wadspau2@gmail.com>
Githubs: welkerCode, c-park
Description: This is the program that needs to be run to execute our simulation

    Can choose between various planning algorithms:
        lra: Local Repair A*
        hca: Hierarchical Cooperative A*
        whca: Windowed Hierarchical Cooperative A*
"""

from reserv_table import *
from env import GridMap
from global_utility import assignTasks
from global_utility import incrementTimestep
from global_utility import bfs_endpoints
from global_utility import _ACTIONS
from agent import Agent
from task import Task

import random
import sys
import copy

_DEBUG = False

def init_agents_tasks(env, reserv_table, n_agents, agent_list, task_list, heuristic):
    """TODO: Initialieses a list of agent and tasks and assigns tasks to agents
             If agent_list and task_list are None, generate n random agents and tasks

    :env: TODO
    :reserv_table: TODO
    :n_agents: TODO
    :agent_list: TODO
    :task_list: TODO
    :returns: TODO

    """
    agents = []
    tasks = []

    if agent_list == None and task_list == None:
        # generates n_agents*2 samples from the list of endpoints
        samples = random.sample(env.endpoints,n_agents*2)
        for i in range(n_agents):
            # generate random agent/task pair
            agent = Agent(i, samples.pop())
            task = Task(i, agent.currentState, samples.pop(),
                        "dropoff", reserv_table, heuristic)
            agent.assignTask(task)
            agents.append(agent)
            tasks.append(task)

    else:
        for i in range(n_agents):
            agent = Agent(i, env.endpoints[agent_list[i]])
            task = Task(i, agent.currentState, env.endpoints[task_list[i]],
                        "dropoff", reserv_table, heuristic)
            agent.assignTask(task)
            agents.append(agent)
            tasks.append(task)

    return agents, tasks

'''
Task needs to be equipped with a initPrioirity

Bidding war algorithm

Create a list to hold tasks that haven't been assigned
Create a list to hold tasks that have been assigned

Until the unassigned task list is empty
    Create a list to hold agents that have been sorted
    Iterate through the list of agents
        Sort the agents into a new list in order of initPrioirty to the task
            Calculate the initDist
    Until the list of sorted agents are empty and we don't have a valid agent
        If the agent is claimed
            Identify the task that claimed it (a function that iterates through the list of all assigned agents and returns the one)                
            If the current task has a greater priority
                Assign agent to this task instead
                Remove priority of prev Task
                Place prev task in the list of unassigned tasks
                Place the current task in the list of assigned tasks
        Else
            Place the task in the list of assigned tasks
            Set valid agent to true
        remove the task from the sorted list (pop off the top).
'''


def init_agents_tasks_with_regret(env, reserv_table, n_agents, agent_list, task_list, heuristic):
    """TODO: Initialieses a list of agent and tasks and assigns tasks to agents
             If agent_list and task_list are None, generate n random agents and tasks

    :env: TODO
    :reserv_table: TODO
    :n_agents: TODO
    :agent_list: TODO
    :task_list: TODO
    :returns: TODO

    """

    if agent_list == None and task_list == None:
        agent_list = []
        task_list = []

        # generates n_agents*2 samples from the list of endpoints
        samples = random.sample(env.endpoints, n_agents * 2)
        for i in range(n_agents):
            # generate random agent/task pair
            agent = Agent(i, samples.pop())
            task = Task(i, agent.currentState, samples.pop(),
                        "dropoff", reserv_table, heuristic)
            agent_list.append(agent)
            task_list.append(task)

    else:
        for i in range(n_agents):
            agent = Agent(i, env.endpoints[agent_list[i]])
            task = Task(i, agent.currentState, env.endpoints[task_list[i]],
                        "dropoff", reserv_table, heuristic)
            agent_list.append(agent)
            task_list.append(task)

    assignedAgents = []
    assignedTasks = []
    unassignedTasks = copy.deepcopy(task_list)
    while len(unassignedTasks) > 0:
        task = unassignedTasks[0]
        sortedAgents = []
        for agent in agent_list:
            initDist = task.trueHeurDrop[agent.currentState[:2]] # Calculate the initial distance between the task and the agent
            #addToSortedList(agent, initDist)    # Add it to the list in sorted order
            sortedAgents.append((initDist, agent))
        # After all agents are in, sort the list
        sortedAgents.sort()

        validAgent = False
        while len(sortedAgents) != 0 and validAgent == False:
            currentAgent = sortedAgents[0][1]
            if currentAgent in assignedAgents:
                competingTask = currentAgent.task
                if task.trueHeurDrop[currentAgent.currentState[:2]] < competingTask.trueHeurDrop[currentAgent.currentState[:2]]:
                    currentAgent.assignTask(task)
                    assignedTasks.remove(competingTask)
                    assignedTasks.append(task)
                    unassignedTasks.append(competingTask)
                    validAgent = True
                else:
                    sortedAgents.pop(0)
            else:
                currentAgent.assignTask(task)
                assignedAgents.append(currentAgent)
                assignedTasks.append(task)
                validAgent = True
        unassignedTasks.pop(0)
    return assignedAgents, assignedTasks

'''
    Until the list of sorted agents are empty and we don't have a valid agent
        If the agent is claimed
            Identify the task that claimed it (a function that iterates through the list of all assigned agents and returns the one)                
            If the current task has a greater priority
                Assign agent to this task instead
                Remove priority of prev Task
                Place prev task in the list of unassigned tasks
                Place the current task in the list of assigned tasks
        Else
            Place the task in the list of assigned tasks
            Set valid agent to true
        remove the task from the sorted list (pop off the top).
'''

def run_lra(agents, tasks, reserv_table, heuristic):
    """TODO: Docstring for plan_lra.

    :arg1: TODO
    :returns: TODO

    """
    pass

def run_hca(agents, tasks,env, reserv_table, heuristic):
    """TODO: Docstring for plan_hca.

    :agents: TODO
    :reserv_table: TODO
    :returns: TODO

    """
    TaskIDGen = 0
    global_timestep = 0
    artif_task_count = 0
    agentsDone = False

    ### ACTION ###
    while not agentsDone:
        for agent in agents:
            if agent.getPlan() is None:
                if not agent.isAgentIdle():
                    if _DEBUG:
                        print("\nPlanning agent {}...".format(agent._id))
                    agent.planPath(reserv_table, global_timestep, heuristic)
                    # reserve n=10 paths to stay put at goal position
                    # for i in range(10):
                    #     next_state = agent.plan[-1][:2] + (agent.plan[-1][2] + i,)
                    #     reserv_table.resvState(next_state)

                    if _DEBUG:
                        print("\nAgent {} Plan: {}".format(agent._id, agent.plan))
                        print("\nAgent {} Plan Cost: {}".format(agent._id, agent.planCost))
                else:
                     #plan mini path to stay put
                     #Add path to res_table
                    next_state = agent.currentState[:2] + (agent.currentState[2] + 1,)
                    agent.plan = [next_state]
                    reserv_table.resvState(next_state)

            else:

                if agent.isAgentIdle():

                    next_state = reserv_table.checkStateResv(agent.currentState[:2], agent.currentState[2] + 1)
                    second_state = reserv_table.checkStateResv(agent.currentState[:2], agent.currentState[2] + 2)
                    third_state = reserv_table.checkStateResv(agent.currentState[:2], agent.currentState[2] + 3)
                    if next_state == True or second_state == True or third_state == True:

                        # create task with different ID
                        # plan from currentState to task

                        # endpoint_index = env.endpoints.index(agent.currentState[:2])
                        # print(endpoint_index)

                        # right = env.endpoints[endpoint_index + 1]
                        # left = env.endpoints[endpoint_index - 1]

                        dest_end = bfs_endpoints(agent.currentState[:2], reserv_table.transition2D, _ACTIONS,
                                                 env.endpoints, tasks, agents)
                        relocateTask = Task('a{}'.format(artif_task_count), None, dest_end, "dropoff", reserv_table)
                        agent.assignTask(relocateTask)
                        agent.planPath(reserv_table, global_timestep, heuristic)
                        artif_task_count += 1
                        # find good endpoint

        incrementTimestep(agents, reserv_table)
        global_timestep += 1
        agentDoneCount = 0
        for agent in agents:
            if agent.isAgentIdle():
                agentDoneCount += 1
        if agentDoneCount == len(agents):
            agentsDone = True



def run_whca(agents, tasks, reserv_table, heuristic):
    """TODO: Docstring for plan_whca.

    :arg1: TODO
    :returns: TODO

    """
    pass

def main(env,alg, heuristic, n_agents, agent_list=None, task_list=None, animate=True):
    """TODO: Docstring for main.

    :env: path to environment file
    :alg: Type of planning algorithm to run
            - 'lra': Local Repair A*
            - 'hca': Hierarchical Cooperative A*
            - 'whca': Windowed Hierarchical Cooperative A*

    :heuristic: Type of heuristic to use for A*
            - 'manhattan': manhattan distance
            - 'true': True distane, found from BFS search

    :n_agents: number of agent/task pairs to generate randomly
    :agent_list: if not random tasks, list of agent endpoint indexes
    :task_list: if not random tasks, list of task endpoint indexes

    :Returns: Agent paths, task dropoff endpoints

    """

    if alg == 'lra':
        run_planner = run_lra
    elif alg == 'hca':
        run_planner = run_hca
    elif alg == 'whca':
        run_planner = run_whca

    env = GridMap('env_files/{}'.format(env))
    reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)

    #agents, tasks = init_agents_tasks_with_regret(env, reserv_table, n_agents,
    #                                  agent_list, task_list, heuristic)
    agents, tasks = init_agents_tasks(env, reserv_table,n_agents,
                                      agent_list,task_list,heuristic)
    if _DEBUG:
        print("\nAgent Starts and Goals")
        print("------------------------\n")

        for i, agent in enumerate(agents):
            print("Agent {}:".format(i))
            print("\t Start: {}".format(agent.currentState))
            print("\t Goal:   {}".format(agent.task.dropoffState))

    reserv_table.resvAgentInit(agents)

    ### ACTION ###
    run_planner(agents, tasks, env, reserv_table, heuristic)

    if _DEBUG:
        reserv_table.display(env)
        print("Creating Animation...")

    ### ANIMATE RESULTS ###
    agent_paths = [agent.getPath() for agent in agents]
    agent_plans = [agent.getPlan() for agent in agents]
    path_costs = [agent.planCost for agent in agents]
    if animate:
        env.display_map(agent_paths, record=False)

    return agent_paths, agent_plans, path_costs

if __name__ == "__main__":
    env = sys.argv[1]
    heur = sys.argv[2]
    n_agents = int(sys.argv[3])
    main(env,'hca', heur, n_agents)

    # Failed test 1
    # test_agent_ep = [-2, -3]
    # test_task_ep = [2, -4]

    # main('env_trial.txt', 2, agent_list=test_agent_ep, task_list=test_task_ep)


    # Failed Test 2
    # test_agent_ep = [-3,-2]
    # test_task_ep = [-4,2]

    # main('env_trial.txt', 2, agent_list=test_agent_ep, task_list=test_task_ep)

    ######################
    # Env_trial2 Testing
    ######################

    # Passed
    # test_agent_ep = [-3,3]
    # test_task_ep = [2,-4]


    # Failed
    # test_agent_ep = [-1,3,5]
    # test_task_ep = [4,6,2]

    ######################
    # Env_warehouse2 Testing
    ######################

    # test_agent_ep = [-1,-26,23, 49]
    # test_task_ep = [71, 50,12, -27]

    ######################
    # Env_warehouse2 Testing
    ######################

    #test_agent_ep = [-5, -4]
    #test_task_ep = [-1, -3]

    ########################

    # main('env_small_warehouse.txt','hca', sys.argv[1], len(test_agent_ep), agent_list=test_agent_ep, task_list=test_task_ep)

