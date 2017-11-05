# Integer Programming Sudoku Solver

An integer programming sudoku solver in python using the [PuLP](https://pypi.python.org/pypi/PuLP) library.

## How to use

### Prerequisites

To run this script, you need [python 3](https://www.python.org/downloads/).
You also need to install PuLP, either with `pip install pulp` from anywhere on your computer or `pip install -r requirements.txt` from the repository.

### Input Format

A text file of exactly 9 lines containing exactly 9 characters, either a digit corresponding to a starting clue or any other character corresponding to an empty space. See the `.sdk` files if you want examples.

### Usage

```
python solver.py [-h] [-o output] input

positional arguments:
  input                 path to the input file

optional arguments:
  -h, --help            show this help message and exit
  -o output, --output output
                        path to the output file
```
