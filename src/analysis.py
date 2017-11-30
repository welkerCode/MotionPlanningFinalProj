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

from main import *


def avg_path_distance(paths):
    """Computes the distance travelled of an agent's path by removing all
       duplicate locations.

       TODO: BUG: Measures total distance travelled, not distance travelled to
             reach goal.

    :paths: list of paths taken by all agents
    :returns: average distance travelled

    """
    distances = [len(set([p[:2] for p in path]))-1 for path in paths]

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

    for i,t in enumerate(path_times):
        print('Path {} time: {}'.format(i,t))

    avg_time = np.mean(path_times)

    return avg_time

def avg_path_cost(path_costs):
    """TODO: Docstring for avg_path_cost.

    :path_costs: TODO
    :returns: TODO

    """
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

def path_analysis(total_paths, goals, path_costs):
    """Given the results of path finding algorithm, print out analysis data to
       command line.

    :paths: TODO
    :path_cost: TODO
    :returns: TODO

    """
    # Removes 3rd time dimension
    path_states = [[l[:2] for l in path] for path in total_paths]

    # find paths to goals from total_paths
    goal_indices = [path.index(goals[i]) for i, path in enumerate(path_states)]
    paths_to_goals = [path[:goal_indices[i]+1] for i, path in enumerate(total_paths)]

    print('Analyzing paths...')
    print('---------------------\n')
    print('Average Path Distance: {}\n'.format(avg_path_distance(paths_to_goals)))
    print('Average Path Time: {} timesteps\n'.format(avg_path_time(paths_to_goals)))
    print('Average Path Cost: {}\n'.format(avg_path_cost(path_costs)))

def failure_analysis(env, alg, heuristic, n_agents, agent_list, task_list, n_iterations):
    """Iterates over main path planning and calculates the number of failures
       to find paths, as well as the number of collisions in the paths it finds.

    :env: TODO
    :alg: TODO
    :heuristic: TODO
    :n_agents: TODO
    :agent_list: TODO
    :task_list: TODO
    :n_iterations: TODO
    :returns: TODO

    """
    pass


if __name__ == "__main__":

    env = sys.argv[1]
    n_agents = int(sys.argv[2])

    paths, goals, costs = main(env=env,
                               alg='hca',
                               heuristic='true',
                               n_agents=n_agents)

    # test_agent_ep = [-5, -4]
    # test_task_ep = [-1, -3]

    # paths, goals, costs = main(env='env_small_warehouse.txt',
    #                            alg='hca',
    #                            heuristic='true',
    #                            n_agents=len(test_agent_ep),
    #                            agent_list=test_agent_ep,
    #                            task_list=test_task_ep)

    print("Paths: {}\n".format(paths))
    print("Goals: {}\n".format(goals))
    print("Costs: {}\n".format(costs))
    print('')

    path_analysis(paths, goals, costs)


