from renderer import Renderer
from organism import Organism
from random import randint


class Simulation:
    def __init__(self):
        self.habitat_width = 200
        self.organisms = []
        self.board = self.get_board()

    def run(self):
        block_width = 5
        population_size = 1000
        renderer = Renderer(block_width, self.habitat_width)
        self.organisms = [
            Organism(randint(0, self.habitat_width - 1), randint(0, self.habitat_width - 1), self.habitat_width,
                     (randint(0, 200), randint(0, 200), randint(0, 200)))
            for _ in range(population_size)]
        while True:
            for organism in self.organisms:
                organism.random_move()
            board = self.get_board()
            renderer.render(board)

    def get_board(self, default_color=(0, 0, 0)):
        board = [[default_color for _ in range(self.habitat_width)] for _ in range(self.habitat_width)]
        for organism in self.organisms:
            board[organism.y][organism.x] = organism.color
        return board
