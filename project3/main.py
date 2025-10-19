import os
import csp
from csp import *
import sys
import  time
import random
import threading

weight= {}      #dom_wdeg_heuristic
conf_set = {}   #fc-cbj
order = {}      #fc-cbj

    

#FUNCTIONS THAT I CREATED 
#------------------------------------------------------------------------------------------------------------


def timeout_handler():
    print("TIMEOUT EXECUTED")
    os._exit(1)  #forcefully exit the entire program

class RFLAP(CSP):
    def __init__(self, instance_id):
        self.CSPVariables = []#list of variables
        self.CSPDomains = {}#dictionary of domains
        self.CSPNeighbors = {}#dictionary of neighbors
        self.CSPConstraints = {}#dictionary of constraints
        self.constraintsChecked = 0#counter for constraint checks

        self.rflap_parse(instance_id)#parse the instance

        CSP.__init__(self,self.CSPVariables, self.CSPDomains, self.CSPNeighbors, self.rflap_constraint)#initialize CSP

    def rflap_constraint(self, A, a, B, b):#constraint function
        self.constraintsChecked += 1#increment constraint checks
        pair = self.CSPConstraints[(A, B)]#get constraint pair
        op = pair[0]
        k = pair[1]
        if op == 0:
            if abs(a - b) == k:
                return True
            
        if op == 1:
            if abs(a - b) > k:
                return True
        return False
            


    def rflap_parse(self, instance_id):
        #constructing file paths for variables, domains, and constraints
        var_file_path = rf'path-to-rlfap\var{instance_id}.txt'
        dom_file_path = rf'path-to-rlfap\dom{instance_id}.txt'
        ctr_file_path = rf'path-to-rlfap\ctr{instance_id}.txt'

        #reading and parsing variable information
        variables = []
        with open(var_file_path) as f:
            h = [int(x) for x in next(f).split()]#header
            for line in f:
                variables.append([int(var_id) for var_id in line.split()])

        #reading and parsing domain information
        domains = []
        with open(dom_file_path) as f:
            h = [int(x) for x in next(f).split()]#header
            for line in f:
                domains.append([int(val) for val in line.split()[2:]])

        #initializing neighbors for each variable
        for v in range(len(variables)):
            self.CSPNeighbors[v] = []

        #reading and parsing constraint information
        with open(ctr_file_path) as f:
            h = [int(x) for x in next(f).split()]#header
            for line in f:#for each constraint
                line = line[:-1]
                parts = line.split()
                var1_id = int(parts[0])
                var2_id = int(parts[1])
                operation = parts[2]
                value = int(parts[3])

                #converting the operation to an opcode (0 for "=" and 1 for ">")
                operation_code = 0 if operation == "=" else 1

                #populate CSP data structures with constraint information
                self.CSPConstraints[(var1_id, var2_id)] = (operation_code, value)
                self.CSPConstraints[(var2_id, var1_id)] = (operation_code, value)
                self.CSPNeighbors[var1_id].append(var2_id)
                self.CSPNeighbors[var2_id].append(var1_id)

        # Populate CSPVariables and CSPDomains with parsed variable and domain information
        self.CSPVariables = [var[0] for var in variables]
        for var in variables:
            self.CSPDomains[var[0]] = domains[var[1]]


        
def dom_wdeg_heuristic(assignment, csp):# dom/wdeg heuristic
    """ dom/wdeg heuristic."""
    wdeg = {}
    minVal = float('inf')
    bestVar = 0
    for var in csp.variables:# for each variable
        wdeg[var] = 1
        if var in assignment:# if variable is assigned continue
            continue
        for y in csp.neighbors[var]:# for each neighbor of variable
            wdeg[var] += weight[(var, y)]
        if csp.curr_domains:# if curr_domains is not empty
            domX = csp.curr_domains[var]
        else:
            domX = csp.domains[var]# else use domains
        ratio = len(domX) / wdeg[var]
        if ratio < minVal:
            minVal = ratio
            bestVar = var
    return bestVar

def fc_cbj(assignment, csp, select_unassigned_variable, order_domain_values, inference):#fc-cbj function
    visited = set()
    counter = 1

    def inner_fc_cbj(assignment):#inner function
        nonlocal counter
        if len(assignment) == len(csp.variables):# if assignment is complete return assignment
            return assignment, None
        var = select_unassigned_variable(assignment, csp)# select unassigned variable
        order[var] = counter
        counter += 1
        for value in order_domain_values(var, assignment, csp):# for each value in order_domain_values
            if csp.nconflicts(var, value, assignment) == 0:
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):# if inference is true
                    result, h = inner_fc_cbj(assignment)# call inner_fc_cbj
                    if result is not None:
                        return result, None
                    elif var in visited and var != h:# if var is in visited and var is not h
                        conf_set[var].clear()
                        visited.discard(var)# remove var from visited
                        csp.restore(removals)
                        csp.unassign(var, assignment)# unassign var
                        return None, h
                csp.restore(removals)# restore removals
        csp.unassign(var, assignment)# unassign var
        visited.add(var)
        h = None
        maxi = 0
        if len(conf_set[var]):
            for c in conf_set[var]:
                if order[c] > maxi:
                    maxi = order[c]
                    h = c
            conf_set[h].update(conf_set[var])
            conf_set[h].discard(h)
        return None, h

    result, h = inner_fc_cbj({})
    assert result is None or csp.goal_test(result)# assert result is None or csp.goal_test(result)
    return result, h


