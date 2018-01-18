#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: analysis.py
Author: Cade Parkison
Email: cadeparkison@gmail.com
Github: c-park
Description: Module to analyize the effectiveness of our algorithm.

TODO:
    - function that simulates an environment with multiple agent/task locations
      and counts the number of successes and failues (collisions or not all goals reached)

    - A measure of path optimality

    - Generate report plots, showing efficiency, optimality, number of failures,
      etc.
"""

import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
import sys
import copy

from main import *


_DEBUG=False
_DISPLAY = True
_RECORD = False

def avg_path_distance(paths):
    """Computes the distance travelled of an agent's path by removing all
       duplicate locations.

       TODO: BUG: Measures total distance travelled, not distance travelled to
             reach goal.

    :paths: list of paths taken by all agents
    :returns: average distance travelled

    """
    distances = [len(set([p[:2] for p in path]))-1 for path in paths]

    if _DEBUG:
        for i,d in enumerate(distances):
            print('Path {} distance: {}'.format(i,d))

    avg_distance = np.mean(distances)

    return avg_distance

def avg_path_time(plans):
    """Given a list of paths, find average path time

    :paths: list of paths taken by all agents
    :path_costs: list of costs for each path taken
    :returns: time, distance, cost averages
    """
    path_times = [len(plan)-1 for plan in plans]

    if _DEBUG:
        for i,t in enumerate(path_times):
            print('Path {} time: {}'.format(i,t))

    avg_time = np.mean(path_times)

    return avg_time

def avg_path_cost(path_costs):
    """TODO: Docstring for avg_path_cost.

    :path_costs: TODO
    :returns: TODO

    """
    if _DEBUG:
        for i,c in enumerate(path_costs):
            print('Path {} cost: {}'.format(i,c))

    return np.mean(path_costs)

def count_collisions(paths):
    """Counts the number of collisions between agents

    :paths: TODO
    :returns: TODO

    """
    collisions = 0
    # for all combinations of two paths, add the number of collisions to total
    for i,j in combinations(paths,2):
        collisions += len(set(i).intersection(j))

    return collisions

def path_analysis(total_paths, goals, path_costs, failure_count):
    """Given the results of path finding algorithm, print out analysis data to
       command line.

    :paths: TODO
    :path_cost: TODO
    :returns: TODO

    """
    if _DEBUG:
        print("total paths: {}".format(total_paths))
        print("goals: {}".format(goals))
        print("path_costs: {}".format(goals))

    # Removes 3rd time dimension
    path_states = [[l[:2] for l in path] for path in total_paths]

    # find paths to goals from total_paths
    goal_indices = [path.index(goals[i]) for i, path in enumerate(path_states)]
    paths_to_goals = [path[:goal_indices[i]+1] for i, path in enumerate(total_paths)]

    # goal_indices = []
    # paths_to_goals= []
    # for i, path in enumerate(path_states):
    #     try:
    #         goal_indices.append(path.index(goals[i]))
    #     except ValueError:
    #         pass
    # for i, path in enumerate(total_paths):
    #     try:
    #         paths_to_goals.append(path[:goal_indices

    # paths_to_goals = [path[:goal_indices[i]+1] for i, path in enumerate(total_paths)]

    avg_dist = avg_path_distance(paths_to_goals)
    avg_time = avg_path_time(paths_to_goals)
    avg_cost = avg_path_cost(path_costs)

    if _DISPLAY:
        print('Analyzing paths...')
        print('---------------------')
        print('Average Path Distance: {}'.format(avg_dist))
        print('Average Path Time: {} timesteps'.format(avg_time))
        print('Average Path Cost: {}'.format(avg_cost))
        print('Failure: {}\n'.format(bool(failure_count)))

    return avg_dist, avg_time, avg_cost

def main_analysis(env_name, n_agents):


    env = GridMap('env_files/{}'.format(env_name))
    reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)


    agents_CA, tasks_CA = init_agents_tasks(env, reserv_table, n_agents,
                                            agent_list=None, task_list=None,
                                            heuristic='manhattan')

    agent_eps = [env.endpoints.index(agent.currentState[:2]) for agent in agents_CA]
    task_eps =  [env.endpoints.index(task.dropoffState) for task in tasks_CA]

    agents_HCA, tasks_HCA = init_agents_tasks(env, reserv_table, n_agents,
                                                  agent_eps, task_eps, 'true')

    ###################
    # CA*
    ###################

    reserv_table_CA = Reserv_Table(env.occupancy_grid, env.rows, env.cols)

    task_goals_CA = [agent.task.dropoffState for agent in agents_CA]

    if _DEBUG:
        print("\nAgent Starts and Goals")
        print("------------------------\n")

        for j, agent in enumerate(agents_CA):
            print("Agent {}:".format(j))
            print("\t Start: {}".format(agent.currentState))
            print("\t Goal:   {}".format(agent.task.dropoffState))

    reserv_table_CA.resvAgentInit(agents_CA)

    ### ACTION ###
    run_hca(agents_CA, tasks_CA, env, reserv_table_CA, 'manhattan', [], None)

    failure_count_CA = 0
    for agent in agents_CA:
        if agent.failure:
            failure_count_CA += 1

    if _DEBUG:
        reserv_table_CA.display(env)
        print("Creating Animation...")

    ### ANIMATE RESULTS ###
    agent_paths_CA = [agent.path for agent in agents_CA]
    path_costs_CA = [agent.planCost for agent in agents_CA]

    if _DISPLAY:
        env.display_map(agent_paths_CA, record=_RECORD, fn='trial_6_ca')
    if _DEBUG:
        path_analysis(agent_paths_CA, task_goals_CA, path_costs_CA)

    results_CA = (agent_paths_CA, task_goals_CA, path_costs_CA, failure_count_CA)

    ###################
    # HCA*
    ###################
    reserv_table_HCA = Reserv_Table(env.occupancy_grid, env.rows, env.cols)

    task_goals_HCA = [agent.task.dropoffState for agent in agents_HCA]

    if _DEBUG:
        print("\nAgent Starts and Goals")
        print("------------------------\n")

        for j, agent in enumerate(agents_HCA):
            print("Agent {}:".format(j))
            print("\t Start: {}".format(agent.currentState))
            print("\t Goal:   {}".format(agent.task.dropoffState))

    reserv_table_HCA.resvAgentInit(agents_HCA)

    ### ACTION ###
    run_hca(agents_HCA, tasks_HCA, env, reserv_table_HCA,'true' , [], None)

    failure_count_HCA = 0
    for agent in agents_HCA:
        if agent.failure:
            failure_count_HCA += 1

    if _DEBUG:
        reserv_table_HCA.display(env)
        print("Creating Animation...")

    ### ANIMATE RESULTS ###
    agent_paths_HCA = [agent.path for agent in agents_HCA]
    path_costs_HCA = [agent.planCost for agent in agents_HCA]

    if _DISPLAY:
        env.display_map(agent_paths_HCA, record=_RECORD, fn='trial_6_hca')
    if _DEBUG:
        path_analysis(agent_paths_HCA, task_goals_HCA, path_costs_HCA)

    results_HCA = (agent_paths_HCA, task_goals_HCA, path_costs_HCA, failure_count_HCA)

    return results_CA, results_HCA

def main_analysis_regret(env_name, n_agents):

    env = GridMap('env_files/{}'.format(env_name))
    reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)


    agents_CA, tasks_CA = init_agents_tasks(env, reserv_table, n_agents,
                                            agent_list=None, task_list=None,
                                            heuristic='manhattan')

    agent_eps = [env.endpoints.index(agent.currentState[:2]) for agent in agents_CA]
    task_eps =  [env.endpoints.index(task.dropoffState) for task in tasks_CA]

    agents_HCA, tasks_HCA = init_agents_tasks(env, reserv_table, n_agents,
                                                  agent_eps, task_eps, 'true')

    ###################
    # CA*
    ###################

    reserv_table_CA = Reserv_Table(env.occupancy_grid, env.rows, env.cols)

    task_goals_CA = [agent.task.dropoffState for agent in agents_CA]

    if _DEBUG:
        print("\nAgent Starts and Goals")
        print("------------------------\n")

        for j, agent in enumerate(agents_CA):
            print("Agent {}:".format(j))
            print("\t Start: {}".format(agent.currentState))
            print("\t Goal:   {}".format(agent.task.dropoffState))

    reserv_table_CA.resvAgentInit(agents_CA)

    ### ACTION ###
    run_hca(agents_CA, tasks_CA, env, reserv_table_CA, 'manhattan', [], None)

    failure_count_CA = 0
    for agent in agents_CA:
        if agent.failure:
            failure_count_CA += 1

    ### ANIMATE RESULTS ###
    agent_paths_CA = [agent.path for agent in agents_CA]
    path_costs_CA = [agent.planCost for agent in agents_CA]

    if _DISPLAY:
        env.display_map(agent_paths_CA, record=_RECORD, fn='trial_6_ca')
    if _DEBUG:
        path_analysis(agent_paths_CA, task_goals_CA, path_costs_CA)

    results_CA = (agent_paths_CA, task_goals_CA, path_costs_CA, failure_count_CA)


    ################
    # Assignment rates
    ################

    env_copy = GridMap('env_files/{}'.format(env_name))
    reserv_table_copy = Reserv_Table(env.occupancy_grid, env.rows, env.cols)


    # Find an optimal baseline to compare against
    agents_baseline, tasks_baseline = init_agents_tasks_with_regret(env, reserv_table, n_agents,
                                                                    agents_HCA, tasks_HCA, heuristic)

    reserv_table.resvAgentInit(agent_list_copy)

    ### ACTION ###
    run_planner(agent_list, task_list, env, reserv_table, heuristic, [], None)
    agent_paths = [agent.path for agent in agent_list]
    path_costs = [agent.planCost for agent in agent_list]

    #findNearestAgent(agent_list_copy, task_list_copy[0])

    run_planner(agent_list_copy, task_list_copy, env_copy, reserv_table_copy, heuristic, task_list_copy, frequency)
    agent_paths_regret = [agent.path for agent in agent_list_copy]
    path_costs_regret = [agent.planCost for agent in agent_list_copy]

    env.display_map(agent_paths, record=_RECORD)
    env_copy.display_map(agent_paths_regret, record=_RECORD)

def main_analysis_iter(env_name, n_agents, iterations=5):
    """TODO: Only works for regret=False right now.

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
    :iterations: number of times to run main loop to average analysis parameters

    :Returns: Agent paths, task dropoff endpoints

    """
    env = GridMap('env_files/{}'.format(env_name))
    reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)

    # Set of agent and task lists to test algorithm performance
    test_set_CA = []
    test_set_HCA =[]

    # generate random agent and task list combinations
    for i in range(iterations):
        agents_CA, tasks_CA = init_agents_tasks(env, reserv_table, n_agents,
                                                agent_list=None, task_list=None,
                                                heuristic='manhattan')

        agent_eps = [env.endpoints.index(agent.currentState[:2]) for agent in agents_CA]
        task_eps =  [env.endpoints.index(task.dropoffState) for task in tasks_CA]

        agents_HCA, tasks_HCA = init_agents_tasks(env, reserv_table, n_agents,
                                                  agent_eps, task_eps, 'true')

        test_set_CA.append((agents_CA, tasks_CA))
        test_set_HCA.append((agents_HCA, tasks_HCA))


    # for i in range(iterations):
    #     print("")
    #     print("CA agent {} inits: {}".format(i, [test_set_CA[i][0][j].currentState for j in range(n_agents)]))
    #     print("CA task {} dropoffs: {}".format(i, [test_set_CA[i][1][j].dropoffState for j in range(n_agents)]))


    # for i in range(iterations):
    #     print("")
    #     print("HCA agent {} inits: {}".format(i, [test_set_HCA[i][0][j].currentState for j in range(n_agents)]))
    #     print("HCA task {} dropoffs: {}".format(i, [test_set_HCA[i][1][j].dropoffState for j in range(n_agents)]))

    # Lists to hold the paths, goals, and costs for the different algorithms
    results_CA = []

    # Cooperative A* (Manhattan Heur)
    for i in range(iterations):
        reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)

        agents = test_set_CA[i][0]
        tasks = test_set_CA[i][1]

        task_goals = [agent.task.dropoffState for agent in agents]

        if _DEBUG:
            print("\nAgent Starts and Goals")
            print("------------------------\n")

            for j, agent in enumerate(agents):
                print("Agent {}:".format(j))
                print("\t Start: {}".format(agent.currentState))
                print("\t Goal:   {}".format(agent.task.dropoffState))

        reserv_table.resvAgentInit(agents)

        ### ACTION ###
        run_hca(agents, tasks, env, reserv_table, 'manhattan', [], None)

        failure_count = 0
        for agent in agents:
            if agent.failure:
                failure_count += 1


        if _DEBUG:
            reserv_table.display(env)
            print("Creating Animation...")

        ### ANIMATE RESULTS ###
        agent_paths = [agent.path for agent in agents]
        path_costs = [agent.planCost for agent in agents]

        if _DISPLAY:
            env.display_map(agent_paths, record=_RECORD)
        if _DEBUG:
            path_analysis(agent_paths, task_goals, path_costs)

        results_CA.append((agent_paths, task_goals, path_costs, failure_count))


    results_HCA = []

    # Hierarchical Cooperative A* (trueHeur)
    for k in range(iterations):
        reserv_table = Reserv_Table(env.occupancy_grid, env.rows, env.cols)

        agents = test_set_HCA[k][0]
        tasks = test_set_HCA[k][1]

        task_goals = [agent.task.dropoffState for agent in agents]

        if _DEBUG:
            print("\nAgent Starts and Goals")
            print("------------------------\n")

            for j, agent in enumerate(agents):
                print("Agent {}:".format(j))
                print("\t Start: {}".format(agent.currentState))
                print("\t Goal:   {}".format(agent.task.dropoffState))

        reserv_table.resvAgentInit(agents)

        ### ACTION ###
        run_hca(agents, tasks, env, reserv_table,'true' , [], None)

        failure_count = 0
        for agent in agents:
            if agent.failure:
                failure_count += 1

        if _DEBUG:
            reserv_table.display(env)
            print("Creating Animation...")

        ### ANIMATE RESULTS ###
        agent_paths = [agent.path for agent in agents]
        path_costs = [agent.planCost for agent in agents]

        if _DISPLAY:
            env.display_map(agent_paths, record=_RECORD)
        if _DEBUG:
            path_analysis(agent_paths, task_goals, path_costs)

        results_HCA.append((agent_paths, task_goals, path_costs, failure_count))

    return results_CA, results_HCA

def test_single(env, n_agents):
    results_CA, results_HCA = main_analysis(env, n_agents)

    print("Test Parameters")
    print('-----------------\n')
    print("Environment: {}".format(env))
    print("Number of agents: {}\n".format(n_agents))

    print("-----------------------")
    print("Cooperative A* Results:")
    print("-----------------------")
    path_analysis(results_CA[0], results_CA[1], results_CA[2], results_CA[3])

    print("-----------------------")
    print("Hierarchical Cooperative A* Results:")
    print("-----------------------")
    path_analysis(results_HCA[0], results_HCA[1], results_HCA[2], results_HCA[3])


def test_multi(env,n_agents,n_iterations):
    results_CA, results_HCA = main_analysis_iter(env, n_agents, n_iterations)

    print('Iteration Test Parameters')
    print('-----------------\n')
    print("Environment: {}".format(env))
    print("Number of agents: {}".format(n_agents))
    print("Number of trial iterations: {}\n".format(n_iterations))

    avg_dist_CA = []
    avg_time_CA = []
    avg_cost_CA = []
    avg_failures_CA = 0

    avg_dist_HCA = []
    avg_time_HCA = []
    avg_cost_HCA = []
    avg_failures_HCA = 0

    print("-----------------------")
    print("Cooperative A* Results:")
    print("-----------------------")

    # print("results: {}".format(results_CA))
    for i,result in enumerate(results_CA):
        dist, time, cost = path_analysis(result[0], result[1], result[2],result[3])
        failure = int(bool(result[3]))

        avg_dist_CA.append(dist)
        avg_time_CA.append(time)
        avg_cost_CA.append(cost)
        avg_failures_CA += failure

    #     print("\nIteration {} Results:".format(i))
        # print("total paths: {}".format(result[0]))
        # print("goals: {}".format(result[1]))
        # print("path_costs: {}".format(result[2]))
        # path_analysis(result[0], result[1], result[2])

    avg_dist_CA = np.mean(avg_dist_CA)
    avg_time_CA = np.mean(avg_time_CA)
    avg_cost_CA = np.mean(avg_cost_CA)

    print("Average path distance: {}".format( avg_dist_CA))
    print("Average path time: {}".format(avg_time_CA))
    print("Average cost: {}".format(avg_cost_CA))
    print("Number of failures: {}".format(avg_failures_CA))


    print("\n-----------------------")
    print("Hierarchical Cooperative A* Results:")
    print("-----------------------")
    # print("results: {}".format(results_HCA))
    for i,result in enumerate(results_HCA):
        dist, time, cost = path_analysis(result[0], result[1], result[2],result[3])
        failure = int(bool(result[3]))

        avg_dist_HCA.append(dist)
        avg_time_HCA.append(time)
        avg_cost_HCA.append(cost)
        avg_failures_HCA += failure

    #     print("\nIteration {} Results:".format(i))
        # print("total paths: {}".format(result_[0]))
        # print("goals: {}".format(result_[1]))
        # print("path_costs: {}".format(result_[2]))
        # path_analysis(result_[0], result_[1], result_[2])

    avg_dist_HCA = np.mean(avg_dist_HCA)
    avg_time_HCA = np.mean(avg_time_HCA)
    avg_cost_HCA = np.mean(avg_cost_HCA)

    print("Average path distance: {}".format( avg_dist_HCA))
    print("Average path time: {}".format(avg_time_HCA))
    print("Average cost: {}".format(avg_cost_HCA))
    print("Number of failures: {}".format(avg_failures_HCA))

if __name__ == "__main__":

    # env = sys.argv[1]
    # n_agents = int(sys.argv[2])
    # n_iterations = int(sys.argv[3])

    # test_multi(env, n_agents, n_iterations)


    env = sys.argv[1]
    n_agents = int(sys.argv[2])

    test_single(env, n_agents)


