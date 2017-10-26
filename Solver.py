'''
Created on 25 oct. 2017

@author: Vincent Larcin
'''

from pulp import *

def create_starting_numbers(path):
    """
    Reads a file containing a sudoku grid and converts its content to a list of tuples.
    @param path: The path of the file to read
    @return A list of tuples containing the starting numbers
    """
    
    starting_numbers = []
    
    with open(path, "r") as file:
        for i, line in enumerate(file):
            for j, char in enumerate(line):
                if char in "123456789":
                    starting_numbers.append((j+1, i+1, int(char)))
                     
    return starting_numbers


def solve(starting_numbers):
    """
    Solves a sudoku problem given its starting numbers.
    @param starting_numbers: The starting numbers of the sudoku problem
    """
    
    sudoku_problem = LpProblem("Sudoku", LpMinimize)
    
    #Creates a list of boxes, each box being a list of tuples, the coordinates of the cells it contains
    boxes = []
    for i in range(3):
        for j in range(3):
            box = []
            for i2 in range(1, 4):
                for j2 in range(1, 4):
                    box.append((i*3+i2, j*3+j2))
            boxes.append(box)
    
    #Creates the 729 variables
    variables = LpVariable.dict("Variables", (range(1, 10), range(1, 10), range(1, 10)), 0, 1, LpInteger)
    
    #Objective function
    sudoku_problem += lpSum(variables[(column, row, possibility)] for column in range(1, 10) for row in range(1, 10) for possibility in range(1, 10)), "Objective function"
    
    #Constraints to have only one possibility per cell
    for column in range(1, 10):
        for row in range(1, 10):
            sudoku_problem += lpSum([variables[(column, row, possibility)] for possibility in range(1, 10)]) == 1, ""
    
    #Constraints to have only one of each possibility in each column
    for row in range(1, 10):
        for possibility in range(1, 10):
            sudoku_problem += lpSum([variables[(column, row, possibility)] for column in range(1, 10)]) == 1, ""
            
    #Constraints to have only one of each possibility in each row
    for column in range(1, 10):
        for possibility in range(1, 10):
            sudoku_problem += lpSum([variables[(column, row, possibility)] for row in range(1, 10)]) == 1, ""
            
    #Constraint to have only one of each possibility in each box
    for box in boxes:
        for possibility in range(1, 10):
            sudoku_problem += lpSum([variables[(column, row, possibility)] for (row, column) in box]) == 1, ""
    
    #Adds all starting numbers constraints
    for number in starting_numbers:
        sudoku_problem += variables[number] == 1, ""
    
    #Writes and solves the problem
    sudoku_problem.writeLP("Sudoku.lp")
    sudoku_problem.solve()
    
    if sudoku_problem.status == 1:
        print("Solution found!\n")
    else:
        print("No solution found.")
    
    #Displays the solution
    for row in range(1, 10):
        line = ""
        for column in range(1, 10):
            for possibility in range(1, 10):
                if value(variables[(column, row, possibility)]) == 1:
                    line += str(possibility)
        print(line)
            
    
    
if __name__ == '__main__':
    starting_numbers = create_starting_numbers("example0.sdk")
    solve(starting_numbers)