def hybrid(csp, select_unassigned_variable=csp.first_unassigned_variable,#hybrid function
           order_domain_values=csp.unordered_domain_values, inference=forward_checking):#hybrid function
    return fc_cbj({}, csp, select_unassigned_variable, order_domain_values, inference)

#Functions from csp.py that i modified
#------------------------------------------------------------------------------------------------------------
def forward_checking_2(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                conf_set[B].add(var)    
                weight[(var, B)] += 1
                weight[(B, var)] += 1
                return False
    return True






def AC3_check(csp, queue=None, removals=None, arc_heuristic=csp.dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                weight[(Xi, Xj)] += 1
                weight[(Xj, Xi)] += 1
                return False,checks# CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True,checks# CSP is satisfiable

def mac_2(csp, var, value, assignment, removals, constraint_propagation=AC3_check):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)


def revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True
    if not csp.curr_domains[Xi]: # if dom(X) emptied
        weight[(Xi, Xj)] += 1
        weight[(Xj, Xi)] += 1
    return revised, checks


def min_conflicts(csp, max_steps=100000):
    """Solve a CSP by stochastic Hill Climbing on the number of conflicts."""
    # Generate a complete assignment for all variables (probably with conflicts)
    csp.current = current = {}
    ans = 0
    for var in csp.variables:
        val = csp.min_conflicts_value(csp, var, current) 
        csp.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current
        if i == max_steps-1:     
            ans = len(conflicted) 
        var = random.choice(conflicted)
        val = csp.min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    print("Constraints violated: %d" % ans)
    return None

#------------------------------------------------------------------------------------------------------------


#MAIN function everything runs on 
#EXAMPLE
#If you want to run 2-f24 for FC-CBJ you run :
#python main.py 2-f24  FC-CBJ
def main():
    args = list(sys.argv)# get command line arguments

    if len(args) != 3:
        exit('Invalid number of arguments.')

    instance = args[1]# get instance
    method = args[2]# get method
    rlfap= RFLAP(instance)  # Construct the RLFA CSP problem


    print("Problem Information:")
    print(f"  Variables: {rlfap.CSPVariables}")
    print(f"  Domains: {rlfap.CSPDomains}")
    print(f"  Neighbors: {rlfap.CSPNeighbors}\n")

    for constr in rlfap.CSPConstraints:# initialize weights
        weight[constr] = 1

    for var in rlfap.variables:# initialize conf_set and order
        conf_set[var] = set()
        order[var] = 0

    tic = time.perf_counter()# start timer
    timeout_threading = threading.Timer(500, timeout_handler)  #Using threading i set a 500 sec timer as said in the lecture 
    try:
        timeout_threading.start()

        if method == "FC":
            try:
                print(f"Solving instance using {method} + dom/wdeg heuristic\n")
                Solution = backtracking_search(rlfap, select_unassigned_variable=dom_wdeg_heuristic, order_domain_values=csp.unordered_domain_values, inference=forward_checking_2)
            finally:# if timeout occurs cancel the timer ,using finally so when the solution print the corrent answer and not an error it cancels the timer
                timeout_threading.cancel()
        elif method == "MAC":
            try:
                print(f"Solving instance using {method} + dom/wdeg heuristic\n")
                Solution = csp.backtracking_search(rlfap, select_unassigned_variable=dom_wdeg_heuristic, order_domain_values=csp.unordered_domain_values, inference=mac_2)
            finally:
                timeout_threading.cancel()# if timeout occurs cancel the timer ,using finally so when the solution print the corrent answer and not an error it cancels the timer
        elif method == "FC-CBJ":
            try:
                print(f"Solving instance using {method} + dom/wdeg heuristic\n")
                Solution = hybrid(rlfap, select_unassigned_variable=dom_wdeg_heuristic, order_domain_values=csp.unordered_domain_values, inference=forward_checking_2)
            finally:
                timeout_threading.cancel()# if timeout occurs cancel the timer ,using finally so when the solution print the corrent answer and not an error it cancels the timer
        elif method == "Min-Conflicts":
            try:
                print(f"Solving instance using {method}\n")
                Solution = min_conflicts(rlfap)# if timeout occurs cancel the timer ,using finally so when the solution print the corrent answer and not an error it cancels the timer
            finally:
                timeout_threading.cancel()# if timeout occurs cancel the timer ,using finally so when the solution print the corrent answer and not an error it cancels the timer
        else:
            exit(f'Invalid method: {method} , please use FC, MAC, FC-CBJ or Min-Conflicts.')
            timeout_threading.cancel()# if timeout occurs cancel the timer ,using finally so when the solution print the corrent answer and not an error it cancels the timer

        toc = time.perf_counter()
    except:
        timeout_threading.cancel()# if timeout occurs cancel the timer ,using finally so when the solution print the corrent answer and not an error it cancels the timer
    toc = time.perf_counter()    
    elapsed_time = toc - tic

    print("\nSolution:")
    if Solution is None:
        print(" None")
    else:
        print(f" {Solution}")
    print(f"Instance: {instance}")
    print(f"Method: {method}\n")

    print(f"\nStatistics:")
    print(f"  Assignments: {rlfap.nassigns}")
    print(f"  Constraint checks: {rlfap.constraintsChecked}")
    print(f"  Time: {elapsed_time:0.4f} seconds")

if __name__ == "__main__":
    main()

