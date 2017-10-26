'''
Created on 25 oct. 2017

@author: Vincent Larcin
'''

import argparse
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
    Solves a sudoku problem given its starting numbers and returns found solution.
    @param starting_numbers: The starting numbers of the sudoku problem
    @return A two-dimensional list that contains the solution, or None if there is no solution
    """
    
    sudoku_problem = LpProblem("Sudoku", LpMinimize)
    
    values = [i for i in range(1, 10)]
    
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
    variables = LpVariable.dict("Variables", (values, values, values), 0, 1, LpInteger)
    
    #No objective function is needed since a solution matching the constraints is always optimal
    sudoku_problem += 1, "No objective function"
    
    #Constraints to have only one possibility per cell
    for column in values:
        for row in values:
            sudoku_problem += lpSum([variables[(column, row, possibility)] for possibility in values]) == 1, ""
    
    
    for possibility in values:
        #Constraints to have only one of each possibility in each column
        for row in values:
            sudoku_problem += lpSum([variables[(column, row, possibility)] for column in values]) == 1, ""
            
        #Constraints to have only one of each possibility in each row
        for column in values:
            sudoku_problem += lpSum([variables[(column, row, possibility)] for row in values]) == 1, ""
            
        #Constraints to have only one of each possibility in each box
        for box in boxes:
            sudoku_problem += lpSum([variables[(column, row, possibility)] for (row, column) in box]) == 1, ""
    
    #Adds all starting numbers constraints
    for number in starting_numbers:
        sudoku_problem += variables[number] == 1, ""
    
    #Writes and solves the problem
    sudoku_problem.writeLP("Sudoku.lp")
    sudoku_problem.solve()
    
    if sudoku_problem.status != 1:
        return None
    
    solution = []
    
    for row in values:
        line = []
        for column in values:
            for possibility in values:
                if value(variables[(column, row, possibility)]) == 1:
                    line.append(possibility)
        solution.append(line)
    
    return solution
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="path to the input file")
    parser.add_argument("-o", "--output", metavar="output", help="path to the output file")
    args = parser.parse_args()
    
    starting_numbers = create_starting_numbers(args.input)
    solution = solve(starting_numbers)
    
    if solution == None:
        print("No solution found.")
    
    else:
        
        print("Solution found!\n")
        
        #Writes the solution in the chosen output file
        if args.output != None:
            with open(args.output, "w") as file:
                for line in solution:
                    file.writelines(str(el) for el in line)
                    file.write("\n")
    
        #Displays the solution
        for i, row in enumerate(solution):
            line = ""
            for j, el in enumerate(row):
                line += str(el)
                if j in (2, 5):
                    line += "|"
            print(line)
            if i in (2, 5):
                print("---+---+---")
