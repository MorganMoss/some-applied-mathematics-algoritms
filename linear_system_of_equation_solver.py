
def getone(pivot_point):
    for i in range(len(sys_of_eq[0])):
        if sys_of_eq[pivot_point][pivot_point] != 1:
            q00 = sys_of_eq[pivot_point][pivot_point]

            for j in range(len(sys_of_eq[0])):
                sys_of_eq[pivot_point][j] = sys_of_eq[pivot_point][j] / q00


def getzero(r, c):
    #for i in rows 
    for i in range(len(sys_of_eq[0])):
        #if given value not equal to 0
        if sys_of_eq[r][c] != 0:
            value = sys_of_eq[r][c]

            #That row is subtracted by that value x respective values in that value's column
            for j in range(len(sys_of_eq[0])):
                sys_of_eq[r][j] = sys_of_eq[r][j] - ((value) * sys_of_eq[c][j])



def gauss_jordan_elimination(system_of_equations):
    global sys_of_eq
    sys_of_eq = system_of_equations

    for i in range(len(sys_of_eq)):
        getone(i)

        for j in range(len(sys_of_eq)):
            if i != j:
                getzero(j, i)
