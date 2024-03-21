# pylint: disable=missing-docstring
import random
import numpy as np

correct_input_grid = [
    [7,0,0,  0,0,0,  0,0,6],
    [0,0,0,  6,0,0,  0,4,0],
    [0,0,2,  0,0,8,  0,0,0],

    [0,0,8,  0,0,0,  0,0,0],
    [0,5,0,  8,0,6,  0,0,0],
    [0,0,0,  0,2,0,  0,0,0],

    [0,0,0,  0,0,0,  0,1,0],
    [0,4,0,  5,0,0,  0,0,0],
    [0,0,5,  0,0,7,  0,0,4]
]

def sudoku_solver(grid):
    """Sudoku solver"""
    counter = 0
    new_grid = np.array(grid.copy())
    numbers = list(range(1,10))

    for r_idx, row in enumerate(new_grid):
        for i_idx, item in enumerate(row):
            if item == 0:
                counter += 1
                if counter % 500 == 0:
                    print(counter, "\n", new_grid)
                # Generate a random number candidate
                for candidate in random.sample(numbers,k=len(numbers)):
                    # Check if it's already in the row
                    if not candidate in row and not candidate in new_grid.T[i_idx]:
                        item = candidate
                        new_grid[r_idx][i_idx] = candidate
                        break
            if item == 0:
                print("game over for\n", new_grid)
                sudoku_solver(grid)

    return new_grid
                # Check if number is already in square
                #elif (r_idx < 3 and i_idx < 3) and candidate in grid[:3,:3]:


print(sudoku_solver(correct_input_grid))
