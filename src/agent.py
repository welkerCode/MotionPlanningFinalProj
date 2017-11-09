'''This is the file that holds the class description for the "Agent" class'''

class Agent:

    '''
    These are the class members
    Agent
    -task: holds the task assigned to the agent.  If task is "None", then the agent is not busy
    -currentState: holds the state the agent is in with regards to position

    -A function to request the token (called if not busy)
    -A function to pass the token to the next agent if it is done with planning
    -A function that calls the AStar Planner.  Must pass in token in order to get a valid plan.
    -A function to update the agent's current position upon moving at a timestep
    -

    '''
    currentState    # This will hold the current State (position + timeStep) that the agent is in
    task            # This will hold the task assigned to the agent, if None, then the agent isn't busy.

    # Allows us to pause the reverse search
    revFrontier     # queue of nodes
    revVisited      # list of nodes

    trueHeur        # dictionary of nodes (key) and their true heuristic (cost/int) to the goal
    plan            # Future movement, updated by the planning algorithm
    path            # True movement of the agent, goes into the animator

    def __init__(self, initState = (0,0,0)):
        self.plan = []
        self.path = []
        self.trueHeur = {}
        self.currentState = initState

        self.revFrontier = None
        self.revVisited = None

        self.task = None

    # This is the function that will be used to plan a path for this agent
    def planPath(self):
        self.plan = whca_search(self.task, self.frontier, self.visited, self.currentState)

    # This is the function that will be used to get the path planned by the planner
    def getPlan(self):
        return self.plan

    # This function will help move the agent
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

    # This is an alternative move function that simply updates the state
    def updateCurrentState(self):
        self.path.append(self.currentState)
        self.currentState = self.plan.pop(0)
        return True

    # Function to return whether the agent is done