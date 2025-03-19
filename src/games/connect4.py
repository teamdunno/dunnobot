from enum import Enum
from pydantic import BaseModel


class Players(Enum):
    Red = "🔴"
    Yellow = "🟡"
    Green = "🟢"
    Blue = "🔵"
    Nothing = "⚫"


class WinState(Enum):
    Red = "🔴 won!"
    Yellow = "🟡 won!"
    Green = "🟢 won!"
    Blue = "🔵 won!"
    NoOne = "⚫"
    Draw = "It's a draw! 🔴🟡🟢🔵"


class Checkpoint(BaseModel):
    win_state: WinState = WinState.NoOne
    playfield: list[list[Players]]
    to_play: Players


class Connect4:
    def __init__(self, width: int = 7, height: int = 6, player_count: int = 2):
        if player_count not in [2, 3, 4]:
            raise ValueError("Connect4 supports only 2, 3, or 4 players")

        self.width: int = width
        self.height: int = height
        self.players = list(Players)[:player_count]
        self.current_turn_idx: int = 0
        self.playfield: list[list[Players]] = [
            [Players.Nothing for _ in range(width)] for _ in range(height)
        ]
        self.checkpoint: Checkpoint = Checkpoint(
            win_state=WinState.NoOne,
            playfield=self.playfield,
            to_play=self.players[self.current_turn_idx],
        )

    def switch_turns(self) -> None:
        self.current_turn_idx = (self.current_turn_idx + 1) % len(self.players)

    def play_move(self, column: int) -> Checkpoint:
        if column < 0 or column >= self.width:
            raise ValueError("Column outside of available playfield")

        for row in reversed(self.playfield):
            if row[column] == Players.Nothing:
                row[column] = self.players[self.current_turn_idx]
                self.switch_turns()
                self.checkpoint = Checkpoint(
                    win_state=self.check_for_win(),
                    playfield=self.playfield,
                    to_play=self.players[self.current_turn_idx],
                )
                return self.checkpoint

        raise ValueError("Column is full")

    def check_for_win(self) -> WinState:
        def check_direction(x, y, dx, dy, player):
            count = 0
            for _ in range(4):
                if (
                    0 <= x < self.width
                    and 0 <= y < self.height
                    and self.playfield[y][x] == player
                ):
                    count += 1
                else:
                    break
                x += dx
                y += dy
            return count == 4

        for y in range(self.height):
            for x in range(self.width):
                if self.playfield[y][x] == Players.Nothing:
                    continue
                player = self.playfield[y][x]
                if any(
                    check_direction(x, y, dx, dy, player)
                    for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]
                ):
                    return WinState[player.name]

        if all(cell != Players.Nothing for row in self.playfield for cell in row):
            return WinState.Draw

        return WinState.NoOne
