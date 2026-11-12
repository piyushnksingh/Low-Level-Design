import random
from abc import ABC, abstractmethod
from collections import deque


class IObserver(ABC):
    @abstractmethod
    def update(self, msg: str):
        pass


class ConsoleNotifier(IObserver):
    def update(self, msg: str):
        print(f"[NOTIFICATION] : {msg}")


class Dice:
    def __init__(self, faces: int):
        self._faces = faces

    def roll_dice(self):
        return random.randint(1, self._faces)


class BoardEntity(ABC):
    def __init__(self, start: int, end: int):
        self._start = start
        self._end = end

    def get_start(self) -> int:
        return self._start

    def get_end(self) -> int:
        return self._end

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class Snake(BoardEntity):
    def __init__(self, start: int, end: int):
        super().__init__(start, end)

    def display(self):
        print(f"Snake : {self.get_start()} -> {self.get_end()}")

    def name(self):
        return "SNAKE"


class Ladder(BoardEntity):
    def __init__(self, start: int, end: int):
        super().__init__(start, end)

    def display(self):
        print(f"Ladder : {self.get_start()} -> {self.get_end()}")

    def name(self):
        return "LADDER"


class BoardSetupStrategy(ABC):
    @abstractmethod
    def setup_board(self, board: Board):
        pass


class Board:
    def __init__(self, size: int):
        if size < 2:
            raise ValueError("Board Dimension must be at least 2")

        self._board_size = size * size
        self._snakes_and_ladders = []
        self._board_entities = {}

    def get_size(self) -> int:
        return self._board_size

    def can_add_entity(self, position: int):
        return (
                1 <= position < self._board_size and
                position not in self._board_entities
        )

    def add_board_entity(self, entity: BoardEntity):
        start = entity.get_start()
        end = entity.get_end()

        if not self.can_add_entity(start):
            raise ValueError(f"Cannot add entity at {start}")

        self._snakes_and_ladders.append(entity)
        self._board_entities[start] = entity

    def setup_board(self, strategy: BoardSetupStrategy):
        strategy.setup_board(self)

    def get_entity(self, pos: int):
        return self._board_entities.get(pos)

    def get_board_size(self) -> int:
        return self._board_size

    def display(self):
        print("\n=== Board Configuration ===")
        print(f"Board Size: {self._board_size} cells")

        snakes = [
            entity for entity in self._snakes_and_ladders
            if entity.name() == "SNAKE"
        ]

        ladders = [
            entity for entity in self._snakes_and_ladders
            if entity.name() == "LADDER"
        ]

        print(f"\n snakes: {len(snakes)}")
        for snake in snakes:
            snake.display()

        print(f"\nLadders: {len(ladders)}")
        for ladder in ladders:
            ladder.display()

        print("=========================")


class StandardBoardSetupStrategy(BoardSetupStrategy):
    def setup_board(self, board: Board):
        size = board.get_size()
        if size != 100:
            raise ValueError("Standard setup only works for a 10x10 board")

        snakes = [
            (99, 54),
            (95, 75),
            (92, 88),
            (89, 68),
            (74, 53),
            (64, 60),
            (62, 19),
            (49, 11),
            (46, 25),
            (16, 6)
        ]

        ladders = [
            (2, 38),
            (7, 14),
            (8, 31),
            (15, 26),
            (21, 42),
            (28, 84),
            (36, 44),
            (51, 67),
            (71, 91),
            (78, 98),
            (87, 94)
        ]

        for start, end in snakes:
            board.add_board_entity(Snake(start, end))

        for start, end in ladders:
            board.add_board_entity(Ladder(start, end))


class Player:
    def __init__(self, name):
        self._name = name
        self._score = 0
        self._position = 0

    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def set_position(self, position: int):
        self._position = position

    def get_score(self):
        return self._score

    def increment_score(self):
        self._score += 1


class SnakeAndLadderRule(ABC):
    @abstractmethod
    def is_valid_move(self, curr_pos: int, dice_val: int, board_size: int):
        pass

    @abstractmethod
    def check_for_win(self, curr_pos: int, board_size: int):
        pass

    @abstractmethod
    def calculate_new_position(self, current_pos: int, dice_value: int, board: Board):
        pass


class StandardSnakeAndLadderRule(SnakeAndLadderRule):
    def is_valid_move(self, curr_pos: int, dice_val: int, board_size: int):
        return curr_pos + dice_val <= board_size

    def check_for_win(self, curr_pos: int, board_size: int):
        return curr_pos == board_size

    def calculate_new_position(self, current_pos: int, dice_value: int, board: Board):
        new_position = current_pos + dice_value

        entity = board.get_entity(new_position)

        if entity is not None:
            return entity.get_end()

        return new_position


