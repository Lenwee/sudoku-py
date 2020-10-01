import copy
import math
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
            return list(range(1, len(self.board)+1))
        elif self.board_token is CHAR_TOKENS:
            return list(string.ascii_lowercase[:len(self.board)])

    def board_is_valid(self):
        board_height = len(self.board)
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

    def __get_block_dimensions(self):
        block_area = len(self.board)
        height = 0
        width = math.ceil(math.sqrt(block_area))
        while width <= block_area:
            if block_area % width == 0:
                height = int(block_area / width)
                break
            width += 1
        return height, width

    def __possible(self, x, y, value):
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
        for x in range(len(self.board)):
            if self.board[y][x] == value:
                return False
        return True

    def __check_col(self, x, value):
        for y in range(len(self.board)):
            if self.board[y][x] == value:
                return False
        return True

    def __solve(self, solutions):
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                if self.board[y][x] == 0:
                    for value in self.board_tokens:
                        if self.__possible(x, y, value):
                            self.board[y][x] = value
                            self.__solve(solutions=solutions)
                            if len(self.solutions) >= solutions:
                                return
                            self.board[y][x] = 0
                    return
        self.solutions.append(copy.deepcopy(self.board))
