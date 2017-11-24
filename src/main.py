#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: global_utility.py
Authors: Taylor Welker, Cade Parkison, Paul Wadsworth
Email:
Github:
Description: This is the program that needs to be run to execute our simulation"""

from reserv_table import *
from env import GridMap
from global_utility import genRandEndpoint
from global_utility import assignTasks
from global_utility import incrementTimestep
from agent import Agent
from task import Task

import random
import sys

_DEBUG = True

'''
init env

init_agents with goals
    init all tasks
        set up heur for each task x
        assign task to closest agent

        for(each task)
            for(each agent)
                if agentV.currentPos < prevAgent.pos
                    agentToAssign = agentV
            agentToAssign.task = task


init res_table(occ grid) x

set timestep to 0



while idle agents exists
    for agent
        if agent doesn't have plan
            if task assigned
                plan path for agent
                add path to res table
            else task not assigned
                plan to stay put
                add path to the res table
    increment timestep
        update all agent movements
            timer updated within agent's task
        unassign tasks if goal is reached and add to report

    for each agent
        agents done boolean = isAgentIdle & prev result
            If true, then all agents are now idle

'''

def main(env, n_agents, random_tasks=True, agent_list=None, task_list=None):
    """TODO: Docstring for main.

    :env: path to environment file
    :n_agents: number of agent/task pairs to generate randomly
    :random_tasks: in True, generate random pairs of agent/tasks
    :agent_list: if not random tasks, list of agent endpoint indexes
    :task_list: if not random tasks, list of task endpoint indexes
    :returns: TODO

    """

    env = GridMap('env_files/{}'.format(env))
    reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)
    global_timestep = 0
    TaskIDGen = 0

    agents = []
    tasks = []

    if random_tasks:
        # generates n_agents*2 samples from the list of endpoints
        samples = random.sample(env.endpoints,n_agents*2)
        for i in range(n_agents):
            # generate random agent/task pair
            agent = Agent(i, samples.pop())
            task = Task(i, agent.currentState, samples.pop() , "dropoff", reserv_table)
            agent.assignTask(task)
            agents.append(agent)
            tasks.append(task)

    else:
        for i in range(n_agents):
            agent = Agent(i, env.endpoints[agent_list[i]])
            task = Task(i, agent.currentState, env.endpoints[task_list[i]], "dropoff", reserv_table)
            agent.assignTask(task)
            agents.append(agent)
            tasks.append(task)


    if _DEBUG:
        print("Agent Starts and Goals")
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
                    agent.planPath(reserv_table, global_timestep)
                    print("Agent {} Plan: {}".format(agent._id, agent.plan))
                    # Add path to res_table
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

    reserv_table.display(env)

    ### PRINT RESULTS ###
    agentPaths = [agent.getPath() for agent in agents]

    if _DEBUG:
        print("\nFinal Paths: ")
        print("----------------------\n")
        for i,agent in enumerate(agents):
            print("Agent {}: {}".format(i, agent.getPath()))

    env.display_map(agentPaths)


if __name__ == "__main__":
    # env = sys.argv[1]
    # n_agents = int(sys.argv[2])
    # main(env, n_agents)

    test_agent_ep = [-3, -4, -2]
    test_task_ep = [2, -1, 1]

    main('env_trial.txt', 3, random_tasks=False, agent_list=test_agent_ep, task_list=test_task_ep)