class SnakeAndLadderGame:
    def __init__(self, board: Board, dice: Dice):
        self._board = board
        self._dice = dice

        self._players = deque()
        self._observers = []
        self._rules = StandardSnakeAndLadderRule()
        self._is_game_over = False

    def add_players(self, player: Player):
        self._players.append(player)

    def add_observer(self, observer: IObserver):
        self._observers.append(observer)

    def notify(self, msg: str):
        for observer in self._observers:
            observer.update(msg)

    def display_player_position(self):
        print("\n ===== Current positions ====")
        for player in self._players:
            print(f"{player.get_name()} : {player.get_position()}")

        print("===============================")

    def play(self):
        if len(self._players) < 2:
            print("Need at least 2 players!")
            return

        self.notify("GAME STARTED !")
        self._board.display()

        while not self._is_game_over:
            current_player = self._players[0]
            input(f"{current_player.get_name()}'s turn. Press Enter to roll die...")

            dice_vale = self._dice.roll_dice()
            print(f"Rolled : {dice_vale}")

            current_pos = current_player.get_position()

            if self._rules.is_valid_move(current_pos, dice_vale, self._board.get_board_size()):
                intermediate_pos = current_pos + dice_vale
                new_position = self._rules.calculate_new_position(current_pos, dice_vale, self._board)

                current_player.set_position(new_position)

                entity = self._board.get_entity(intermediate_pos)

                if entity is not None:
                    if entity.name() == "SNAKE":
                        print(
                            f"Oh no! Snake at {intermediate_pos}! "
                            f"Going down to {new_position}"
                        )
                        self.notify(
                            f"{current_player.get_name()} encountered "
                            f"snake at {intermediate_pos}, "
                            f"now going down to {new_position}"
                        )
                    else:
                        print(
                            f"Great! Ladder at {intermediate_pos}! "
                            f"Going up to {new_position}"
                        )
                        self.notify(
                            f"{current_player.get_name()} encountered "
                            f"ladder at {intermediate_pos}, "
                            f"now going up to {new_position}"
                        )

                self.notify(
                    f"{current_player.get_name()} played.. New position: {new_position}"
                )

                self.display_player_position()

                if self._rules.check_for_win(new_position, self._board.get_board_size()):
                    print(f"\n{current_player.get_name()} wins!")

                    current_player.increment_score()

                    self.notify(f"Game ended. Winner is {current_player.get_name()}")
                    self._is_game_over = True
                else:
                    self._players.rotate(-1)
            else:
                print(f"Need exact roll to win !")
                self._players.rotate(-1)


class SnakeAndLadderGameFactory:
    @staticmethod
    def create_standard_game():
        board = Board(10)

        strategy = StandardBoardSetupStrategy()
        board.setup_board(strategy)

        dice = Dice(6)

        return SnakeAndLadderGame(board, dice)


def main():
    game = SnakeAndLadderGameFactory.create_standard_game()
    # Observer
    notifier = ConsoleNotifier()
    game.add_observer(notifier)

    game.add_players(Player("piyush"))
    game.add_players(Player("ramesh"))

    game.play()


if __name__ == "__main__":
    main()

# ------------------------------ with additional strategies --------------------------------



from abc import ABC, abstractmethod
from collections import deque
from enum import Enum
import random


# =========================
# Observer Pattern
# =========================

class IObserver(ABC):
    @abstractmethod
    def update(self, msg: str):
        pass


class SnakeAndLadderConsoleNotifier(IObserver):
    def update(self, msg: str):
        print(f"[NOTIFICATION] {msg}")


# =========================
# Dice
# =========================

class Dice:
    def __init__(self, faces: int):
        self.faces = faces

    def roll(self) -> int:
        return random.randint(1, self.faces)


# =========================
# Board Entities
# =========================

class BoardEntity(ABC):
    def __init__(self, start: int, end: int):
        self.start_position = start
        self.end_position = end

    def get_start(self) -> int:
        return self.start_position

    def get_end(self) -> int:
        return self.end_position

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class Snake(BoardEntity):
    def __init__(self, start: int, end: int):
        if end >= start:
            raise ValueError("Invalid snake: end must be less than start")

        super().__init__(start, end)

    def display(self):
        print(f"Snake: {self.start_position} -> {self.end_position}")

    def name(self) -> str:
        return "SNAKE"


