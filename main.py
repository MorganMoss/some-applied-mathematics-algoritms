import math

# import window

x_list = [-1, -0.5, 0, 0.5]
fx_list = [ 0.86199480, 0.95802009, 1.0986123, 1.2943767]

value_set:set = set()

control_points = list(map(lambda a, b : (a,b), x_list, fx_list))

def actual(x):
    print("Actual value: ")
    f_x = math.log((math.e**x)+2)
    print(f"f({x}) = {f_x}\n")
    return f_x


def lagrange_interpolating_polynomial(approx_x):
    n = len(x_list)
    p_x = 0
    print(f"Lagrange interpolating polynomial of degree {n-1}")

    #P(x) sum 
    for j in range(n):  
 
        #Pj(x) product
        product = 1
        for k in range(n):
            if j == k : continue
            product *= (approx_x-x_list[k])/(x_list[j]-x_list[k])
        product *= fx_list[j]
        print(f"P{j+1}({approx_x}) = {product}")

        p_x += product

    print(f"P({approx_x}) = {p_x}\n")
    return p_x


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
def newtons_divided_difference_formula(approx_x):
    print(f"Newtons divided difference formula of degree {len(x_list)-1}")
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
    print("Table of results:")
    print(*value_set, sep="\n")
    value_set = set()


    print(f"P({approx_x}) = {p_x}")
    return p_x


def get_roots(x):
    a = -control_points[0][0]+3*control_points[1][0]-3*control_points[2][0]+control_points[3][0]
    b = 3*control_points[0][0] - 6*control_points[1][0] + 6*control_points[2][0]
    c = -3*control_points[0][0] + 3*control_points[1][0]
    d = control_points[0][0]-x

    if a == 0 and b == 0 and c == 0:
        t = -d
        print(f"t at {x} = {t}")
        return t


    if a == 0 and b == 0:
        t = -d/c
        print(f"t at {x} = {t}")
        return t


    if a == 0: 
        a,b,c = b,c,d
        t = (-b + (b**2-4*a*c)**(1/2))/(2*a)
        print(f"t at {x} = {t}")
        return t


    del0 = b**2-3*a*c
    del1 = 2*b**3-9*a*b*c+27*a**2*d


    C = ((del1 - (del1**2-4*del0**3)**(1/2))/2)**(1/3)

    if C == 0:
        t = (-1/(3*a)*(b))
    else:
        C *= ((-1+(-3)**(1/2))/2)**0
        t = (-1/(3*a)*(b + C + del0/C))

    print(f"t at {x} = {t}")
    return t


def bezier_point(approx_x):  
    control_points = list(map(lambda a, b : (a,b), x_list, fx_list))

    print(f"Bezier point from control points: {control_points}")  
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
    
    print(f"B({t}) = {(x,y)}")
    return (x,y)

def find_specific_x_from_bezier():
    ...


def absolute_error(actual, approx):
    Ea = actual - approx
    min(*x_list)
    Ea
    print(f"absolute error = {Ea}\n")


def main():
    f_x = actual(0.25)
    absolute_error(f_x, lagrange_interpolating_polynomial(0.25))
    absolute_error(f_x, newtons_divided_difference_formula(0.25))
    absolute_error(f_x, bezier_point(0.25)[1])


main()