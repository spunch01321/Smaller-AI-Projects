import random

BOARD_SIZE = 10
SHIP_SIZES = [5, 4, 3, 3, 2]

class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0

class Board:
    def __init__(self):
        self.grid = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.ships = []

    def place_ship(self, ship, x, y, horizontal):
        if horizontal:
            for i in range(ship.size):
                self.grid[y][x + i] = 'S'
        else:
            for i in range(ship.size):
                self.grid[y + i][x] = 'S'
        self.ships.append(ship)

    def receive_attack(self, x, y):
        if self.grid[y][x] == 'S':
            self.grid[y][x] = 'X'
            for ship in self.ships:
                if self.is_ship_hit(ship):
                    ship.hits += 1
            return True
        elif self.grid[y][x] == ' ':
            self.grid[y][x] = 'O'
        return False

    def is_ship_hit(self, ship):
        count = sum(row.count('X') for row in self.grid)
        return count > sum(s.hits for s in self.ships) - ship.hits

    def all_ships_sunk(self):
        return all(ship.hits == ship.size for ship in self.ships)

class BattleshipGame:
    def __init__(self):
        self.player_board = Board()
        self.ai_board = Board()
        self.setup_boards()

    def setup_boards(self):
        for board in [self.player_board, self.ai_board]:
            for size in SHIP_SIZES:
                while True:
                    x = random.randint(0, BOARD_SIZE - 1)
                    y = random.randint(0, BOARD_SIZE - 1)
                    horizontal = random.choice([True, False])
                    if self.can_place_ship(board, size, x, y, horizontal):
                        board.place_ship(Ship(size), x, y, horizontal)
                        break

    def can_place_ship(self, board, size, x, y, horizontal):
        if horizontal:
            if x + size > BOARD_SIZE:
                return False
            return all(board.grid[y][x+i] == ' ' for i in range(size))
        else:
            if y + size > BOARD_SIZE:
                return False
            return all(board.grid[y+i][x] == ' ' for i in range(size))

    def player_turn(self):
        while True:
            try:
                x = int(input("Enter x coordinate (0-9): "))
                y = int(input("Enter y coordinate (0-9): "))
                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                    hit = self.ai_board.receive_attack(x, y)
                    print("Hit!" if hit else "Miss!")
                    return
                else:
                    print("Invalid coordinates. Try again.")
            except ValueError:
                print("Invalid input. Please enter numbers.")

    def ai_turn(self):
        best_move = self.minimax(self.player_board, 3, float('-inf'), float('inf'), True)
        x, y = best_move[0]
        hit = self.player_board.receive_attack(x, y)
        print(f"AI attacks ({x}, {y}). {'Hit!' if hit else 'Miss!'}")

    def minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.all_ships_sunk():
            return (None, self.evaluate_board(board))

        if maximizing:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_possible_moves(board):
                x, y = move
                new_board = self.simulate_attack(board, x, y)
                eval = self.minimax(new_board, depth - 1, alpha, beta, False)[1]
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (best_move, max_eval)
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_possible_moves(board):
                x, y = move
                new_board = self.simulate_attack(board, x, y)
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)[1]
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (best_move, min_eval)

    def get_possible_moves(self, board):
        return [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if board.grid[y][x] in [' ', 'S']]

    def simulate_attack(self, board, x, y):
        new_board = Board()
        new_board.grid = [row[:] for row in board.grid]
        new_board.ships = [Ship(ship.size) for ship in board.ships]
        new_board.receive_attack(x, y)
        return new_board

    def evaluate_board(self, board):
        ship_cells = sum(ship.size for ship in board.ships)
        hit_cells = sum(row.count('X') for row in board.grid)
        return hit_cells / ship_cells

    def play(self):
        while True:
            self.player_turn()
            if self.ai_board.all_ships_sunk():
                print("Congratulations! You win!")
                break
            self.ai_turn()
            if self.player_board.all_ships_sunk():
                print("AI wins. Better luck next time!")
                break

if __name__ == "__main__":
    game = BattleshipGame()
    game.play()