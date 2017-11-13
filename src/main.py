'''This is the program that needs to be run to execute our simulation'''

from reserv_table import *
from env import GridMap

gm = GridMap('env_files/env_warehouse.txt')
x = gm.cols
y = gm.rows
og = gm.occupancy_grid

rt = Reserv_Table(env_x=x, env_y=y, occupancyGrid=og)
rt.showTable()
