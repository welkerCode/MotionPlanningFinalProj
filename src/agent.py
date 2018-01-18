#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: agent.py
Authors: Taylor Welker, Cade Parkison, Paul Wadsworth
Emails: <taylormaxwelker@gmail.com>,  <cadeparkison@gmail.com>, <wadspau2@gmail.com>
Githubs: welkerCode, c-park
Description: Holds the class description for the "Agent" class
"""


from priorityq import *
from task import *
from whca import whca_search


_DEBUG = False

class Agent:


    ###############################################
    ############# Class Functions #################
    ###############################################

    def __init__(self, _id,  initPos = (0,0), newTask = None):
        self._id = _id
        self.plan = None  # This holds the future actions that the planning algorithm will give the agent
        self.planCost = 0
        self.path = []  # This holds the paths that the agent has taken thus far.
        self.trueHeur = {}  # This holds the dictionary matching a state to a true heuristic
        self.currentState = (initPos[0], initPos[1], 0)   # This holds the current state the agent is in
        self.path.append(self.currentState) # We need to add the initial state to our path
        self.task = newTask # This holds the task assigned to the agent.  If none, then the agent is 'idle'
        self.timestep = 0
        self.taskCompetionTime = [] # This holds the final timer value kept within the task when the task has been completed.  Used for regret analysis
        self.failure = False

        # In order to pause our reverse search for true heuristic, we need these two member variables
        self.revFrontier = PriorityQ()  # This is used to hold the frontier of the reverse search
        self.revVisited = None          # This is used to hold the list of nodes visited for the reverse search


    def planPath(self, reserv_table, currentTime, heuristic):
        """
        Plans a path for the agent
        Maybe include a function here to remove old states from the reservation
        table associated with the old plan
        """

        try:
            self.plan, self.planCost = whca_search(self.currentState, self.task,
                                                self.task.trueHeurDrop,
                                                reserv_table, currentTime, heuristic)
        except TypeError:
            self.plan= None
            self.planCost = None
            self.failure = True
            # print('Path Planning failed for agent {}!'.format(self._id))


        # Maybe include another function to claim new states in the reservation table corresponding with the new plan

    def reserveState(self, reserv_table):
        print(len(self.path))

    def assignTask(self, newTask):
        """
        Assigns a task to the agent
        """
        self.plan = None
        self.task = newTask

    def moveAgent(self, action):
        """
        This function will help move the agent (not necessary if we are using
        states instead of actions to define plan)

        """
        if action == 'u':
            self.currentState[1] = self.currentState[1] - 1
        elif action == 'd':
            self.currentState[1] = self.currentState[1] + 1
        elif action == 'l':
            self.currentState[0] = self.currentState[0] - 1
        elif action == 'r':
            self.currentState[0] = self.currentState[0] + 1
        elif action == 'w':
            self.currentState = self.currentState # No change, this step is trivial
        else:
            return False    # If we have reached here, then return False

        return True         # If nothing went wrong, return True

    def updateCurrentState(self, reserv_table):
        """
        Moves the agent to the next state in plan and adds this state to the path
        """
        self.timestep += 1
        if _DEBUG:
            print("Agent {} current plan: {}".format(self._id, self.plan))
        try:
            if self.plan is not None:
                self.currentState = self.plan[0]
            else:
                self.currentState = (self.currentState[0], self.currentState[1], self.currentState[2]+1)
                reserv_table.resvState(self.currentState)
                self.path.append(self.currentState)
<<<<<<< HEAD
=======

>>>>>>> 1d53b3142fc6dccfefc9660bc1284819f5b4dda5
        except IndexError:
            self.currentState = self.path[-1][:2] + (self.timestep,)
        if self.plan is not None:
            self.plan = self.plan[1:]
            if len(self.plan) == 0:
                reserv_table.resvState(self.currentState)
                if _DEBUG:
                    print("Agent {} task:".format(self._id, self.task))
                if not self.isAgentIdle():
                    # If it is not an artificial task, get the timer value
                    self.task.tickTimer()
                    if str(self.task.taskId)[0] != 'a':
                        self.taskCompetionTime.append(self.task.getTimer())
                    self.task.progressStatus()
                    self.assignTask(None)
                    self.plan = None
            self.path.append(self.currentState)  # Append the step to the path

        # If the Agent is not idle, update the timer associated with the task
        if not self.isAgentIdle():
            self.task.tickTimer()

    def isAgentIdle(self):
        """
        Returns True if the agent is considered 'idle' and taskless
        """
        return self.task == None

    def isTaskComplete(self):
        """
        Returns True if the agent is done with it's task
        """
        return self.task.getTaskStatus() == "complete"

    ###############################################
    ############# Getters and Setters #############
    ###############################################

    def getPlan(self):
        return self.plan

    def getPath(self):
        return self.path
