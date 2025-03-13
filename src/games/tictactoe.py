from enum import Enum
from pydantic import BaseModel

type Playfield = list[list[Players]]


class Players(Enum):
    Knots = "⭕"
    Crosses = "❌"
    Nothing = "⬛"


class WinState(Enum):
    Knots = "⭕ won!"
    Crosses = "❌ won!"
    NoOne = "⬛"
    Draw = "It's a draw! ❌⭕"


class Checkpoint(BaseModel):
    win_state: WinState = WinState.NoOne
    playfield: Playfield
    to_play: Players


class TicTacToe:
    def __init__(self, size: int = 3):
        self.size: int = size
        self.playfield: Playfield = [
            [Players.Nothing for _ in range(size)] for _ in range(size)
        ]
        self.current_turn: Players = Players.Knots
        self.checkpoint: Checkpoint = Checkpoint(
            win_state=WinState.NoOne,
            playfield=self.playfield,
            to_play=self.current_turn,
        )

    def switch_turns(self) -> None:
        self.current_turn = (
            Players.Crosses if self.current_turn == Players.Knots else Players.Knots
        )

    def play_move(self, x: int, y: int) -> Checkpoint:
        if x > (self.size - 1) or y > (self.size - 1):
            raise ValueError("Position outside of available playfield")
        if self.playfield[y][x] != Players.Nothing:
            raise ValueError("Position already taken")

        self.playfield[y][x] = self.current_turn
        self.switch_turns()

        self.checkpoint = Checkpoint(
            win_state=self.check_for_win(),
            playfield=self.playfield,
            to_play=self.current_turn,
        )

        return self.checkpoint

    # stands for: rotated playfield clockwise
    def rotated_playfield_cw(self) -> Playfield:
        # rotating a matrix should NOT be this complicated!!!!!
        return [list(row) for row in zip(*self.playfield[::-1])]

    def check_for_win(self) -> WinState:
        for player in [Players.Knots, Players.Crosses]:
            # straight horizontal
            for row in self.playfield:
                if [player] * self.size == row:
                    return WinState[player.name]

            # straight vertical
            for column in self.rotated_playfield_cw():
                if [player] * self.size == column:
                    return WinState[player.name]

            # ltr diagonal
            if all(self.playfield[i][i] == player for i in range(self.size)):
                return WinState[player.name]

            # rtl diagonal
            if all(
                self.playfield[i][(self.size - 1) - i] == player
                for i in range(self.size)
            ):
                return WinState[player.name]

        # Check for a draw (if no empty spaces remain)
        if all(cell != Players.Nothing for row in self.playfield for cell in row):
            return WinState.Draw

        return WinState.NoOne
