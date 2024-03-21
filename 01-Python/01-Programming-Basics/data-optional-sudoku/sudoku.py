# pylint: disable=missing-docstring

def sudoku_validator(grid):
    numbers = list(range(1,10))

    # Check horizontal rows
    # If any horizontal row is invalid, return False
    for h_row in grid:
        if any(n not in h_row for n in numbers):
            return False

    # Create a new transposed grid to check the "vertical rows"
    transposed_grid = zip(*grid)
    # If any vertical row is invalid, return False
    for v_row in transposed_grid:
        if any(n not in v_row for n in numbers):
            return False

    # Create lists containing the numbers of the 3x3 squares
    thruples = []
    for row in grid:
        thruples.append(row[:3])
    for row in grid:
        thruples.append(row[3:6])
    for row in grid:
        thruples.append(row[6:9])

    square_rows = []
    for i in range(3, 30, 3):
        square_rows.append(thruples[i-3:i])

    # If any square is invalid, return False
    for s_row in square_rows:
        square = s_row[0] + s_row[1] + s_row[2]
        if any(n not in square for n in numbers):
            return False

    # If get this far in the code, the sudoku is valid
    return True
