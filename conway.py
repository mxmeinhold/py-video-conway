""" Conway's game of life """

from copy import deepcopy
import random
from typing import Any, Literal
import itertools
from functools import cache

Option = Literal[0, 1]

class Conway:
    """ An implementation of a board for Conway's game of life

    Attributes:
        rows: int - the number of rows in the grid
        cols: int - the number of columns in the grid
        num_iters: int - the number of steps that have occurred on this grid
        grid: list[list[Option]] - the backing data structure
    """
    rows: int
    cols: int
    num_iters: int
    grid: list[list[Option]]

    def __init__(self, rows: int = 100, cols: int = 100, seed: Any = None):
        self.rows = rows
        self.cols = cols
        self.num_iters = 0

        random.seed(a=seed)
        self.grid = [random.choices([0, 1], k=cols) for _ in range(rows)]

    def step(self) -> None:
        """ Iterate the grid state """

        self.num_iters += 1

        # We'll be modifying the grid so backup the last iteration
        shadow = deepcopy(self.grid)

        def next_val(row: int, col: int) -> Option:
            """ Get the next state for the given coordinates """
            num_neighs = sum(map(lambda n: shadow[n[0]][n[1]], self.neighbors(row, col)))
            if num_neighs == 3 or (num_neighs == 2 and shadow[row][col]) == 1:
                return 1
            return 0


        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = next_val(row, col)

    def get(self, row: int, col: int) -> Option:
        """ Get the value (row, col) on the board.

        Raises IndexError on index out of bounds
        """

        # TODO make this usable for shadow so we get bounds checking
        if row >= len(self.grid) or row < 0:
            raise IndexError(f'{row} outside of bounds [0, {len(self.grid) - 1}]')

        if col >= len(self.grid[row]) or col < 0:
            raise IndexError(f'{col} outside of bounds [0, {len(self.grid[row]) - 1}]')

        return self.grid[row][col]


    @cache
    def neighbors(self, row: int, col: int) -> set[tuple[int, int]]:
        """ Get all the valid 8 connected neighbor coords as (r, c) """
        return set(
            filter(
                lambda n: 0 <= n[0] < self.rows, # bounds check rows
                filter(
                    lambda n: 0 <= n[1] < self.cols, # bounds check cols
                    itertools.product(
                        range(row-1, row+2),
                        range(col-1, col+2),
                    )
                )
            )
        ) - {(row, col)} # don't count here as a neighbor
