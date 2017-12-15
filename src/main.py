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
from global_utility import incrementTimestep, incrementTimestepWHCA
from global_utility import bfs_endpoints
from global_utility import _ACTIONS
from agent import Agent
from task import Task
from analysis import *

import matplotlib.pyplot as plt
import random
import sys
import copy

_DEBUG = False
_DISPLAY = True # display animation

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

def gen_tasks_agents(env, reserv_table, n_agents, heuristic):
    # This first part is very similar to init_agent_tasks(), but doesn't assign tasks.
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
    return agent_list, task_list

def findNearestAgent(agents, task):
    sortedAgents = []
    for agent in agents:
        eligible = False    # This flag is used to check if the current agent is idle or has an artificial task
        if agent.isAgentIdle(): # If the agent is Idle, set the flag
            eligible = True
        elif str(agent.task.taskId)[0] == 'a': # If the agent is not idle, but
            eligible = True
        if eligible == True:    # If the flag was set
            initDist = task.trueHeurDrop[agent.currentState[:2]]  # Get the initial distance
            sortedAgents.append((initDist, agent))  # Add the agent to the list
    sortedAgents.sort() # Once all of the agents have been collected, sort the list according to the distance
    desiredAgent = sortedAgents[0][1]  # Get the best agent
    desiredAgent.assignTask(task)   # Assign the task to the agent
    return desiredAgent # Return the agent

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

    assignedAgents = [] # This list will hold the agents that have been assigned tasks
    assignedTasks = []  # This list will hold the tasks that have been assigned an agent
    unassignedTasks = copy.deepcopy(task_list)  # This list will hold the tasks that still need an agent

    '''Bidding War Algorithm'''

    # This is the largest while loop in the algorithm: until we have assigned all tasks have been assigned to an agent
    while len(unassignedTasks) > 0:
        task = unassignedTasks[0]   # Get the next task
        sortedAgents = []           # Create a list that holds agents according to the task's priority

        # For every agent in the list
        for agent in agent_list:
            initDist = task.trueHeurDrop[agent.currentState[:2]] # Get the initial distance between the task and the agent
            sortedAgents.append((initDist, agent))               # Add that distance and agent as a tuple into the list to be sorted
        sortedAgents.sort() # After all agents are in, sort the list according to their initDist

        validAgent = False  # This is a flag that allows us to break the next while loop when the task finds a valid agent

        # Until the list of sorted agents are empty and we don't have a valid agent
        while len(sortedAgents) != 0 and validAgent == False:
            currentAgent = sortedAgents[0][1]       # Get the task's new favorite agent
            if currentAgent in assignedAgents:      # If that agent has already been claimed
                competingTask = currentAgent.task   # Get the task that claimed it

                # If the current task has a higher bid than the previous task
                if task.trueHeurDrop[currentAgent.currentState[:2]] < competingTask.trueHeurDrop[currentAgent.currentState[:2]]:
                    currentAgent.assignTask(task)           # Reassign the agent to this current task
                    assignedTasks.remove(competingTask)     # Remove the previous task from the list of assigned tasks
                    assignedTasks.append(task)              # Add the current task to the list of assigned tasks
                    unassignedTasks.append(competingTask)   # Add the previous task to the list of unassigned tasks
                    validAgent = True                       # Set the flag so we can escape this while loop

                # Otherwise, if the previous task had the higher bid
                else:
                    sortedAgents.pop(0)                     # Remove this agent from our list of sorted agents and start again

            # Otherwise, if the agent in question hasn't already been claimed
            else:
                currentAgent.assignTask(task)       # Assign the task to the agent
                assignedAgents.append(currentAgent) # Add the agent to the list of assigned agents
                assignedTasks.append(task)          # Add the task to the list of assigned tasks
                validAgent = True                   # Set the flag so we can escape this while loop

        unassignedTasks.pop(0)                      # Once we get here, we have assigned an agent to this task.  Now remove it from the list of unassigned tasks
    return assignedAgents, assignedTasks            # In the end, return the list of assigned tasks and agents



def run_hca(agents, tasks,env, reserv_table, heuristic, unassignedTasks, frequency):
    """TODO: Docstring for plan_hca.

    :agents: TODO
    :reserv_table: TODO
    :returns: TODO

    """
    TaskIDGen = 0
    global_timestep = 0
    artif_task_count = 0
    agentsDone = False
    agentFailureCount = 0

    ### ACTION ###
    while not agentsDone or len(unassignedTasks) > 0:
        if len(unassignedTasks) > 0 and global_timestep % frequency == 0:
            findNearestAgent(agents, unassignedTasks[0])
            unassignedTasks.pop(0)
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

        # print("timestep:{}".format(global_timestep))
        incrementTimestep(agents, reserv_table)
        global_timestep += 1
        agentDoneCount = 0
        for agent in agents:
            if agent.isAgentIdle():
                agentDoneCount += 1
        if agentDoneCount == len(agents):
            agentsDone = True

