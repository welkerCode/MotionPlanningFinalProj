import numpy as np

file_name = "rand_map.txt"
_ROW = 100
_COL = 100
grid = np.chararray((_ROW,_COL))
grid[:] = '0'


obs_percent = .3
end_percent = .3
free_percent = 1 - obs_percent - end_percent

for row in xrange(0,_ROW):
    for col in xrange(0,_COL):
        rand = np.random.choice(['0','x','e'], p=[free_percent, obs_percent, end_percent])
        grid[row][col] = rand

file = open(file_name,"w+")
for row in xrange(0,_ROW):
    row_write = []
    for col in xrange(0,_COL):
        row_write.append(grid[row][col])
    row_write.append('\n')
    row_write = ''.join(row_write)
    file.write(row_write)
file.close()

file = open("rand_map.txt","r")
obs_count = 0.
end_count = 0.
free_count = 0.
nodes = float(_ROW * _COL)
readlines = file.readlines()

for line in xrange(_ROW):
    for ch in readlines[line]:
        if ch == 'x':
            obs_count += 1
        elif ch == 'e':
            end_count += 1
        elif ch == '0':
            free_count += 1

file.close()

print('Percent Obstacles:')
print(obs_count/nodes)
print('Percent Endpoints:')
print(end_count/nodes)
print('Percent Free Nodes:')
print(free_count/nodes)