class Ladder(BoardEntity):
    def __init__(self, start: int, end: int):
        if end <= start:
            raise ValueError("Invalid ladder: end must be greater than start")

        super().__init__(start, end)

    def display(self):
        print(f"Ladder: {self.start_position} -> {self.end_position}")

    def name(self) -> str:
        return "LADDER"


# =========================
# Strategy Pattern
# Board Setup
# =========================

class BoardSetupStrategy(ABC):
    @abstractmethod
    def setup_board(self, board):
        pass


# =========================
# Board
# =========================

class Board:
    def __init__(self, dimension: int):
        if dimension < 2:
            raise ValueError("Board dimension must be at least 2")

        self.size = dimension * dimension
        self.snakes_and_ladders = []
        self.board_entities = {}

    def can_add_entity(self, position: int) -> bool:
        return (
            1 <= position < self.size
            and position not in self.board_entities
        )

    def add_board_entity(self, entity: BoardEntity):
        start = entity.get_start()
        end = entity.get_end()

        if not (1 <= start < self.size):
            raise ValueError("Entity start must be within the board")

        if not (1 <= end < self.size):
            raise ValueError("Entity end must be within the board")

        if not self.can_add_entity(start):
            raise ValueError(f"Entity already exists at {start}")

        self.snakes_and_ladders.append(entity)
        self.board_entities[start] = entity

    def setup_board(self, strategy: BoardSetupStrategy):
        strategy.setup_board(self)

    def get_entity(self, position: int):
        return self.board_entities.get(position)

    def get_board_size(self) -> int:
        return self.size

    def display(self):
        print("\n=== Board Configuration ===")
        print(f"Board Size: {self.size} cells")

        snakes = [
            entity for entity in self.snakes_and_ladders
            if entity.name() == "SNAKE"
        ]

        ladders = [
            entity for entity in self.snakes_and_ladders
            if entity.name() == "LADDER"
        ]

        print(f"\nSnakes: {len(snakes)}")
        for snake in snakes:
            snake.display()

        print(f"\nLadders: {len(ladders)}")
        for ladder in ladders:
            ladder.display()

        print("=========================")


# =========================
# Random Board Setup
# =========================

class RandomBoardSetupStrategy(BoardSetupStrategy):

    class Difficulty(Enum):
        EASY = 1
        MEDIUM = 2
        HARD = 3

    def __init__(self, difficulty):
        self.difficulty = difficulty

    def setup_with_probability(self, board, snake_probability):
        board_size = board.get_board_size()
        total_entities = board_size // 10

        for _ in range(total_entities):
            if random.random() < snake_probability:
                self._add_random_snake(board)
            else:
                self._add_random_ladder(board)

    def _add_random_snake(self, board):
        board_size = board.get_board_size()

        for _ in range(100):
            start = random.randint(2, board_size - 1)
            end = random.randint(1, start - 1)

            if board.can_add_entity(start):
                board.add_board_entity(Snake(start, end))
                return

    def _add_random_ladder(self, board):
        board_size = board.get_board_size()

        for _ in range(100):
            start = random.randint(1, board_size - 2)
            end = random.randint(start + 1, board_size - 1)

            if board.can_add_entity(start):
                board.add_board_entity(Ladder(start, end))
                return

    def setup_board(self, board):
        probability = {
            self.Difficulty.EASY: 0.3,
            self.Difficulty.MEDIUM: 0.5,
            self.Difficulty.HARD: 0.7
        }

        self.setup_with_probability(
            board,
            probability[self.difficulty]
        )


# =========================
# Custom Board Setup
# =========================

class CustomCountBoardSetupStrategy(BoardSetupStrategy):
    def __init__(self, snakes, ladders, random_positions):
        self.num_snakes = snakes
        self.num_ladders = ladders
        self.random_positions = random_positions

        self.snake_positions = []
        self.ladder_positions = []

    def add_snake_position(self, start, end):
        self.snake_positions.append((start, end))

    def add_ladder_position(self, start, end):
        self.ladder_positions.append((start, end))

    def _add_random_snakes(self, board):
        for _ in range(self.num_snakes):
            self._add_random_snake(board)

    def _add_random_ladders(self, board):
        for _ in range(self.num_ladders):
            self._add_random_ladder(board)

    def _add_random_snake(self, board):
        board_size = board.get_board_size()

        for _ in range(100):
            start = random.randint(2, board_size - 1)
            end = random.randint(1, start - 1)

            if board.can_add_entity(start):
                board.add_board_entity(Snake(start, end))
                return

        raise RuntimeError("Unable to place snake")

    def _add_random_ladder(self, board):
        board_size = board.get_board_size()

        for _ in range(100):
            start = random.randint(1, board_size - 2)
            end = random.randint(start + 1, board_size - 1)

            if board.can_add_entity(start):
                board.add_board_entity(Ladder(start, end))
                return

        raise RuntimeError("Unable to place ladder")

    def setup_board(self, board):
        if self.random_positions:
            self._add_random_snakes(board)
            self._add_random_ladders(board)

        else:
            for start, end in self.snake_positions:
                board.add_board_entity(Snake(start, end))

            for start, end in self.ladder_positions:
                board.add_board_entity(Ladder(start, end))


