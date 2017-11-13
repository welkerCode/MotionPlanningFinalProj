class SearchNode:
    def __init__(self, s, A, parent=None, parent_action=None, cost=0, depth=0):
        '''
        s - the state defining the search node
        A - list of actions
        parent - the parent search node
        parent_action - the action taken from parent to get to s
        '''
        self.parent = parent
        self.cost = cost
        self.parent_action = parent_action
        self.state = s[:]
        self.actions = A[:]
        self.depth = depth

    def __str_full__(self):
        return str(self.state) + ' ' + str(self.actions)+' '+str(self.parent)+' '+str(self.parent_action)
    def __str__(self):
        return str(self.state) + ' ' + str(self.cost)
