import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import prepare_mesh
import matplotlib.tri as tri
import solver


# Read the data from the Femap file output for the Mesh
prepare_mesh.create_element()
prepare_mesh.create_node()
prepare_mesh.create_loads()


#Store the data of the elements, nodes, 
# loads and restrictions into variables
nodes=prepare_mesh.node_variables()                 # Info por the loads, ID, Xcoord, Ycoord, DOF
elements=prepare_mesh.element_variables()           # Info for the Elements, ID, node1, node2, node3, node4 
loads=prepare_mesh.node_loads()                     # Info for the node IDs for the loads

list_node_f=[]
for i in range (0, int((nodes[0][-1])), 1):
    list_node_f.append([])

for i in range (0, int((elements[0][-1])), 1):
    list_node_f[int(elements[1][i])-1].append(int(elements[2][i]))                       # Node 1 (1,2)
    list_node_f[int(elements[1][i])-1].append(int(elements[4][i]))                       # Node 1 (1,4)
    list_node_f[int(elements[2][i])-1].append(int(elements[1][i]))                       # Node 2 (2,1)
    list_node_f[int(elements[2][i])-1].append(int(elements[3][i]))                       # Node 2 (2,3)
    list_node_f[int(elements[3][i])-1].append(int(elements[2][i]))                       # Node 3 (3,2)
    list_node_f[int(elements[3][i])-1].append(int(elements[4][i]))                       # Node 3 (3,4)
    list_node_f[int(elements[4][i])-1].append(int(elements[3][i]))                       # Node 4 (4,3)
    list_node_f[int(elements[4][i])-1].append(int(elements[1][i]))                       # Node 4 (4,1)
    


# Create a final array with no repeated node values
# This will be three nodes connected to each node for the iteration
list_node_final=[]
for i in range (0,int(nodes[0][-1]), 1):
    new=list(set(list_node_f[i]))
    list_node_final.append(new)
    
distancia=solver.distance_xy(elements,nodes)
print(distancia)

solucion =solver.iteration1(distancia, 0.1, 0.001, nodes, loads, 5000, list_node_final)
print(solucion)



##################################################################################################################################
#----------------------------------------------- PLOT AREA ----------------------------------------------------------------------#
##################################################################################################################################

initial=[]

for i in range (0, int(nodes[0][-1]), 1):
    initial.append(np.array([float(nodes[1][i]), float(nodes[2][i])]))


lines=[]

for i in range (0,int(elements[0][-1]),1):
    lines.append([int(elements[1][i])-1, int(elements[2][i])-1])
    lines.append([int(elements[1][i])-1, int(elements[4][i])-1])
    lines.append([int(elements[3][i])-1, int(elements[2][i])-1])
    lines.append([int(elements[4][i])-1, int(elements[1][i])-1])
    lines.append([int(elements[3][i])-1, int(elements[4][i])-1])
    


triang=[]
for i in range (0,int(elements[0][-1]),1):
    triang.append([int(elements[1][i])-1, int(elements[2][i])-1, int(elements[3][i])-1])
    triang.append([int(elements[1][i])-1, int(elements[3][i])-1, int(elements[4][i])-1])

triangles=np.array(triang)

init=np.array(initial)
triang = tri.Triangulation(init[:, 0], init[:, 1], triangles)

plt.figure(figsize=(9, 4.5))
plt.axis('equal')
plt.axis('off')

temp_final=np.array(solucion)
# Plot contour of stress values on the deformed mesh
contour = plt.tricontourf(triang, temp_final, levels=20, cmap='plasma', interpolation='bilinear', origin='lower')

# Plot temperature in the mesh
for line in lines:
    x_vals = [init[line[0], 0], init[line[1], 0]]
    y_vals = [init[line[0], 1], init[line[1], 1]]
    plt.plot(x_vals, y_vals, 'k-', linewidth=0.8)  # Black lines for mesh

# Add color bar for temperature values
cbar = plt.colorbar(contour)
cbar.set_label("Temperature on the plate")

plt.title("Contour Map of Temperature")
plt.show()