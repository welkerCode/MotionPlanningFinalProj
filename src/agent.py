'''This is the file that holds the class description for the "Agent" class'''
from priorityq import *
from task import *


class Agent:

    ###############################################
    ############# Class Variables #################
    ###############################################

    # Required class variables
    currentState    # This will hold the current State (position + timeStep) that the agent is in
    task            # This will hold the task assigned to the agent, if None, then the agent isn't busy.
    trueHeur        # dictionary of nodes (key) and their true heuristic (cost/int) to the goal
    plan            # Future movement, updated by the planning algorithm
    path            # True movement of the agent, goes into the animator

    # Allows us to pause the reverse search (if desired)
    revFrontier     # PriorityQ of nodes
    revVisited      # list of nodes


    ###############################################
    ############# Class Functions #################
    ###############################################

    # The init function
    def __init__(self, initState = (0,0,0), newTask = None):
        self.plan = []  # This holds the future actions that the planning algorithm will give the agent
        self.path = []  # This holds the paths that the agent has taken thus far.
        self.trueHeur = {}  # This holds the dictionary matching a state to a true heuristic
        self.currentState = initState   # This holds the current state the agent is in
        self.path.append(self.currentState) # We need to add the initial state to our path
        self.task = newTask # This holds the task assigned to the agent.  If none, then the agent is 'idle'

        # In order to pause our reverse search for true heuristic, we need these two member variables
        self.revFrontier = PriorityQ()  # This is used to hold the frontier of the reverse search
        self.revVisited = None          # This is used to hold the list of nodes visited for the reverse search


    # This is the function that will be used to plan a path for this agent
    def planPath(self):
        # Maybe include a function here to remove old states from the reservation table associated with the old plan

        self.plan = whca_search(self.currentState, self.task, self.frontier, self.visited)
            # The task object will yield the pickup and dropoff locations

        # Maybe include another function to claim new states in the reservation table corresponding with the new plan

    # This function assigns a task to the agent
    def assignTask(self, newTask):
        self.task = newTask

    # This function will help move the agent (not necessary if we are using states instead of actions to define plan)
    def moveAgent(self, action):
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

    # This is an alternative move function that simply updates the state the agent is in while appending the new state to the path
    def updateCurrentState(self):
        self.currentState = self.plan.pop(0) # Get the next immediate step of the plan (and remove it from the plan)
        self.path.append(self.currentState)  # Append the step to the path
        if not self.isAgentIdle():
            # If the Agent is not idle, update the timer associated with the task
            self.task.tickTimer()

    # Function to see if the agent is considered 'idle' and taskless
    def isAgentIdle(self):
        if self.task == None:
            return True
        else:
            return False

    # Function to return whether the agent is done
    def isTaskComplete(self):
        taskStatus = self.task.getTaskStatus()
        if taskStatus == "complete":
            return True
        else:
            return False

    ###############################################
    ############# Getters and Setters #############
    ###############################################

    def getPlan(self):
        return self.plan
    def getPath(self):
        return self.path