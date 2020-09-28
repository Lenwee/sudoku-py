import copy
import random
import string

empty_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]


class Sudoku:

    def __init__(self, grid, grid_tokens=None):
        if grid_tokens is None:
            grid_tokens = list(range(1, 10))
        self.grid = grid
        self._grid_tokens = grid_tokens

    def __str__(self):
        display = ''
        for row in self.grid:
            for col in row:
                display += f'{col} '
            display += f'\n'
        return display

    def grid_exchange_values(self, value_mappings):
        for y in range(0, 9):
            for x in range(0, 9):
                if self.grid[y][x] != 0:
                    self.grid[y][x] = value_mappings[self.grid[y][x]]
        return self.grid

    def grid_rotate_90_deg(self):
        self.grid = list(zip(*self.grid[::-1]))
        return self.grid

    def grid_shuffle_rows_in_block(self, block):
        rows = [0, 1, 2]
        random.shuffle(rows)
        offset = block * 3
        a = offset + rows.pop()
        b = offset + rows.pop()
        c = offset + rows.pop()
        self.grid[a], self.grid[c], self.grid[b] = self.grid[b], self.grid[a], self.grid[c]

    def grid_shuffle_cols_in_block(self, block):
        cols = [0, 1, 2]
        random.shuffle(cols)
        offset = block * 3
        a = offset + cols.pop()
        b = offset + cols.pop()
        c = offset + cols.pop()
        for row in self.grid:
            row[a], row[b], row[c] = row[b], row[c], row[a]

    def grid_shuffle_cols_by_block(self):
        temp_grid = copy.deepcopy(self.grid)
        blocks = [0, 1, 2]
        random.shuffle(blocks)
        for y in range(0, 9):
            offset = 0
            for block in blocks:
                self.grid[y][offset * 3] = temp_grid[y][block * 3]
                self.grid[y][offset * 3 + 1] = temp_grid[y][block * 3 + 1]
                self.grid[y][offset * 3 + 2] = temp_grid[y][block * 3 + 2]
                offset += 1

    def grid_shuffle_rows_by_block(self):
        temp_grid = copy.deepcopy(self.grid)
        blocks = [0, 1, 2]
        random.shuffle(blocks)
        offset = 0
        for block in blocks:
            self.grid[offset * 3] = temp_grid[block * 3]
            self.grid[offset * 3 + 1] = temp_grid[block * 3 + 1]
            self.grid[offset * 3 + 2] = temp_grid[block * 3 + 2]
            offset += 1


class SudokuSolver(Sudoku):

    def __init__(self, grid, grid_tokens=None):
        super().__init__(grid, grid_tokens)
        self.solutions = []

    def _possible(self, x, y, value):
        return (self._check_row(y, value) and
                self._check_column(x, value) and
                self._check_square(x, y, value))

    def _check_square(self, x, y, value):
        square_x = (x // 3) * 3
        square_y = (y // 3) * 3

        for y in range(0, 3):
            for x in range(0, 3):
                if self.grid[square_y + y][square_x + x] == value:
                    return False
        return True

    def _check_row(self, y, value):
        for x in range(0, 9):
            if self.grid[y][x] == value:
                return False
        return True

    def _check_column(self, x, value):
        for y in range(0, 9):
            if self.grid[y][x] == value:
                return False
        return True

    def _solve(self, max_solutions=1):
        for y in range(0, 9):
            for x in range(0, 9):
                if self.grid[y][x] == 0:
                    for value in self._grid_tokens:
                        if self._possible(x, y, value):
                            self.grid[y][x] = value
                            self._solve()
                            if len(self.solutions) >= max_solutions:
                                return
                            self.grid[y][x] = 0
                    return
        self.solutions.append(copy.deepcopy(self.grid))

    def solve(self, max_solutions=1):
        self.solutions = []
        self._solve(max_solutions=max_solutions)


class SudokuGenerator(SudokuSolver):

    def __init__(self):
        grid_tokens = list(string.ascii_lowercase[:9])
        self._final_grid_created = False
        super().__init__(grid=empty_grid, grid_tokens=grid_tokens)

    @staticmethod
    def _get_random_value(cell_options):
        return random.choice(cell_options)

    def _create_final_grid(self):
        for y in range(0, 9):
            for x in range(0, 9):
                if self.grid[y][x] == 0:
                    cell_options = copy.deepcopy(self._grid_tokens)
                    while len(cell_options) > 0:
                        if len(cell_options) == 0:
                            break
                        value = self._get_random_value(cell_options)
                        if self._possible(x, y, value):
                            self.grid[y][x] = value
                            self._create_final_grid()
                            if self._final_grid_created:
                                return
                            self.grid[y][x] = 0
                        cell_options.remove(value)
                    return
        self._final_grid_created = True
        return

    def generate_start_grid(self, cells_to_remove):
        self._create_final_grid()
        grid_coords = []
        for y in range(0, 9):
            for x in range(0, 9):
                grid_coords.append((x, y))
        random.shuffle(grid_coords)
        for x, y in grid_coords:
            if cells_to_remove == 0:
                return self.grid
            if self.grid[y][x] != 0:
                prev_value = self.grid[y][x]
                self.grid[y][x] = 0
                temp_grid = copy.deepcopy(self.grid)
                self.solutions = []
                self.solve()
                self.grid = temp_grid
                cells_to_remove -= 1
                if len(self.solutions) != 1:
                    self.grid[y][x] = prev_value
                    cells_to_remove += 1
        return self.grid
