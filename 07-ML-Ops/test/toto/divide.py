# SOLUTION
def divide_without_raising(x:float, y:float) -> float:
    '''
    divides x by y, but instead of raising errors when y equals 0, returns:
    - inf if x positive
    - -inf if x negative
    - nan if x equals 0
    '''
    if y != 0.:
        return x/y
    else:
        if x > 0.:
            return float('inf')
        if x < 0.:
            return -1 * float('inf')
        if x == 0.:
            return float('nan')
