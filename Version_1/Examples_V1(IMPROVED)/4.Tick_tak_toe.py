from abc import ABC, abstractmethod
from collections import deque
from enum import Enum


class IObserver(ABC):
    @abstractmethod
    def update(self, msg: str) -> None:
        pass

class ConsoleNotifier(IObserver):
    def update(self, msg: str) -> None:
        print(f"[NOTIFICATION]: {msg}")

class Symbol:
    def __init__(self, mark: str):
        self._mark = mark

    def get_mark(self) -> str:
        return self._mark

class Board:
    def __init__(self, size: int):
        self._board_size = size
        self._empty_symbol = Symbol("-")
        self._grid = [
            [self._empty_symbol for _ in range(self._board_size)]
            for _ in range(self._board_size)
        ]

    def get_board_size(self):
        return self._board_size

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self._board_size and 0 <= col < self._board_size

    def get_cell_symbol(self, row: int, col: int) -> Symbol | None:
        if not self.is_valid_position(row, col):
            print("Not a valid row or col !")
            return
        return self._grid[row][col]

    def mark_position(self, row, col, symbol: Symbol) -> bool:
        if not self.is_valid_position(row, col):
            print("Not a valid row or col !")
            return False

        self._grid[row][col] = symbol
        return True

    def is_empty_cell(self, row: int, col: int):
        return self._grid[row][col] == self._empty_symbol

    def display(self):
        print("\n", end = "  ")
        for i in range(self._board_size):
            print(i, end=" ")
        print()
        for i in range(self._board_size):
            print(i, end = " ")
            for j in range(self._board_size):
                print(self._grid[i][j].get_mark(), end = " ")

            print()
        print()

class Player:
    def __init__(self, name: str, symbol: Symbol):
        self._name = name
        self._symbol = symbol
        self._score = 0

    def get_name(self) -> str:
        return self._name

    def get_symbol(self) -> Symbol:
        return self._symbol

    def get_score(self) -> int:
        return self._score

    def increment_score(self) -> None:
        self._score += 1

class TicTacToeRules(ABC):
    @abstractmethod
    def is_valid_move(self, row: int, col: int, board: Board) -> bool:
        pass

    @abstractmethod
    def check_draw_condition(self, board: Board) -> bool:
        pass

    @abstractmethod
    def check_win_condition(self, board: Board, symbol: Symbol) -> bool:
        pass

class StandardTicTacToeRules(TicTacToeRules):
    def is_valid_move(self, row: int, col: int, board: Board) -> bool:
        if not board.is_valid_position(row, col):
            return False

        if not board.is_empty_cell(row, col):
            return False

        return True

    def check_draw_condition(self, board: Board) -> bool:
        size = board.get_board_size()
        for i in range(size):
            for j in range(size):
                if board.is_empty_cell(i, j):
                    return False

        return True

    def check_win_condition(self, board: Board, symbol: Symbol) -> bool:
        size = board.get_board_size()

        #check row
        for i in range(size):
            win = True
            for j in range(size):
                if board.get_cell_symbol(i, j) is not symbol:
                    win = False
                    break
            if win:
                return True

        # check col
        for j in range(size):
            win = True
            for i in range(size):
                if board.get_cell_symbol(i, j) is not symbol:
                    win = False
                    break
            if win:
                return True

        # check main diagonal
        win = True
        for i in range(size):
            if board.get_cell_symbol(i, i) is not symbol:
                win = False
                break

        if win:
            return True

        #check anti-diagonal
        win = True
        for i in range(size):
            if board.get_cell_symbol(i, i) is not symbol:
                win = False
                break

        return win

class TicTacToeGame:
    def __init__(self, board_size: int):
        self._size = board_size
        self._board = Board(board_size)
        self._players = deque()
        self._observers = []
        self._is_game_over = False
        self._rules = StandardTicTacToeRules()

    def add_player(self, player: Player):
        self._players.append(player)

    def add_observer(self, observer: IObserver):
        self._observers.append(observer)

    def notify(self, msg: str):
        for observer in self._observers:
            observer.update(msg)

    def play(self):
        print("=== TIC TAC TOE GAME STARTED ===")
        self._board.display()

        while not self._is_game_over:

            current_player = self._players[0]
            symbol = current_player.get_symbol()

            print(f"{current_player.get_name()}'s turn ({symbol.get_mark()}): ")
            row = int(input("Enter row: "))
            col = int(input("Enter col: "))

            if not self._board.is_valid_position(row, col):
                print("Invalid Position ! try again")
                return

            if self._rules.is_valid_move(row, col, self._board):
                self._board.mark_position(row, col, symbol)
                if self._rules.check_win_condition(self._board, symbol):
                    print(f"{current_player.get_name()} wins !")
                    self.notify(f"{current_player.get_name()} wins !")
                    self._is_game_over = True
                elif self._rules.check_draw_condition(self._board):
                    print("It's a DRAW !")
                    self.notify("It's a DRAW !")
                    self._is_game_over = True
                self._board.display()
            else:
                print("Invalid Move")
                return

            self._players.rotate(-1)

class GameType(Enum):
    STANDARD = 1

class TicTacToeGameFactory:
    @staticmethod
    def create_game(size: int, game_type: GameType):
        if game_type == GameType.STANDARD:
            return TicTacToeGame(size)
        else:
            raise ValueError("Unsupported game type")

def main():
    # size = int(input("Enter board size: "))
    size = 3
    game = TicTacToeGameFactory.create_game(size, GameType.STANDARD)

    player1 = Player("Piyush", Symbol("X"))
    player2 = Player("Arun", Symbol("O"))

    game.add_player(player1)
    game.add_player(player2)

    notification_service = ConsoleNotifier()
    game.add_observer(notification_service)

    game.play()


if __name__ == "__main__":
    main()









