# =========================
# Standard Board Setup
# =========================

class StandardBoardSetupStrategy(BoardSetupStrategy):

    def setup_board(self, board):
        if board.get_board_size() != 100:
            raise ValueError(
                "Standard setup only works for a 10x10 board"
            )

        snakes = [
            (99, 54),
            (95, 75),
            (92, 88),
            (89, 68),
            (74, 53),
            (64, 60),
            (62, 19),
            (49, 11),
            (46, 25),
            (16, 6)
        ]

        ladders = [
            (2, 38),
            (7, 14),
            (8, 31),
            (15, 26),
            (21, 42),
            (28, 84),
            (36, 44),
            (51, 67),
            (71, 91),
            (78, 98),
            (87, 94)
        ]

        for start, end in snakes:
            board.add_board_entity(Snake(start, end))

        for start, end in ladders:
            board.add_board_entity(Ladder(start, end))


# =========================
# Player
# =========================

class SnakeAndLadderPlayer:
    def __init__(self, player_id: int, name: str):
        self.player_id = player_id
        self.name = name
        self.position = 0
        self.score = 0

    def get_name(self) -> str:
        return self.name

    def get_position(self) -> int:
        return self.position

    def set_position(self, position: int):
        self.position = position

    def get_score(self) -> int:
        return self.score

    def increment_score(self):
        self.score += 1


# =========================
# Strategy Pattern
# Game Rules
# =========================

class SnakeAndLadderRules(ABC):

    @abstractmethod
    def is_valid_move(self, current_pos, dice_value, board_size):
        pass

    @abstractmethod
    def calculate_new_position(self, current_pos, dice_value, board):
        pass

    @abstractmethod
    def check_win_condition(self, position, board_size):
        pass


class StandardSnakeAndLadderRules(SnakeAndLadderRules):

    def is_valid_move(self, current_pos, dice_value, board_size):
        return current_pos + dice_value <= board_size

    def calculate_new_position(self, current_pos, dice_value, board):
        new_position = current_pos + dice_value

        entity = board.get_entity(new_position)

        if entity is not None:
            return entity.get_end()

        return new_position

    def check_win_condition(self, position, board_size):
        return position == board_size


# =========================
# Game
# =========================

class SnakeAndLadderGame:
    def __init__(self, board, dice):
        self.board = board
        self.dice = dice

        self.players = deque()
        self.rules = StandardSnakeAndLadderRules()
        self.observers = []

        self.game_over = False

    def add_player(self, player):
        self.players.append(player)

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify(self, msg):
        for observer in self.observers:
            observer.update(msg)

    def display_player_positions(self):
        print("\n=== Current Positions ===")

        for player in self.players:
            print(f"{player.get_name()}: {player.get_position()}")

        print("======================")

    def play(self):
        if len(self.players) < 2:
            print("Need at least 2 players!")
            return

        self.notify("Game started")

        self.board.display()

        while not self.game_over:
            current_player = self.players[0]

            input(
                f"\n{current_player.get_name()}'s turn. "
                "Press Enter to roll dice..."
            )

            dice_value = self.dice.roll()
            print(f"Rolled: {dice_value}")

            current_pos = current_player.get_position()

            if self.rules.is_valid_move(
                current_pos,
                dice_value,
                self.board.get_board_size()
            ):
                intermediate_pos = current_pos + dice_value

                new_position = self.rules.calculate_new_position(
                    current_pos,
                    dice_value,
                    self.board
                )

                current_player.set_position(new_position)

                entity = self.board.get_entity(intermediate_pos)

                if entity is not None:
                    if entity.name() == "SNAKE":
                        print(
                            f"Oh no! Snake at {intermediate_pos}! "
                            f"Going down to {new_position}"
                        )

                        self.notify(
                            f"{current_player.get_name()} encountered "
                            f"snake at {intermediate_pos}, "
                            f"now going down to {new_position}"
                        )

                    else:
                        print(
                            f"Great! Ladder at {intermediate_pos}! "
                            f"Going up to {new_position}"
                        )

                        self.notify(
                            f"{current_player.get_name()} encountered "
                            f"ladder at {intermediate_pos}, "
                            f"now going up to {new_position}"
                        )

                self.notify(
                    f"{current_player.get_name()} played. "
                    f"New Position: {new_position}"
                )

                self.display_player_positions()

                if self.rules.check_win_condition(
                    new_position,
                    self.board.get_board_size()
                ):
                    print(f"\n{current_player.get_name()} wins!")

                    current_player.increment_score()

                    self.notify(
                        f"Game Ended. Winner is: "
                        f"{current_player.get_name()}"
                    )

                    self.game_over = True

                else:
                    self.players.rotate(-1)

            else:
                print(
                    f"Need exact roll to reach "
                    f"{self.board.get_board_size()}!"
                )

                self.players.rotate(-1)


