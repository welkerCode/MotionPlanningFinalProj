'''This is the file that holds the class description for the "Agent" class'''

class Agent:

    '''
    These are the class members
    '''
    token           # This will hold the token if the agent has it.  Otherwise, it will hold "None"
    busy            # This will act as a boolean to declare whether or not the agent has a job already
    path            # This should be a list of actions + states that define the path that the agent will take
    currentState    # This will hold the current State (position + timeStep) that the agent is in
    task


    def __init__(self, initState = (0,0,0)):
        token = None
        busy = False
        path = []
        currentState = initState

    # This function is used to pass the token to a new agent
    def passToken(self):
        '''

        :return:

        Proposed Actions
        1. Get the list of agents
        2. Give token to the next agent in the list
        3. Remove token from class members in this agent

        '''

        return None

    def requestToke(self):
        # Do something

    def receiveToken(self, newToken):
        '''

        :return:

        Proposed Action
        1. If this method is called, then we need to
        '''

    # This is the function that will be used to find a path for this agent
    def choosePath(self):
        '''

        :return: Probably should return a new Path variable that can go in the "path" member of this class

        Proposed Actions
        1. Call the token's method to get a path?

        '''
        return None

    # This function will help move the agent
    def moveAgent(self, action):
        '''

        :param action: this is determined by the path, and is used to calculate the new state
        :return: Not sure if we should return anything...maybe a boolean to signal whether or not we were successful?

        Proposed Actions
        1. Use action to calculate new state
        2. Check if in collision?
        3. Update currentState variable
        4. Update path?
        5. Return boolean signaling success?
        '''


        return None


'''
Agent passes token to path-planning algorithm (acts as a key, and holds other paths for collision checking).

'''
