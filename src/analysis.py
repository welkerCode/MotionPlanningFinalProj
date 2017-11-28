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
    distances = []
    for path in paths:
        # Ignores timestep, removes duplicate locations
        unique_positions = set([p[:2] for p in path])
        distances.append(len(unique_positions))
    avg_distance = np.mean(distances)

    return avg_distance

def avg_path_time(plans):
    """Given a list of paths, find average path time

    :paths: list of paths taken by all agents
    :path_costs: list of costs for each path taken
    :returns: time, distance, cost averages
    """
    avg_time = np.mean([len(plan) for plan in plans])

    return avg_time

def avg_path_cost(path_costs):
    """TODO: Docstring for avg_path_cost.

    :path_costs: TODO
    :returns: TODO

    """
    return np.mean(path_costs)

def count_collisions(paths):
    """Counts the number of collisions between agents

    :paths: TODO
    :returns: TODO

    """
    pass

def path_analysis(paths, plans, path_costs):
    """Given the results of path finding algorithm, print out analysis data to
       command line.

    :paths: TODO
    :path_cost: TODO
    :returns: TODO

    """

    print('Analyzing paths...')
    print('---------------------\n')
    print('Average Path Distance: {}'.format(avg_path_distance(paths)))
    print('Average Path Time: {} timesteps'.format(avg_path_time(plans)))
    print('Average Path Cost: {}'.format(avg_path_cost(path_costs)))

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

    test_agent_ep = [-5, -4]
    test_task_ep = [-1, -3]

    paths, plans, costs = main(env='env_small_warehouse.txt',
                               alg='hca',
                               heuristic='true',
                               n_agents=len(test_agent_ep),
                               agent_list=test_agent_ep,
                               task_list=test_task_ep,
                               animate=True)

    path_analysis(paths, plans, costs)


