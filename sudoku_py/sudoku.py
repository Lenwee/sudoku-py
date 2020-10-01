import copy
import math
import random
import string

NUMBER_TOKENS = 'N'
CHAR_TOKENS = 'C'

VALID_TOKENS = [
    NUMBER_TOKENS,
    CHAR_TOKENS
]


class SudokuException(Exception):
    pass


class Sudoku:

    def __init__(self, board, block_width=None, block_height=None, board_token=NUMBER_TOKENS):
        self.board = board
        self.board_width = len(board)
        if not block_height and not block_width:
            self.block_height, self.block_width = self.__get_block_dimensions()
        elif not block_height:
            self.block_height = block_width
        elif not block_width:
            self.block_width = block_height
        else:
            self.block_width = block_width
            self.block_height = block_height
        if board_token not in VALID_TOKENS:
            raise SudokuException('Invalid board token selected.')
        self.board_token = board_token
        self.board_tokens = self.get_board_tokens()
        self.solutions = []
        self.board_is_valid()

    def get_board_tokens(self):
        if self.board_token is NUMBER_TOKENS:
            return list(range(1, self.board_width + 1))
        elif self.board_token is CHAR_TOKENS:
            return list(string.ascii_lowercase[:self.board_width])

    def board_is_valid(self):
        board_height = self.board_width
        for row in self.board:
            if len(row) != board_height:
                raise SudokuException('Board dimensions are invalid.')
        block_area = self.block_height * self.block_width
        if block_area != board_height:
            raise SudokuException('Block dimensions are not valid for a board of this size.')
        for row in self.board:
            for cell in row:
                if cell != 0 and cell not in self.board_tokens:
                    raise SudokuException('Cell contains invalid value: {0}'.format(cell))

    def solve(self, solutions=1):
        self.solutions = []
        self.__solve(solutions=solutions)

    def board_exchange_values(self, value_mappings):
        for y in range(self.board_width):
            for x in range(self.board_width):
                if self.board[y][x] != 0:
                    try:
                        self.board[y][x] = value_mappings[self.board[y][x]]
                    except KeyError:
                        raise SudokuException('Value mapping has missing value: {0}'.format(self.board[y][x]))

    def __get_block_dimensions(self):
        block_area = self.board_width
        height = 0
        width = math.ceil(math.sqrt(block_area))
        while width <= block_area:
            if block_area % width == 0:
                height = int(block_area / width)
                break
            width += 1
        return height, width

    def _possible(self, x, y, value):
        return (self.__check_row(y, value) and
                self.__check_col(x, value) and
                self.__check_block(x, y, value))

    def __check_block(self, x, y, value):
        block_x = (x // self.block_width) * self.block_width
        block_y = (y // self.block_height) * self.block_height

        for y in range(self.block_height):
            for x in range(self.block_width):
                if self.board[block_y + y][block_x + x] == value:
                    return False
        return True

    def __check_row(self, y, value):
        for x in range(self.board_width):
            if self.board[y][x] == value:
                return False
        return True

    def __check_col(self, x, value):
        for y in range(self.board_width):
            if self.board[y][x] == value:
                return False
        return True

    def __solve(self, solutions):
        for y in range(self.board_width):
            for x in range(self.board_width):
                if self.board[y][x] == 0:
                    for value in self.board_tokens:
                        if self._possible(x, y, value):
                            self.board[y][x] = value
                            self.__solve(solutions=solutions)
                            if len(self.solutions) >= solutions:
                                return
                            self.board[y][x] = 0
                    return
        self.solutions.append(copy.deepcopy(self.board))


class SudokuGenerator(Sudoku):

    def __init__(self, board_width, block_width=None, block_height=None):
        self.board_width = board_width
        super(SudokuGenerator, self).__init__(
            board=self.__create_empty_board(),
            block_width=block_width,
            block_height=block_height,
            board_token=CHAR_TOKENS
        )
        self.__board_created = False

    @staticmethod
    def __get_random_value(cell_options):
        return random.choice(cell_options)

    def __create_empty_board(self):
        return [[0] * self.board_width for i in range(self.board_width)]

    def __create_full_grid(self):
        for y in range(self.board_width):
            for x in range(self.board_width):
                if self.board[y][x] == 0:
                    cell_options = copy.deepcopy(self.board_tokens)
                    while len(cell_options) > 0:
                        if len(cell_options) == 0:
                            break
                        value = self.__get_random_value(cell_options)
                        if self._possible(x, y, value):
                            self.board[y][x] = value
                            self.__create_full_grid()
                            if self.__board_created:
                                return
                            self.board[y][x] = 0
                        cell_options.remove(value)
                    return
        self.__board_created = True
        return

    def generate(self, cells_to_remove):
        self.__create_full_grid()
        grid_coords = []
        for y in range(self.board_width):
            for x in range(self.board_width):
                grid_coords.append((x, y))
        random.shuffle(grid_coords)
        for x, y in grid_coords:
            if cells_to_remove == 0:
                return self.board

            if self.board[y][x] != 0:
                prev_value = self.board[y][x]
                self.board[y][x] = 0
                temp_grid = copy.deepcopy(self.board)
                self.solve(solutions=1)
                self.board = temp_grid
                cells_to_remove -= 1
                if len(self.solutions) != 1:
                    self.board[y][x] = prev_value
                    cells_to_remove += 1
        return self.board
