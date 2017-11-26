#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: global_utility.py
Authors: Taylor Welker, Cade Parkison, Paul Wadsworth
Emails: <taylormaxwelker@gmail.com>,  <cadeparkison@gmail.com>, <wadspau2@gmail.com>
Githubs: welkerCode, c-park
Description: This is the program that needs to be run to execute our simulation
"""

from reserv_table import *
from env import GridMap
from global_utility import assignTasks
from global_utility import incrementTimestep
from agent import Agent
from task import Task

import random
import sys

_DEBUG = False

def init_agents_tasks(env, reserv_table, n_agents, agent_list, task_list):
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
                        "dropoff", reserv_table)
            agent.assignTask(task)
            agents.append(agent)
            tasks.append(task)

    else:
        for i in range(n_agents):
            agent = Agent(i, env.endpoints[agent_list[i]])
            task = Task(i, agent.currentState, env.endpoints[task_list[i]],
                        "dropoff", reserv_table)
            agent.assignTask(task)
            agents.append(agent)
            tasks.append(task)

    return agents, tasks

def main(env, n_agents, agent_list=None, task_list=None):
    """TODO: Docstring for main.

    :env: path to environment file
    :n_agents: number of agent/task pairs to generate randomly
    :agent_list: if not random tasks, list of agent endpoint indexes
    :task_list: if not random tasks, list of task endpoint indexes
    :returns: TODO

    """

    env = GridMap('env_files/{}'.format(env))
    reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)
    global_timestep = 0
    TaskIDGen = 0

    agents, tasks = init_agents_tasks(env, reserv_table, n_agents,
                                      agent_list, task_list)

    if _DEBUG:
        print("\nAgent Starts and Goals")
        print("------------------------\n")

        for i, agent in enumerate(agents):
            print("Agent {}:".format(i))
            print("\t Start: {}".format(agent.currentState))
            print("\t Goal:   {}".format(agent.task.dropoffState))

    agentsDone = False
    reserv_table.resvAgentInit(agents)

    ### ACTION ###
    while not agentsDone:
        for agent in agents:
            if agent.getPlan() is None:
                if not agent.isAgentIdle():
                    if _DEBUG:
                        print("\nPlanning agent {}...".format(agent._id))
                    agent.planPath(reserv_table, global_timestep)
                    # reserve n=10 paths to stay put at goal position
                    for i in range(10):
                        next_state = agent.plan[-1][:2] + (agent.plan[-1][2] + i,)
                        reserv_table.resvState(next_state)

                    if _DEBUG:
                        print("\nAgent {} Plan: {}".format(agent._id, agent.plan))
                        print("\nAgent {} Plan Cost: {}".format(agent._id, agent.planCost))
                else:
                    # plan mini path to stay put
                    # Add path to res_table
                    next_state = agent.currentState[:2] + (agent.currentState[2] + 1,)
                    agent.plan = [next_state]
                    reserv_table.resvState(next_state)

        incrementTimestep(agents, reserv_table)
        global_timestep += 1
        agentDoneCount = 0
        for agent in agents:
            if agent.isAgentIdle():
                agentDoneCount += 1
        if agentDoneCount == len(agents):
            agentsDone = True

    if _DEBUG:
        reserv_table.display(env)
        print("Creating Animation...")

    ### ANIMATE RESULTS ###
    agentPaths = [agent.getPath() for agent in agents]
    env.display_map(agentPaths, record=False)

if __name__ == "__main__":
    env = sys.argv[1]
    n_agents = int(sys.argv[2])
    main(env, n_agents)

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


    #######################

    # main('env_trial2.txt', 3, agent_list=test_agent_ep, task_list=test_task_ep)

