from PIL import Image
import gtk
import numpy as np
import itertools

width = gtk.gdk.screen_width()
height = gtk.gdk.screen_height()
matrix_size = None
boundary_cond = None
rule_set = None
M = None

# function for initializing each parameter
def initialize(size,boundary,rules,intial):
    matrix_size = size
    boundary_cond = boundary
    rule_set = rules
    M = initial

# function for computing next generation
def next_gen(size,boundary,rules,M_t):
    # check if matrix size is valid
    if size[0]<3 or size[1]<3 or size[0]>width or size[1]>height:
        raise Exception("Matrix minimum size is 3x3 and maximum size is {}x{}".format(width,height))
    N = np.zeros(size)
    M_n = np.zeros(size)
    rule = rules[1:].split('/S')
    born = [int(s) for s in rule[0]]
    occupied = [int(s) for s in rule[1]]
    cells = list(itertools.product(range(size[0]),range(size[1])))
    # check if border condition valid
    if boundary != "toroidal" and boundary != "death_edge":
        raise Exception("Boundary condition has to be either toroidal or death_edge")
    elif boundary == "toroidal":
        # calculating adjacency numbers
        for x in range(size[0]-1):
            for y in range(size[1]-1):
                N[x,y+1] += M_t[x,y]
                N[x+1,y] += M_t[x,y]
                N[x+1,y+1] += M_t[x,y]
                N[x+1,y-1] += M_t[x,y]
                N[x,y-1] += M_t[x,y]
                N[x-1,y-1] += M_t[x,y]
                N[x-1,y] += M_t[x,y]
                N[x-1,y+1] += M_t[x,y]
        # outer borders are edge cases, index out of range errors have to be prevented
        y = size[1]-1
        for x in range(size[0]-1):
            N[x,0] += M_t[x,y]
            N[x+1,y] += M_t[x,y]
            N[x+1,0] += M_t[x,y]
            N[x+1,y-1] += M_t[x,y]
            N[x,y-1] += M_t[x,y]
            N[x-1,y-1] += M_t[x,y]
            N[x-1,y] += M_t[x,y]
            N[x-1,0] += M_t[x,y]
        x = size[0]-1
        for y in range(size[1]-1):
            N[x,y+1] += M_t[x,y]
            N[0,y] += M_t[x,y]
            N[0,y+1] += M_t[x,y]
            N[0,y-1] += M_t[x,y]
            N[x,y-1] += M_t[x,y]
            N[x-1,y-1] += M_t[x,y]
            N[x-1,y] += M_t[x,y]
            N[x-1,y+1] += M_t[x,y]
        N[-2,-1] += M_t[-1,-1]
        N[-2,-2] += M_t[-1,-1]
        N[-1,-2] += M_t[-1,-1]
        N[0,-1] += M_t[-1,-1]
        N[-1,0] += M_t[-1,-1]
        N[0,0] += M_t[-1,-1]
        N[-2,0] += M_t[-1,-1]
        N[0,-2] += M_t[-1,-1]
        for x,y in cells:
            if M_t[x,y] == 0 and N[x,y] in born:
                M_n[x,y] = 1
            elif M_t[x,y] == 0:
                M_n[x,y] = 0
            else:
                if N[x,y] in occupied:
                    M_n[x,y] = 1
                else:
                    M_n[x,y] = 0
        return M_n
    # boundary == 'death edge'
    else:
        # adjacency numbers for inner cells
        for x in range(1,size[0]-1):
            for y in range(1,size[1]-1):
                N[x,y+1] += M_t[x,y]
                N[x+1,y] += M_t[x,y]
                N[x+1,y+1] += M_t[x,y]
                N[x+1,y-1] += M_t[x,y]
                N[x,y-1] += M_t[x,y]
                N[x-1,y-1] += M_t[x,y]
                N[x-1,y] += M_t[x,y]
                N[x-1,y+1] += M_t[x,y]
        # adjacency numbers for outer ring of cells
        L = [x for x in cells if x[0] == 0 or x[0] == size[0]-1 or x[1] == 0 or x[1] == size[1]-1]
        for x,y in L:
            if y+1 < size[1]:
                N[x,y+1] += M_t[x,y]
            if x+1 < size[0]:            
                N[x+1,y] += M_t[x,y]
            if x+1 < size[0] and y+1 < size[1]:
                N[x+1,y+1] += M_t[x,y]
            if x+1 < size[0] and y > 0:
                N[x+1,y-1] += M_t[x,y]
            if y > 0:
                N[x,y-1] += M_t[x,y]
            if x > 0 and y > 0: 
                N[x-1,y-1] += M_t[x,y]
            if x > 0:
                N[x-1,y] += M_t[x,y]
            if x > 0 and y+1 < size[1]:
                N[x-1,y+1] += M_t[x,y]
        for x,y in cells:
            if M_t[x,y] == 0 and N[x,y] in born:
                M_n[x,y] = 1
            elif M_t[x,y] == 0:
                M_n[x,y] = 0
            else:
                if N[x,y] in occupied:
                    M_n[x,y] = 1
                else:
                    M_n[x,y] = 0
        return M_n

# display game of life matrix as a two color picture    
def display(M_t,size):
    pic = np.zeros((size[1],size[0],3), dtype=np.uint8)
    for x,y in list(itertools.product(range(size[0]),range(size[1]))):
        if M_t[x,y] == 1:
            pic[x,y] = [0,255,0]
        else: 
            pic[x,y] = [0,0,255]
    img = Image.fromarray(pic, 'RGB')
    img.show()

# testing for display function
# M = np.random.randint(2,size =(300,300))
# matrix_size = M.shape
# display(M,matrix_size)
