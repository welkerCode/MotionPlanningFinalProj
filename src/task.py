#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: task.py
Authors: Taylor Welker, Cade Parkison, Paul Wadsworth
Emails: <taylormaxwelker@gmail.com>,  <cadeparkison@gmail.com>, <wadspau2@gmail.com>
Githubs: welkerCode, c-park
Description: Implements Task Class
"""

from global_utility import bfs_search_map
from global_utility import _ACTIONS
from reserv_table import Reserv_Table

class Task:

    ###############################################
    ############# Class Variables #################
    ###############################################

    '''
    taskId          # This is a unique identifier that differentiates this task from the others (int value)
    pickupState     # This holds the state at which the pickup must occur (2D)
    dropoffState    # This holds the state at which the dropoff must occur (2D)
    taskStatus      # This holds the status of the task (one of 3 strings: 'pickup', 'dropoff', 'complete')
    timer           # This holds the number of time steps used to complete the task thus far (int value)
    #trueHeurPick
    trueHeurDrop
    '''
    ###############################################
    ############# Class Functions #################
    ###############################################

    # Initialization function
    def __init__(self, newId, newPickupState=None, newDropoffState=None,
                 newTaskStatus = "dropoff", res_table = None, heuristic=None):
        self.taskId = newId                 # Get the id of the task
        self.pickupState = newPickupState   # Get the pickup location
        self.dropoffState = newDropoffState # Get the dropoff location
        self.taskStatus = newTaskStatus     # Get the predefined status of the task (start at dropoff if agent is already at pickup location)
        self.timer = 0                      # Start the timer
        '''
        Add code for trueHeur dropoff
        Add code for trueHeur pickup
        '''
        if heuristic is not None:
            self.trueHeurDrop = bfs_search_map(self.dropoffState,
                                               res_table.transition2D, _ACTIONS)
        else:
            self.trueHeurDrop = {}

    # This function progresses the status of the task by one step
    def progressStatus(self):
        if self.taskStatus == "pending":
            self.taskStatus = "pickup"
        elif self.taskStatus == "pickup":
            self.taskStatus = "dropoff"
        elif self.taskStatus == "dropoff":
            self.taskStatus = "complete"
        else:
            self.taskStatus = "error"

    # This function updates the timer
    def tickTimer(self):
        self.timer = self.timer + 1

    ###############################################
    ############# Getters and Setters #############
    ###############################################

    def getTimer(self):
        return self.timer
    def getTaskStatus(self):
        return self.taskStatus
    def getPickup(self):
        return self.pickupState
    def setPickup(self, newPickupState):
        self.pickupState = newPickupState
    def getDropoff(self):
        return self.dropoffState
    def setDropoff(self, newDropoffState):
        self.dropoffState = newDropoffState

    '''
    There needs to be a task report class/table that holds the data associated with each task:
    -Time steps to acheive
    -Path
    -Agent that completed it

    '''

    '''
    Every time a new task initializes, run the whca_reverse search to find the
    true heuristic for every node in the map given the new dropoff location
    This dictionary of true heurisitcs will be stored as a member of the task
    class and will be accessed by the whca_search algorithm. Our reasons for
    doing this is to eliminate the need for a paused reverse search and to find
    the true heuristic of each node upfront. This means that the forward whca
    search will never call the reverse search directly.  Instead, every possible
    heuristic will already be calculated and stored in the task passed to it.
    '''
