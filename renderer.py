from typing import List, Tuple
import pygame


class Renderer:
    # block_width is how many pixels wide each square is
    # board_size is how many blocks wide the board is
    def __init__(self, block_width: int, board_size: int) -> None:
        pygame.init()
        self.__block_width: int = block_width
        self.__window_width: int = block_width * board_size
        self.__screen = pygame.display.set_mode((self.__window_width, self.__window_width))

    def render(self, board: List[List[Tuple[int, int, int]]]) -> None:
        self.__draw_grid(board, self.__block_width)
        pygame.display.update()

    def __draw_grid(self, board: List[List[Tuple[int, int, int]]], block_width: int) -> None:
        for i, row in enumerate(board):
            for j in range(len(row)):
                self.__draw_rectangle(i * block_width, j * block_width, block_width, board[j][i])

    # x, y are top left corner of rectangle
    def __draw_rectangle(self, x: int, y: int, width: int, color: Tuple[int, int, int]) -> None:
        rectangle = pygame.draw.rect(self.__screen, (0, 0, 0), pygame.Rect(x, y, width, width), 1)
        pygame.Surface.fill(self.__screen, color, rect=rectangle)