def run_whca(agents, tasks,env, reserv_table, heuristic, window):
    """TODO: Docstring for plan_hca.

    :agents: TODO
    :reserv_table: TODO
    :returns: TODO

    """
    TaskIDGen = 0
    global_timestep = 0
    artif_task_count = 0
    agentsDone = False
    agentFailureCount = 0

    # k = window//2
    k = window

    busy_agents = copy.deepcopy(agents)
    idle_agents = []

    while len(busy_agents) > 0:
        if global_timestep % k == 0:
            #if global_timestep != 0:
            #    for agent in busy_agents:
            #        print(agent.plan)
            #        reserv_table.clearPlan(agent.plan)

            # reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)
            # reserv_table.resvAgentInitWHCA(busy_agents, global_timestep)
            # reserv_table.resvAgentInitWHCA(idle_agents, global_timestep)
            random.shuffle(busy_agents)
            for agent in busy_agents:
                agent.planPathWHCA(reserv_table, global_timestep, heuristic )
                if len(agent.plan) >= window:
                    agent.plan = agent.plan[:window]
                reserv_table.resvPath(agent.plan, global_timestep)

        incrementTimestepWHCA(busy_agents, idle_agents,reserv_table)

        for agent in idle_agents:
            # local repair for idle agents
            if agent.isAgentIdle():
                #next_state = reserv_table.checkStateResv(agent.currentState[:2], agent.currentState[2] + 1)
                second_state = reserv_table.checkStateResv(agent.currentState[:2], agent.currentState[2] + 2)
                third_state = reserv_table.checkStateResv(agent.currentState[:2], agent.currentState[2] + 3)
                #if next_state == True or second_state == True or third_state == True:
                if second_state == True or third_state == True:
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
                    agent.planPathWHCA(reserv_table, global_timestep, heuristic)
                    artif_task_count += 1

        global_timestep += 1

    return idle_agents

def run_lra(agents, tasks, env, reserv_table, heuristic):
    """TODO: Docstring for plan_lra.

    :arg1: TODO
    :returns: TODO

    """
    global_timestep = 0
    agentsDone = False
    agitation = 0
    failure=False

    while not agentsDone:
        for agent in agents:
            if agent.getPlan() is None:
                if not agent.isAgentIdle():
                    agent.planPathLRA(reserv_table, global_timestep, heuristic, agitation)
                    # print(agent.plan)

        next_state = []
        for agent1 in agents:
            if agent1.getPlan() is not None:
                for agent2 in agents:
                    if agent2.getPlan() is not None:
                        agent1_x = agent1.currentState[0]
                        agent1_y = agent1.currentState[1]
                        agent1_t = agent1.currentState[2]
                        agent2_x = agent2.currentState[0]
                        agent2_y = agent2.currentState[1]
                        agent2_t = agent2.currentState[2]
                        if agent1.plan[0] == agent2.plan[0] and agent1._id != agent2._id: # Going to same spot
                            # print('collision')
                            #agent1.planPathLRA(reserv_table, global_timestep, heuristic)
                            #agent2.planPathLRA(reserv_table, global_timestep, heuristic)
                            agent1.plan = None
                            agent2.plan = None
                            agitation += 1
                            # print agitation
                            break
                        if agent1.plan[0] == (agent2_x,agent2_y,agent2_t+1) and agent2.plan[0] == (agent1_x,agent1_y,agent1_t+1): # Crossing over
                            # print('collision 2')
                            #agent1.planPathLRA(reserv_table, global_timestep, heuristic)
                            #agent2.planPathLRA(reserv_table, global_timestep, heuristic)
                            agent1.plan = None
                            agent2.plan = None
                            agitation += 1
                            # print agitation
                            break
                        if agent1.plan[0] == (agent2_x,agent2_y,agent2_t+1): # and agent2.plan[0] == (agent2_x,agent2_y,agent2_t+1): # Moving into occupied
                            # print('collision 3a')
                            agent1.plan = None
                            #agent2.plan = None
                            agitation += 1
                            # print agitation
                            break
                        if agent2.plan[0] == (agent1_x,agent1_y,agent1_t+1): # and agent1.plan[0] == (agent1_x,agent1_y,agent1_t+1): # Moving into occupied
                            # print('collision 3b')
                            agent2.plan = None
                            #agent1.plan = None
                            agitation += 1
                            # print agitation
                            break
                    else:
                        agent1_x = agent1.currentState[0]
                        agent1_y = agent1.currentState[1]
                        agent1_t = agent1.currentState[2]
                        agent2_x = agent2.currentState[0]
                        agent2_y = agent2.currentState[1]
                        agent2_t = agent2.currentState[2]
                        if agent1.plan[0] == (agent2_x,agent2_y,agent2_t+1):
                            # print('collision 4a')
                            agent1.plan = None
                            break
            else:
                for agent2 in agents:
                    agent1_x = agent1.currentState[0]
                    agent1_y = agent1.currentState[1]
                    agent1_t = agent1.currentState[2]
                    agent2_x = agent2.currentState[0]
                    agent2_y = agent2.currentState[1]
                    agent2_t = agent2.currentState[2]
                    if agent2.getPlan() is not None:
                        if agent2.plan[0] == (agent1_x,agent1_y,agent1_t+1):
                            # print('collision 4b')
                            agent2.plan = None
                            break
        if agitation >= 10 :
            agitation = 0

        incrementTimestep(agents, reserv_table)
        global_timestep += 1
        if global_timestep == 200:
            failure = True
            break

        agentDoneCount = 0
        for agent in agents:
            if agent.isAgentIdle():
                agentDoneCount += 1
        if agentDoneCount == len(agents):
            agentsDone = True
            # print('done')

    return failure

