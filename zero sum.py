from scipy.optimize import linprog
import numpy as np
import random
def solve(A):

    #Player 2 Optimal
    m = len(A) #number of rows
    n = len(A[0]) #number of cols
    c = np.zeros((n+1,1))
    c[0] = 1
    app = -np.ones((m,1))
    A_ub = np.hstack((app, A))
    b_ub = np.zeros((m,1))
    A_eq = np.ones((1,n+1))
    A_eq[0][0] = 0
    b_eq = 1
    bound_list =[(None, None)]
    for i in range(n):
        bound_list.append((0,None))
    bounds = tuple(bound_list)
   

    res = linprog(c.reshape(n+1), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,bounds= bounds, method='simplex', callback=None, options=None)
    y = res.x
    y = y[1:n+1]
    value = res.fun

    #Player 1 Optimal
    c = np.zeros((m+1,1))
    c[0] = 1
    app = -np.ones((n,1))
    A_ub = np.hstack((app, -np.transpose(A)))
    b_ub = np.zeros((n,1))
    A_eq = np.ones((1,m+1))
    A_eq[0][0] = 0
    b_eq = 1

    bound_list =[(None, None)]
    for i in range(m):
        bound_list.append((0,None))
    bounds = tuple(bound_list)
    

    res = linprog(c.reshape(m+1), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,bounds=bounds, method='simplex', callback=None, options=None)
    x = res.x
    x = x[1:m+1]
    value = -res.fun

    return  (x,y,value)


def main():
    
    A = [[1,-2,3],
    [-2,1,-1],
    [4,-4,0],
    [10,-10,1]]
    solve(A)
    
    (x,y,value) = solve(A)
    print("The value of the game is", end = " ")
    print(value)
    print("Player 1's optimal strategy is", end = " ")
    print(x)
    print("Player 2's optimal strategy is", end = " ")
    print(y)
   
if __name__ == "__main__" :
    main()
