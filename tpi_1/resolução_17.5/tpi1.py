# TP1
# João António Assis Reis
# 98747
#
# Colleagues with whom I discussed this assigment
# Alexandre Serras, 
#

from tree_search import *
from cidades import *
import random

class MyNode(SearchNode):
    def __init__(self,state,parent,arg3=None,arg4=None,arg5=None):
        super().__init__(state,parent)
        self.cost = arg3
        self.heuristic = arg4
        self.eval = arg5

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',seed=0): 
        super().__init__(problem,strategy,seed)

        self.problem = problem

        self.initial_state = problem.initial
        root_heuristic = self.problem.domain.heuristic(self.initial_state, self.problem.goal)
        root_cost = 0
        root_eval = round(root_heuristic + root_cost)
        root = MyNode(self.initial_state, None, root_cost, root_heuristic, root_eval)

        self.all_nodes = [root]
        self.solution = None
        self.open_nodes = [0]
        self.curr_pseudo_rand_number = seed 

        self.all_states = {}
        self.all_states[root] = problem.initial

        self.solution_tree = None

    def astar_add_to_open(self,lnewnodes):
        self.open_nodes += lnewnodes
        self.open_nodes.sort(key=lambda pos_node: self.all_nodes[pos_node].heuristic + self.all_nodes[pos_node].cost)

    def propagate_eval_upwards(self,node):

        if node.parent is None: # se o node for a root
            return
    
        lst = []
        for n in self.all_nodes:
            if n.parent == node.parent:
                lst.append(n)

        lst.sort(key=lambda node: node.eval) # ordenar a lista por menor eval
        lowest_eval = lst[0].eval

        parent = self.all_nodes[node.parent]
        parent.eval = lowest_eval
        self.propagate_eval_upwards(parent)


    def search2(self,atmostonce=False):

        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]

            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1

                return self.get_path(node)

            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)

                newnode_cost =  node.cost + self.problem.domain.cost(node.state, (node.state, newstate))
                newnode_heuristic = self.problem.domain.heuristic(newstate, self.problem.goal)
                newnode_eval = round(newnode_cost + newnode_heuristic)
                newnode = MyNode(newstate, nodeID, newnode_cost, newnode_heuristic, newnode_eval)

                if not atmostonce:
                    if newstate not in self.get_path(node):
        
                        self.all_nodes.append(newnode)
                        lnewnodes.append(len(self.all_nodes)-1)

                        self.propagate_eval_upwards( newnode )

                else: # graph search

                    if newstate in self.all_states.values():

                        for no, state in self.all_states.items():
                            if state == newstate: old_node = no

                        if old_node.eval > newnode.eval:
                            for n in self.open_nodes:
                                if self.all_nodes[n] == old_node:
                                    self.open_nodes.remove(n)

                            self.all_states[newnode] = newstate

                            self.all_nodes.append(newnode)
                            lnewnodes.append(len(self.all_nodes)-1)

                            self.propagate_eval_upwards( newnode )

                    else:
                        self.all_states[newnode] = newstate

                        self.all_nodes.append(newnode)
                        lnewnodes.append(len(self.all_nodes)-1)

                        self.propagate_eval_upwards( newnode )
                        
            self.add_to_open(lnewnodes)

        return None

    def repeated_random_depth(self,maxattempts=3,atmostonce=False):
        tree_min_cost = None    # tree a retornar, ou seja, a com menor custo
        tree_path = None        # caminho da melhor tree

        for x in range(maxattempts):
            t = MyTree(self.problem, 'rand_depth', x)
            path = t.search2()
            if tree_min_cost:
                if t.solution.cost < tree_min_cost.solution.cost:
                    tree_path = path
                    tree_min_cost = t
            else:
                tree_path = path
                tree_min_cost = t

        self.solution_tree = tree_min_cost
        return tree_path

    def make_shortcuts(self):
        path = self.get_path(self.solution)

        connections = []
        for city in path:
            connections += self.problem.domain.actions(city)

        self.used_shortcuts = []

        for x in range(len(path)-2):
            for y in range(x+2,len(path)):
                conn = (path[x], path[y]) 
                if conn in connections:
                    path = path[:x+1] + path[y:]
                    x = y + 1
                    self.used_shortcuts.append(conn)
                    break

        return path
        



class MyCities(Cidades):

    def maximum_tree_size(self,depth):   # assuming there is no loop prevention
        total = 0
        for city in self.coordinates.keys():
            total += len(self.actions(city))

        # (avg_branch**(depth+1)-1)/(avg_branch-1)
        avg_branch = total/len(self.coordinates)
        return (avg_branch**(depth+1)-1) / (avg_branch-1)
        


