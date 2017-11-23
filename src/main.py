#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''This is the program that needs to be run to execute our simulation'''

from reserv_table import *
from env import GridMap
from global_utility import genRandEndpoint
from global_utility import assignTasks
from global_utility import incrementTimestep
from agent import Agent
from task import Task

import random
import sys

_DEBUG = False

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


# test path of 4 agents, the zeros represent an agent waiting one time step
"""
env = GridMap('env_files/env_trial.txt')
reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)
global_timestep = 0
TaskIDGen = 0

### INITIALIZATION ###
agent0Start = env.endpoints[0]
agent1Start = env.endpoints[1]

agent0 = Agent(0, agent0Start)
agent1 = Agent(1, agent1Start)

dropoff0 = env.endpoints[-1]
dropoff1 = env.endpoints[-4]

task0 = Task(0, agent0.currentState, dropoff0, "dropoff", reserv_table)
task1 = Task(1, agent1.currentState, dropoff1, "dropoff", reserv_table)

tasks = [task0, task1]
agents = [agent0, agent1]

agent0.assignTask(task0)
agent1.assignTask(task1)

print("Agents:")
for i,agent in enumerate(agents):
    print("Agent {} init state: {}".format(i, agent.currentState))
    print("Agent {} goal state: {}\n".format(i, agent.task.getDropoff()))

agentsDone = False

reserv_table.resvAgentInit(agents)

### ACTION ###
while not agentsDone:
    for agent in agents:
        if agent.getPlan() is None:
            if not agent.isAgentIdle():
                agent.planPath(reserv_table, global_timestep)
                # Add path to res_table
            else:
                # plan mini path to stay put
                # Add path to res_table
                print("test")
                agent.plan = [(agent.currentState[0],agent.currentState[1])]
    incrementTimestep(agents)
    agentDoneCount = 0
    for agent in agents:
        if agent.isAgentIdle():
            agentDoneCount += 1
    if agentDoneCount == len(agents):
        agentsDone = True


### PRINT RESULTS ###
agentPaths = [agent.getPath() for agent in agents]



print("Final Paths: \n")
for i,agent in enumerate(agents):
    print("Agent {}: {}".format(i, agent.getPath()))

env.display_map(agentPaths)

'''
Random Pseudocode

for agent in range(2):
    genRandEndpoint(env.endpoints)




dropoff0 = genRandEndpoint(env.endpoints)
dropoff1 = genRandEndpoint(env.endpoints)
'''
"""

def main(env, n_agents, random_tasks=True, agent_list=None, task_list=None):
    """TODO: Docstring for main.

    :env: path to environment file
    :n_agents: number of agent/task pairs to generate randomly
    :random_tasks: in True, generate random pairs of agent/tasks
    :agent_list: if not random tasks, list of agents
    :task_list: if not random tasks, list of tasks
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

    agentsDone = False

    reserv_table.resvAgentInit(agents)

    ### ACTION ###
    while not agentsDone:
        for agent in agents:
            if agent.getPlan() is None:
                if not agent.isAgentIdle():
                    agent.planPath(reserv_table, global_timestep)
                    # Add path to res_table
                else:
                    # plan mini path to stay put
                    # Add path to res_table
                    agent.plan = [(agent.currentState[0],agent.currentState[1])]
        incrementTimestep(agents)
        agentDoneCount = 0
        for agent in agents:
            if agent.isAgentIdle():
                agentDoneCount += 1
        if agentDoneCount == len(agents):
            agentsDone = True

    ### PRINT RESULTS ###
    agentPaths = [agent.getPath() for agent in agents]

    if _DEBUG:
        print("Final Paths: \n")
        for i,agent in enumerate(agents):
            print("Agent {}: {}".format(i, agent.getPath()))

    env.display_map(agentPaths)


if __name__ == "__main__":
    print(sys.argv)
    env = sys.argv[1]
    n_agents = int(sys.argv[2])
    main(env, n_agents)
