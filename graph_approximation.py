import math

from linear_system_of_equation_solver import gauss_jordan_elimination

x_list = [-1, -0.5, 0, 0.5]
fx_list = [ 0.86199480, 0.95802009, 1.0986123, 1.2943767]
value_set:set = set()
printout = False

#############################################################################################
#Actual curve
def actual(x):
    if printout: print("Actual value: ")
    f_x = math.log((math.e**x)+2)
    if printout: print(f"f({x}) = {f_x}\n")
    return f_x

#############################################################################################
#Lagrange Interpolating Polynomial - Generalized
def lagrange_interpolating_polynomial(approx_x):
    n = len(x_list)
    p_x = 0
    if printout: print(f"1.1 a) Lagrange interpolating polynomial of degree {n-1}")

    #P(x) sum 
    for j in range(n):  
 
        #Pj(x) product
        product = 1
        for k in range(n):
            if j == k : continue
            product *= (approx_x-x_list[k])/(x_list[j]-x_list[k])
        product *= fx_list[j]
        if printout: print(f"P{j+1}({approx_x}) = {product}")

        p_x += product

    if printout: print(f"P({approx_x}) = {p_x}\n")
    return p_x

#############################################################################################
#Used for Newtons Divided Difference Formula
def divided_difference(list_x, list_y):
    if len(list_x) == 2:
        value = (list_y[1]-list_y[0])/(list_x[1]-list_x[0])
    else: 
        value = (
            (divided_difference(list_x[1:], list_y[1:])
            -divided_difference(list_x[:-1], list_y[:-1]))/

            (list_x[-1]-list_x[0])
        )

    global value_set
    value_set.add(f"f{list_x} = {value}")
    return value

#Newtons Divided Difference Formula - Generalized
def newtons_divided_difference_formula(approx_x):
    if printout: print(f"1.1 b) Newtons divided difference formula of degree {len(x_list)-1}")
    p_x = fx_list[0]

    for n in range(1, len(fx_list)):


        #(x-x0)(x-x1)...(x-xn)
        product = 1
        for i in range(n):
            product *= (approx_x - x_list[i])
        
        # f[x1, x0] + f[x2, x1, x0] + ... + f[xn, ... x0] 
        # though each f[] is multiplied by the respective product
        p_x += product * divided_difference(x_list[:n+1],fx_list[:n+1])


    #printing out the divided differences
    global value_set
    value_set = list(value_set)
    value_set.sort(key = lambda a: len(a))
    if printout: print("Table of results:")
    if printout: print(*value_set, sep="\n")
    value_set = set()


    if printout: print(f"P({approx_x}) = {p_x}\n")
    return p_x

#############################################################################################
#Just gets the first one - fine for my use case
def get_roots(x):
    a = -x_list[0]+3*x_list[1]-3*x_list[2]+x_list[3]
    b = 3*x_list[0] - 6*x_list[1] + 6*x_list[2]
    c = -3*x_list[0] + 3*x_list[1]
    d = x_list[0]-x

    if a == 0 and b == 0 and c == 0:
        t = -d
        if printout: print(f"t at {x} = {t}")
        return t


    if a == 0 and b == 0:
        t = -d/c
        if printout: print(f"t at {x} = {t}")
        return t


    if a == 0: 
        a,b,c = b,c,d
        t = (-b + (b**2-4*a*c)**(1/2))/(2*a)
        if printout: print(f"t at {x} = {t}")
        return t


    del0 = b**2-3*a*c
    del1 = 2*b**3-9*a*b*c+27*a**2*d


    C = ((del1 - (del1**2-4*del0**3)**(1/2))/2)**(1/3)

    if C == 0:
        t = (-1/(3*a)*(b))
    else:
        C *= ((-1+(-3)**(1/2))/2)**0
        t = (-1/(3*a)*(b + C + del0/C))

    if printout: print(f"t at {x} = {t}")
    return t

#Cubic Bezier Curve 
#  General Formula was a lot to implement when considering
#  I want to find a t that gives me x = 0.25 - which involves solving a nth-degree polynomial
def bezier_point(approx_x):  
    control_points = list(map(lambda a, b : (a,b), x_list, fx_list))

    if printout: print(f"1.1 c) Bezier point from control points: {control_points}")  
    t = get_roots(approx_x)

    x = (
            (1 - t)**3*control_points[0][0] 
            + 3*(1 -  t)**2*t*control_points[1][0] 
            + 3*(1 -  t)*t**2*control_points[2][0] 
            + t**3*control_points[3][0]
        )

    y = (
            (1 - t)**3*control_points[0][1] 
            + 3*(1 -  t)**2*t*control_points[1][1] 
            + 3*(1 -  t)*t**2*control_points[2][1] 
            + t**3*control_points[3][1]
        )   
    
    if printout: print(f"B({t}) = {(x,y)}\n")
    return (x,y)

def bezier_point_y_only(approx_x):  
    control_points = list(map(lambda a, b : (a,b), x_list, fx_list))

    if printout: print(f"1.1 c) Bezier point from control points: {control_points}")  
    t = get_roots(approx_x)

    y = (
            (1 - t)**3*control_points[0][1] 
            + 3*(1 -  t)**2*t*control_points[1][1] 
            + 3*(1 -  t)*t**2*control_points[2][1] 
            + t**3*control_points[3][1]
        )   
    

    if printout: print(f"B({approx_x}) = {y}\n")
    return y

