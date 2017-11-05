'''This is the class description for the "Token" class'''

class Token:

    def __init__(self):

        self.timestep
        self.listOfPlans
        self.listOfAgents   # Might not be necessary?

    def getPlan(self, agent, listOfAgents, pickupLoc, dropoffLoc):
        '''

        :param agent:
        :param listOfAgents:
        :param pickupLoc:
        :param dropoffLoc:
        :return:

        Proposed Action
        1. Draft a plan for the new agent
        2. Check plan against list of other plans, looking for collisions
        3. If collision, then replan with new action at state before collision
        4. Return final path

        '''

        return None


    '''
    Subroutine to perform an AStar (variant) seach
    Update timesteps after agents no longer request token
    Every free agent wants to "request" the task
    Every time step involves checking requests for each agent making them. (if no more tasks, this is quick)
    At each time steps positions update, plans, and states (if done with their task)
    While loop (while agent needs a token) w/in "main" function
    '''
