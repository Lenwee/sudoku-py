# Sudoku-py

## Overview
Sudoku-py allows you to represent Sudoku boards easily. While also giving you the ability to solve and generate your own Sudoku boards.

## Examples
### Generator Example
```python
from sudoku_py import SudokuGenerator

sudokuGenerator = SudokuGenerator(board_size=9)

sudokuGenerator.generate(cells_to_remove=50, symmetry_removal=True)

print(sudokuGenerator)
0 0 0 | h 0 0 | d e 0 
e 0 0 | 0 0 0 | 0 0 h 
0 h 0 | b 0 0 | 0 0 0 
---------------------
d b a | g h 0 | 0 0 e 
0 e i | a 0 f | g d 0 
c 0 0 | 0 b d | h a i 
---------------------
0 0 0 | 0 0 b | 0 h 0 
f 0 0 | 0 0 0 | 0 0 c 
0 d h | 0 0 g | 0 0 0 

sudokuGenerator.board_exchange_values({'a': 9, 'b': 8, 'c': 7, 'd': 6, 'e': 5, 'f': 4, 'g': 3, 'h': 2, 'i': 1})

print(sudokuGenerator)
0 0 0 | 2 0 0 | 6 5 0 
5 0 0 | 0 0 0 | 0 0 2 
0 2 0 | 8 0 0 | 0 0 0 
---------------------
6 8 9 | 3 2 0 | 0 0 5 
0 5 1 | 9 0 4 | 3 6 0 
7 0 0 | 0 8 6 | 2 9 1 
---------------------
0 0 0 | 0 0 8 | 0 2 0 
4 0 0 | 0 0 0 | 0 0 7 
0 6 2 | 0 0 3 | 0 0 0 
```

### Sudoku Board
```python
from sudoku_py import Sudoku
Sudoku(board=[
    [0,0,0,2,0,0,6,5,0],
    [5,0,0,0,0,0,0,0,2],
    [0,2,0,8,0,0,0,0,0],
    [6,8,9,3,2,0,0,0,5],
    [0,5,1,9,0,4,3,6,0],
    [7,0,0,0,8,6,2,9,1],
    [0,0,0,0,0,8,0,2,0],
    [4,0,0,0,0,0,0,0,7],
    [0,6,2,0,0,3,0,0,0]
])

print(sudoku)
0 0 0 | 2 0 0 | 6 5 0 
5 0 0 | 0 0 0 | 0 0 2 
0 2 0 | 8 0 0 | 0 0 0 
---------------------
6 8 9 | 3 2 0 | 0 0 5 
0 5 1 | 9 0 4 | 3 6 0 
7 0 0 | 0 8 6 | 2 9 1 
---------------------
0 0 0 | 0 0 8 | 0 2 0 
4 0 0 | 0 0 0 | 0 0 7 
0 6 2 | 0 0 3 | 0 0 0 

sudoku.solve(solutions=1)

print(sudoku)
1 3 8 | 2 4 7 | 6 5 9 
5 7 4 | 6 3 9 | 1 8 2 
9 2 6 | 8 1 5 | 4 7 3 
---------------------
6 8 9 | 3 2 1 | 7 4 5 
2 5 1 | 9 7 4 | 3 6 8 
7 4 3 | 5 8 6 | 2 9 1 
---------------------
3 1 7 | 4 5 8 | 9 2 6 
4 9 5 | 1 6 2 | 8 3 7 
8 6 2 | 7 9 3 | 5 1 4 

```