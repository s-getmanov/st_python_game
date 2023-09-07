from random import randint as rand

def randbool(x):
    r = rand(0,100)
    return (r <= x)

def rand_cell(h, w):
    return(rand(0, h-1), rand(0,w-1))

def rand01():
    r = rand(0,100)
    if r <= 50:
        return 0
    else:
        return 1
    
def rand_101():
    r = rand(0,100)
    if r <= 33:
        return 0
    elif r <= 66:
        return 1
    else:
        return -1
    
def randtree(legend):
    r = rand(1,3)
    if r == 1:
        return legend.tree1
    elif r == 2:
        return legend.tree2
    elif r == 3:
        return legend.tree3
    return legend.tree1 

