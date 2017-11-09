class Task:
    
    # Class variables
    # State: (x_loc, y_loc)

    pickupState     # This holds the state at which the pickup must occur
    dropoffState    # This holds the state at which the dropoff must occur
    taskStatus      # This holds the status of the task

    # Initialization function
    def __init__(self, newPickupState=None, newDropoffState=None):
        self.pickupState = newPickupState
        self.dropoffState = newDropoffState
        self.taskStatus = "pickup"

    # Return the state holding the pickup location
    def getPickup(self):
        return self.pickupState

    # Set the pickup location
    def setPickup(self, newPickupState):
        self.pickupState = newPickupState

    # Return the state holding the dropoff location
    def getDropoff(self):
        return self.dropoffState

    # Set the dropoff location
    def setDropoff(self, newDropoffState):
        self.dropoffState = newDropoffState

    # This function progresses the status of the task by one step
    def progressStatus(self):
        if self.taskStatus == "pickup":
            self.taskStatus = "dropoff"
        elif self.taskStatus == "dropoff":
            self.taskStatus = "complete"
        else:
            self.taskStatus = "error"

    # This function returns the status of the task
    def getTaskStatus(self):
        return self.taskStatus