def main(env_name,alg, heuristic, n_agents, agent_list=None, task_list=None, regret=False, frequency=3):
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

    env = GridMap('env_files/{}'.format(env_name))
    reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)
    if regret == False:
        agents, tasks = init_agents_tasks(env, reserv_table, n_agents,
                                          agent_list, task_list, heuristic)

        task_goals = [agent.task.dropoffState for agent in agents]

        if _DEBUG:
            print("\nAgent Starts and Goals")
            print("------------------------\n")

            for i, agent in enumerate(agents):
                print("Agent {}:".format(i))
                print("\t Start: {}".format(agent.currentState))
                print("\t Goal:   {}".format(agent.task.dropoffState))

        reserv_table.resvAgentInit(agents)

        ### ACTION ###
        if alg == 'hca':
            run_hca(agents, tasks, env, reserv_table, heuristic, [], None )
        if alg == 'whca':
            agents = run_whca(agents, tasks, env, reserv_table, heuristic, window=20 )
        if alg == 'lra':
            run_lra(agents, tasks, env, reserv_table, heuristic)

        reserv_table.display(env)
        if _DEBUG:
            print("Creating Animation...")

        ### ANIMATE RESULTS ###
        agent_paths = [agent.path for agent in agents]
        path_costs = [agent.planCost for agent in agents]

        if _DISPLAY:
            env.display_map(agent_paths, record=False)
        # path_analysis(agent_paths, task_goals, path_costs)

        return agent_paths, task_goals, path_costs

    else:
        # Create copies of the environment and the reservation table
        env_copy = GridMap('env_files/{}'.format(env_name))
        reserv_table_copy = Reserv_Table(env.occupancy_grid, env.rows, env.cols)

        # Create two copies of a random sample of tasks and agents
        agent_list, task_list = gen_tasks_agents(env, reserv_table, n_agents, heuristic)
        task_list_copy = copy.deepcopy(task_list)
        agent_list_copy = copy.deepcopy(agent_list)

        # Find an optimal baseline to compare against
        agents_baseline, tasks_baseline = init_agents_tasks_with_regret(env, reserv_table, n_agents,
                                                                        agent_list, task_list, heuristic)

        reserv_table.resvAgentInit(agent_list_copy)

        ### ACTION ###
        run_planner(agent_list, task_list, env, reserv_table, heuristic, [], None)
        agent_paths = [agent.path for agent in agent_list]
        path_costs = [agent.planCost for agent in agent_list]

        #findNearestAgent(agent_list_copy, task_list_copy[0])

        run_planner(agent_list_copy, task_list_copy, env_copy, reserv_table_copy, heuristic, task_list_copy, frequency)
        agent_paths_regret = [agent.path for agent in agent_list_copy]
        path_costs_regret = [agent.planCost for agent in agent_list_copy]

        env.display_map(agent_paths, record=False)
        env_copy.display_map(agent_paths_regret, record=False)
        #path_analysis(agent_paths, task_goals, path_costs)
        #path_analysis_regret(agent_paths_regret, task_goals, path_costs_regret)

        # Do the regret analysis:
        taskCompSumBaseline = 0.0
        taskCompSumRegret = 0.0
        for agent in agent_list:
            for value in agent.taskCompetionTime:
                taskCompSumBaseline += value
        for agent in agent_list_copy:
            for value in agent.taskCompetionTime:
                taskCompSumRegret += value

        regret = taskCompSumRegret/taskCompSumBaseline
        print("Regret: ", regret)

        return agent_paths, path_costs

if __name__ == "__main__":
    env = sys.argv[1]
    planner = sys.argv[2]
    n_agents = int(sys.argv[3])
    main(env,planner, heuristic='manhattan', n_agents=n_agents, regret=False, frequency=3)

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

    # print('true heur')

    # main('env_warehouse2.txt','hca','true', len(test_agent_ep),
    #      agent_list=test_agent_ep, task_list=test_task_ep, regret=False)

    # print('manhattan')

    # main('env_warehouse2.txt','hca','manhattan', len(test_agent_ep),
    #      agent_list=test_agent_ep, task_list=test_task_ep, regret=False)