# =========================
# Factory Pattern
# =========================

class SnakeAndLadderGameFactory:

    @staticmethod
    def create_standard_game():
        board = Board(10)

        strategy = StandardBoardSetupStrategy()
        board.setup_board(strategy)

        dice = Dice(6)

        return SnakeAndLadderGame(board, dice)

    @staticmethod
    def create_random_game(board_size, difficulty):
        board = Board(board_size)

        strategy = RandomBoardSetupStrategy(difficulty)
        board.setup_board(strategy)

        dice = Dice(6)

        return SnakeAndLadderGame(board, dice)

    @staticmethod
    def create_custom_game(board_size, strategy):
        board = Board(board_size)
        board.setup_board(strategy)

        dice = Dice(6)

        return SnakeAndLadderGame(board, dice)


# =========================
# Main
# =========================

def main():
    print("=== SNAKE AND LADDER GAME ===")

    print("Choose game setup:")
    print("1. Standard Game (10x10 board)")
    print("2. Random Game with Difficulty")
    print("3. Custom Game")

    choice = int(input("Enter choice: "))

    game = None

    if choice == 1:
        game = SnakeAndLadderGameFactory.create_standard_game()

    elif choice == 2:
        board_size = int(input("Enter board dimension: "))

        print("Choose difficulty:")
        print("1. Easy (more ladders)")
        print("2. Medium (balanced)")
        print("3. Hard (more snakes)")

        diff_choice = int(input("Enter difficulty: "))

        difficulty_map = {
            1: RandomBoardSetupStrategy.Difficulty.EASY,
            2: RandomBoardSetupStrategy.Difficulty.MEDIUM,
            3: RandomBoardSetupStrategy.Difficulty.HARD
        }

        difficulty = difficulty_map.get(
            diff_choice,
            RandomBoardSetupStrategy.Difficulty.MEDIUM
        )

        game = SnakeAndLadderGameFactory.create_random_game(
            board_size,
            difficulty
        )

    elif choice == 3:
        board_size = int(input("Enter board dimension: "))

        print("Choose custom setup type:")
        print("1. Specify counts only (random placement)")
        print("2. Specify exact positions")

        custom_choice = int(input("Enter choice: "))

        num_snakes = int(input("Enter number of snakes: "))
        num_ladders = int(input("Enter number of ladders: "))

        strategy = CustomCountBoardSetupStrategy(
            num_snakes,
            num_ladders,
            custom_choice == 1
        )

        if custom_choice == 2:
            for i in range(num_snakes):
                start, end = map(
                    int,
                    input(
                        f"Enter snake {i + 1} start and end: "
                    ).split()
                )

                strategy.add_snake_position(start, end)

            for i in range(num_ladders):
                start, end = map(
                    int,
                    input(
                        f"Enter ladder {i + 1} start and end: "
                    ).split()
                )

                strategy.add_ladder_position(start, end)

        game = SnakeAndLadderGameFactory.create_custom_game(
            board_size,
            strategy
        )

    else:
        print("Invalid choice!")
        return

    # Observer
    notifier = SnakeAndLadderConsoleNotifier()
    game.add_observer(notifier)

    # Players
    num_players = int(input("Enter number of players: "))

    for i in range(num_players):
        name = input(f"Enter name for player {i + 1}: ")

        player = SnakeAndLadderPlayer(i + 1, name)
        game.add_player(player)

    # Start game
    game.play()


if __name__ == "__main__":
    main()

















