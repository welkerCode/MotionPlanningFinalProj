'''This is the program that needs to be run to execute our simulation'''

from reserv_table import *
from env import GridMap
from global_util import genRandEndpoint
from global_util import assignTasks
from agent import Agent

'''
init env

init_agents with goals
    init all tasks
        set up heur for each task x
        assign task to closest agent
        
        for(each task)
            for(each agent)
                if agentV.currentPos < prevAgent.pos 
                    agentToAssign = agentV
            agentToAssign.task = task
            
        
init res_table(occ grid) x

set timestep to 0


    
while idle agents exists
    for agent
        if agent doesn't have plan
            if task assigned
                plan path for agent
                add path to res table 
            else task not assigned
                plan to stay put
                add path to the res table
    increment timestep
        update all agent movements
            timer updated within agent's task        
        unassign tasks if goal is reached and add to report
        
    for each agent
        agents done boolean = isAgentIdle & prev result
            If true, then all agents are now idle

'''


# test path of 4 agents, the zeros represent an agent waiting one time step

env = GridMap('env_files/env_warehouse.txt')
reserv_table = Reserv_Table(env.occupancy_grid)
global_timestep = 0
TaskIDGen = 0

### INITIALIZATION ###
agent0 = Agent(env.endpoints[0])
agent1 = Agent(env.endpoints[1])
dropoff0 = env.endpoints[-1]
dropoff1 = env.endpoints[-2]
task0 = Task(0, agent0.state, dropoff0, "dropoff")
task1 = Task(1, agent1.state, dropoff1, "dropoff")




tasks = [task0, task1]
agents = [agent0, agent1]
assignTasks(tasks, agents)
agentsDone = False


### ACTION ###
while not agentsDone:
    for agent in agents:
        if agent.getPlan is None:
            if not agent.isAgentIdle():
                agent.planPath()
                # Add path to res_table
            else:
                # plan mini path to stay put
                # Add path to res_table
    incrementTimestep()
    agentDoneCount = 0
    for agent in agents:
        if agent.isAgentIdle():
            agentDoneCount += 1
    if agentDoneCount == len(agents):
        agentsDone = True


### PRINT RESULTS ###
agentPaths = [agent.getPath() for agent in agents]

env.display_map(agentPaths)

'''
Random Pseudocode

for agent in range(2):
    genRandEndpoint(env.endpoints)
    



dropoff0 = genRandEndpoint(env.endpoints)
dropoff1 = genRandEndpoint(env.endpoints)
'''