#############################################################################################
#Used just for the 1st degree polynomial
def linear_least_squares_polynomial(approx_x):
    if printout: print("2.1) Linear Least Squares Polynomial")
    n = len(x_list)
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_xx = 0
    for i in range(n):
        sum_xy += x_list[i]*fx_list[i]
        sum_x +=  x_list[i]
        sum_y +=  fx_list[i]
        sum_xx +=  x_list[i]**2
    if printout:
        print(f"sum of x*y = {sum_xy}" )
        print(f"sum of x = {sum_x}" )
        print(f"sum of y = {sum_y}" )
        print(f"sum of x*x = {sum_xx}" )


    m = (n*sum_xy-sum_x*sum_y)/(n*sum_xx - sum_x**2)
    c = (sum_y-m*sum_x)/n
    if printout:
        print(f"y = {m}x + {c}")
        print(f"y({approx_x}) = {m*approx_x+c}\n")

    return m*approx_x+c

#############################################################################################
#This has been made to work with any size polynomial
def least_squares_polynomial(approx_x):
    sum_left = list()
    n = 2
    m = len(x_list)

    if printout: print(f"2.2) Least squares polynomial of degree {n}")

    matrix = list()        
    #generate set of equations
    for j in range(n+1):
        eq = list()
        
    
        for k in range(n+1):
            sum = 0

            for i in range(m):
                sum += x_list[i]**(k+j)
            eq += [sum]

        sum = 0    

        for i in range(m):
            sum += fx_list[i]*x_list[i]**(j)
        

        eq += [sum]
        matrix += [eq]

    if printout:
        print("System of equations (Unsolved):")
        for row in matrix:
            for col in range(m):
                if col < m-2:
                    print(f"{row[col]}(a{col})", end = " + ")
                if col == m-2:
                    print(f"{row[col]}(a{col})", end = " = ")
                if col == m-1:
                    print(f"{row[col]}")
    #solve set of equations
    gauss_jordan_elimination(matrix)
    if printout:
        print("System of equations (Solved):")
        for row in matrix:
            for col in range(m):
                if col < m-2:
                    print(f"{row[col]}(a{col})", end = " + ")
                if col == m-2:
                    print(f"{row[col]}(a{col})", end = " = ")
                if col == m-1:
                    print(f"{row[col]}")
        print("Therefore:")

        for row in range(n+1):
            print(f"a({row}) = {matrix[row][m-1]}")

    P_x = 0
    for row in range(n+1):
        P_x += matrix[row][m-1]*approx_x**row

    if printout:
        print(f"P({approx_x}) = {P_x}\n")

    return P_x

#############################################################################################
# Simplified the matrices before implementation
def least_squares_exponential_form(approx_x):
    if printout: print("2.3) Exponential Least Squares Polynomial")
    
    #generate set of equations
    n = len(x_list)
    sum_xlny = 0
    sum_x = 0
    sum_lny = 0
    sum_xx = 0
    for i in range(n):
        sum_xlny += x_list[i]*math.log(fx_list[i])
        sum_x +=  x_list[i]
        sum_lny +=  math.log(fx_list[i])
        sum_xx +=  x_list[i]**2
    
    eq1 = [sum_x, n, sum_lny]
    eq2 = [sum_xx,  sum_x, sum_xlny]

    matrix = [eq1, eq2]
    m = 3
    
    if printout:
        print("System of equations (Unsolved):")
        for row in matrix:
            for col in range(m):
                if col < m-2:
                    print(f"{row[col]}(a{col})", end = " + ")
                if col == m-2:
                    print(f"{row[col]}(a{col})", end = " = ")
                if col == m-1:
                    print(f"{row[col]}")

    #solve set of equations
    gauss_jordan_elimination(matrix)
    if printout:
        print("System of equations (Solved):")
        for row in matrix:
            for col in range(m):
                if col < m-2:
                    print(f"{row[col]}(a{col})", end = " + ")
                if col == m-2:
                    print(f"{row[col]}(a{col})", end = " = ")
                if col == m-1:
                    print(f"{row[col]}")

    a = matrix[0][-1]
    b = math.pow(math.e, matrix[-1][-1])
    P_x = b*math.pow(math.e, a*approx_x)
    if printout:
        print("Therefore, in the equation y = be^ax,")
        print(f"a = {a}\nb = {b}")
        print(f"P({approx_x}) = {P_x}\n")

    return P_x

#############################################################################################
#Printout of the absolute value of the difference between the two values
def actual_error(actual, approx):
    error = abs(actual - approx)
    if printout: print(f"Error = {error}\n")
#############################################################################################
#run program from here for printout of approximations at x = 0.25
def main():
    global printout
    printout = True
    line_len = 35

    print("-"*line_len)
    print("Actual Value")
    print("-"*line_len)

    f_x = actual(0.25)
    print("-"*line_len)

    print("Question 1.1-1.2")
    print("-"*line_len)

    actual_error(f_x, lagrange_interpolating_polynomial(0.25))
    print("-"*line_len)

    actual_error(f_x, newtons_divided_difference_formula(0.25))
    print("-"*line_len)

    actual_error(f_x, bezier_point(0.25)[1])
    print("-"*line_len)

    print("Question 2.1-2.3")
    print("-"*line_len)

    actual_error(f_x, linear_least_squares_polynomial(0.25))
    print("-"*line_len)

    actual_error(f_x, least_squares_polynomial(0.25))
    print("-"*line_len)

    actual_error(f_x, least_squares_exponential_form(0.25))
    print("-"*line_len)

if __name__ == '__main__': 
    main()