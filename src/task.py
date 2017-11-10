class Task:

    ###############################################
    ############# Class Variables #################
    ###############################################

    taskId          # This is a unique identifier that differentiates this task from the others (int value)
    pickupState     # This holds the state at which the pickup must occur (2D)
    dropoffState    # This holds the state at which the dropoff must occur (2D)
    taskStatus      # This holds the status of the task (one of 3 strings: 'pickup', 'dropoff', 'complete')
    timer           # This holds the number of time steps used to complete the task thus far (int value)

    ###############################################
    ############# Class Functions #################
    ###############################################

    # Initialization function
    def __init__(self, newId, newPickupState=None, newDropoffState=None, newTaskStatus = "dropoff"):
        self.taskId = newId                 # Get the id of the task
        self.pickupState = newPickupState   # Get the pickup location
        self.dropoffState = newDropoffState # Get the dropoff location
        self.taskStatus = newTaskStatus     # Get the predefined status of the task (start at dropoff if agent is already at pickup location)
        self.timer = 0                      # Start the timer

    # This function progresses the status of the task by one step
    def progressStatus(self):
        if self.taskStatus == "pickup":
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