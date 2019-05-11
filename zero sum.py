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
    """
    A = [[1,-2,3],
    [-2,1,-1],
    [4,-4,0],
    [10,-10,1]]
    solve(A)
    """
    n = 3

    p_junk = 0.501177
    p_pair = 0.422569
    #p_two_pair = 0.047539
    p_high = 1 - p_junk - p_pair #- p_two_pair
    p = [p_high, p_pair, p_junk]
    prob = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            prob[i,j] = p[i]*p[j]
    

    p1 = ["" for x in range(pow(3,n))]
    p2 = ["" for x in range(pow(4,n))]


    for i in range(3):
        for j in range(3):
            for k in range(3):
            
                str = ""
                if i == 0:
                    str = str + "A"
                elif i == 1:
                    str = str + "S"
                elif i == 2:
                    str = str + "P"
                if j == 0:
                    str = str + "A"
                elif j == 1:
                    str = str + "S"
                elif j == 2:
                    str = str + "P"
                if k == 0:
                    str = str + "A"
                elif k == 1:
                    str = str + "S"
                elif k == 2:
                    str = str + "P"
                p1[k + 3*j + 9*i] = str
    
    for i in range(4):
        for j in range(4):
            for k in range(4):
            
                str = ""
                if i == 0:
                    str = str + "A"
                elif i == 1:
                    str = str + "S"
                elif i == 2:
                    str = str + "C"
                elif i == 3:
                    str = str + "P"
                if j == 0:
                    str = str + "A"
                elif j == 1:
                    str = str + "S"
                elif j == 2:
                    str = str + "C"
                elif j == 3:
                    str = str + "P"
                if k == 0:
                    str = str + "A"
                elif k == 1:
                    str = str + "S"
                elif k == 2:
                    str = str + "C"
                elif k == 3:
                    str = str + "P"

                
                p2[k + 4*j + 16*i] = str
    
    A = np.zeros((pow(3,n), pow(4,n)))
    for i in range(pow(3,n)):
        for j in range(pow(4,n)):
            str1 = p1[i]
            str2 = p2[j]
            sum = 0
            for k in range(n):
                for l in range(n):
                    payoff = 0
                    # k is P1's hand strength, l is P2's
                    s1 = str1[k]
                    s2 = str2[l]
                    if (s1 == "A" and s2 == "A") or (s1 == "A" and s2 == "S") or (s1 == "S" and s2 == "A") or (s1 == "S" and s2 == "C"):
                        if k < l:
                            payoff = 2
                        elif k == l:
                            payoff = 0
                        else:
                            payoff = -2
                    elif (s1 == "S" and s2 == "S") and (s1 == "S" and s2 == "P") or (s1 == "P" and s2 == "S") or (s1 == "P" and s2 == "P"):
                        if k < l:
                            payoff = 1
                        elif k == l:
                            payoff = 0
                        else:
                            payoff = -1
                    elif (s1 == "A" and s2 == "C") or (s1 == "A" and s2 == "P"):
                        payoff = 1
                    elif (s1 == "P" and s2 == "A") or (s1 == "P" and s2 == "C"):
                        payoff = -1

                    sum = sum + prob[k,l]*payoff
            

            A[i,j] = sum
    (x,y,value) = solve(A)
    print("The value of the game is", end = " ")
    print(value)
    print("Player 1's optimal strategy is", end = " ")
    print(x)
    print("Player 2's optimal strategy is", end = " ")
    print(y)
    for i in range(pow(4,n)):
        if(y[i] > 0.001):
            print(p2[i], end = " ")
            print(y[i])
    r = random.uniform(0,1)
    k = 0
    while r > 0:
        r = r - y[k]
        k = k + 1
    
        

    
if __name__ == "__main__" :
    main()
