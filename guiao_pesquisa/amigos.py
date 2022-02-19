from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

def amigos_constraint(a1,t1,a2,t2):
    c1, b1 = t1
    c2, b2 = t2
    
    if b1 == b2 or c1 == c2:
        return False
    
    if b1 == c1 or  b2 == c2:
        return False
    
    if c1 == "Claudio" and b1 != "Bernardo":
        return False
    
    if c2 == "Claudio" and b2 != "Bernardo":
        return False
    
    return True

def make_constraint_graph():
    return { (X,Y):amigos_constraint for X in amigos for Y in amigos if X!=Y }
    

def make_domains():
    print({ amigo :[(chapeu, bicicleta)] for chapeu in amigos for bicicleta in amigos for amigo in amigos })
    return { amigo :[(chapeu, bicicleta)] for chapeu in amigos for bicicleta in amigos for amigo in amigos}

cs = ConstraintSearch(make_domains(), make_constraint_graph())

print(cs.search())
