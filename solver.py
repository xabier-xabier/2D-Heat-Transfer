import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

    
def distance_xy(elements, nodes):
    d_xy=12000000000000000000
    
    # We will create a loop through all the elements to determine the minimum distance
    # between nodes for the fourier calculation
    for i in range (0,int(elements[0][-1]),1):
        xcoord1=nodes[1][int(elements[1][i])-1]
        ycoord1=nodes[2][int(elements[1][i])-1]
        xcoord2=nodes[1][int(elements[2][i])-1]
        ycoord2=nodes[2][int(elements[2][i])-1]
        xcoord3=nodes[1][int(elements[3][i])-1]
        ycoord3=nodes[2][int(elements[3][i])-1]
        xcoord4=nodes[1][int(elements[4][i])-1]
        ycoord4=nodes[2][int(elements[4][i])-1]
        
        
        dx12=abs(float(xcoord1)-float(xcoord2))
        dy12=abs(float(ycoord1)-float(ycoord2))
        d_12=(((dx12)**2)+((dy12)**2))**0.5
        if d_12<d_xy:
            d_xy=d_12
                
        dx14=abs(float(xcoord1)-float(xcoord4))
        dy14=abs(float(ycoord1)-float(ycoord4))
        d_14=((dx14**2)+(dy14**2))**0.5
        if d_14<d_xy:
            d_xy=d_14
            
        dx23=abs(float(xcoord2)-float(xcoord3))
        dy23=abs(float(ycoord2)-float(ycoord3))
        d_23=((dx23**2)+(dy23**2))**0.5
        if d_23<d_xy:
            d_xy=d_23
            
        dx34=abs(float(xcoord3)-float(xcoord4))
        dy34=abs(float(ycoord3)-float(ycoord4))
        d_34=((dx34**2)+(dy34**2))**0.5
        if d_34<d_xy:
            d_xy=d_34
            
    return d_xy

    
def iteration(d_xy, alpha, delta_t, nodes, loads, iterations, list_node_final):    
    fourier = alpha * delta_t / (d_xy ** 2)     
    
    if fourier >= 0.25:
        raise ValueError(f"The Fourier number is unstable, please reduce delta_t. Fourier number : {fourier}")   
    
    # Initialize the whole matrix in zeros        
    Temp=np.zeros(int(nodes[0][-1]), dtype=float)
    
    # Set the initial conditions of the problem
    for load in loads:
        Temp[int(load)-1]=100  
    
    j = 0
    for i in range(iterations):
        j += 1
        Temp_new = np.copy(Temp)  # Copia profunda para evitar referencias incorrectas
       
        for x in range(0, int(nodes[0][-1]), 1):
            if len(list_node_final[x]) == 2:
                Temp_new[x] = ((1 - (4 * fourier))*Temp[x]) + (fourier * (Temp[int(list_node_final[x][0]) - 1] + Temp[int(list_node_final[x][1]) - 1]))

            elif len(list_node_final[x]) == 3:
                Temp_new[x] = (1 - (4 * fourier))*Temp[x] + (fourier * (
                Temp[int(list_node_final[x][0]) - 1] +
                Temp[int(list_node_final[x][1]) - 1] +
                Temp[int(list_node_final[x][2]) - 1]
                ))

            elif len(list_node_final[x]) == 4:
                Temp_new[x] = (1 - (4 * fourier))*Temp[x] + (fourier * (
                Temp[int(list_node_final[x][0]) - 1] +
                Temp[int(list_node_final[x][1]) - 1] +
                Temp[int(list_node_final[x][2]) - 1] +
                Temp[int(list_node_final[x][3]) - 1]
                ))

        # Aplicar las condiciones de carga después de actualizar todos los nodos
        for load in loads:
            Temp_new[int(load) - 1] = 100
            
        Temp = np.copy(Temp_new)

    return Temp
