# Sudoku-py

## Overview
Sudoku-py allows you to represent Sudoku grids easily. While also giving you the ability to solve and generate your own Sudoku grids.

## Example
```python
from sudoku_py import SudokuGenerator

generator = SudokuGenerator()
generator.generate_start_grid(cells_to_remove=56)

[
    [0, 0, 0, 0, 0, 0, 'i', 'f', 0], 
    ['h', 0, 'i', 0, 0, 'c', 0, 0, 'd'], 
    [0, 0, 0, 'i', 'e', 'h', 0, 0, 0], 
    [0, 0, 0, 'h', 'i', 0, 0, 0, 0], 
    ['b', 0, 0, 0, 0, 0, 0, 0, 0], 
    ['f', 'i', 0, 'b', 0, 'e', 0, 0, 'g'], 
    ['g', 0, 0, 'a', 0, 'd', 0, 0, 'e'], 
    [0, 0, 0, 'g', 0, 0, 0, 0, 0], 
    [0, 'c', 0, 0, 'f', 0, 'h', 0, 0]
]

generator.grid_exchange_values(
    value_mappings={'a': 1,'b': 2,'c': 3,'d': 4,'e': 5,'f': 6,'g': 7,'h': 8,'i': 9}
)

[
    [0, 0, 0, 0, 0, 0, 9, 6, 0], 
    [8, 0, 9, 0, 0, 3, 0, 0, 4], 
    [0, 0, 0, 9, 5, 8, 0, 0, 0], 
    [0, 0, 0, 8, 9, 0, 0, 0, 0], 
    [2, 0, 0, 0, 0, 0, 0, 0, 0], 
    [6, 9, 0, 2, 0, 5, 0, 0, 7], 
    [7, 0, 0, 1, 0, 4, 0, 0, 5], 
    [0, 0, 0, 7, 0, 0, 0, 0, 0], 
    [0, 3, 0, 0, 6, 0, 8, 0, 0]
]
```

## TODO
* Add support for various Sudoku grid sizes
* Add various digging holes methods