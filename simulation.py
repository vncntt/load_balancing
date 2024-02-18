import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import random
from collections import deque

#People don't just use perfect load balancing since keeping track of all the information
#about all the servers can also be inefficient. You have to query each server and wait for a response. 
#https://www.eecs.harvard.edu/~michaelm/postscripts/handbook2001.pdf

colors = [(0,1,0), (1,1,0), (1,0,0)]
n_bins=100
cmap = LinearSegmentedColormap.from_list("GreenYellowRed",colors,N=n_bins)


grid_size = 5 
grid1 = np.zeros((grid_size, grid_size), dtype=int)
grid2 = np.zeros((grid_size, grid_size), dtype=int)
grid3 = np.zeros((grid_size, grid_size), dtype=int)

fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(15, 5))
mat1 = ax1.matshow(grid1, cmap=cmap, vmin=1, vmax=30)
mat2 = ax2.matshow(grid2, cmap=cmap, vmin=1, vmax=30)
mat3 = ax3.matshow(grid3, cmap=cmap, vmin=1, vmax=30)

ax1.axis('off')
ax2.axis('off')
ax3.axis('off')
#plt.colorbar(mat, ax=ax, label = 'Value in grid')

ax1.set_title("Random", fontsize=14)
ax2.set_title("Minimum of Random Two", fontsize=14)
ax3.set_title("Minimum of Random Three", fontsize=14)

texts1 = [[ax1.text(j,i,str(grid1[i,j]),va='center',ha='center',color='black') for j in range(grid_size)] for i in range(grid_size)]
texts2 = [[ax2.text(j,i,str(grid2[i,j]),va='center',ha='center',color='black') for j in range(grid_size)] for i in range(grid_size)]
texts3 = [[ax3.text(j,i,str(grid3[i,j]),va='center',ha='center',color='black') for j in range(grid_size)] for i in range(grid_size)]

update_history1 = deque(maxlen=500)
update_history2 = deque(maxlen=500)
update_history3 = deque(maxlen=500)

def update(frame):
    x1,y1 = random.randint(0,grid_size-1), random.randint(0,grid_size-1)
    grid1[x1,y1]+=1
    texts1[x1][y1].set_text(grid1[x1,y1])


    x2,y2 = random.randint(0,grid_size-1), random.randint(0,grid_size-1)
    x3,y3 = random.randint(0,grid_size-1), random.randint(0,grid_size-1)
    if(grid2[x2,y2]>grid2[x3,y3]):
        x2,y2=x3,y3
    grid2[x2,y2]+=1
    texts2[x2][y2].set_text(grid1[x2,y2])

    min_val = 9999999
    chosen_x,chosen_y = -1,-1
    for _ in range(3):
        x,y = random.randint(0,grid_size-1), random.randint(0,grid_size-1)
        if(grid3[x,y]<min_val):
            chosen_x,chosen_y = x,y
            min_val = grid3[x,y]

    grid3[chosen_x,chosen_y]+=1
    texts3[chosen_x][chosen_y].set_text(grid3[chosen_x,chosen_y])



    update_history1.append((x1,y1))
    update_history2.append((x2,y2))
    update_history3.append((x3,y3))


    if len(update_history1)==500:
        old_x1,old_y1 = update_history1.popleft()
        grid1[old_x1,old_y1] -=1


    if len(update_history2)==500:
        old_x2,old_y2 = update_history2.popleft()
        grid2[old_x2,old_y2] -=1

    if len(update_history3)==500:
        old_x3,old_y3 = update_history3.popleft()
        grid3[old_x3,old_y3] -=1



    for i in range(grid_size):
        for j in range(grid_size):
            texts1[i][j].set_text(grid1[i,j])
            texts2[i][j].set_text(grid2[i,j])
            texts3[i][j].set_text(grid3[i,j])

    mat1.set_array(grid1)
    mat2.set_array(grid2)
    mat3.set_array(grid3)

    return [mat1] + [txt for row in texts1 for txt in row] + [mat2] + [txt for row in texts2 for txt in row] + [mat3] + [txt for row in texts3 for txt in row]


ani = FuncAnimation(fig, update, frames=1000, interval=33, blit = True)

#plt.show()

ani.save('grid_animation_20s.gif', writer='pillow', fps=30)


