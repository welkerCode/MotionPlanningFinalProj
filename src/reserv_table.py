class Reserv_Table:
    '''
    The reservation table is a dictionary of dictionaries.  The outer dictionary uses x values as the key to accessing
    y values and their occupation status over time.  The inner dictionary uses the y values as the key, and they yield
    another dictionary.  This dictionary uses the timestep as the key, and the occupation status of that position at the
    desired timestep is returned
    '''

    res_table = {}

    def __init__(self, env_x=2, env_y=2, occupancyGrid = []):
        self.res_table = {}                     # Create the outer dictionary
        for i in range(0, env_x, 1):            # For all of the x's in the environment
            d = {}                              # Create a second dictionary for each y
            for j in range(0, env_y, 1):        # For all of the y's in the environment
                d[j] = {0 : occupancyGrid[2]}              # Fill the second dictionary with the third dictionary (1 = obstacle)
            self.res_table[i] = d               # Tie three dictionaries together



    # Simply prints the table.  Might be good to format for easy debugging?
    def showTable(self):
        print(self.res_table)