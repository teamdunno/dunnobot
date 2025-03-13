import games.tictactoe as ttt
import pytest


def test_initializes_correctly():
    game = ttt.TicTacToe()
    assert game.playfield == [[ttt.Players.Nothing] * 3] * 3
    assert game.current_turn == ttt.Players.Knots


def test_does_not_allow_placing_twice():
    game = ttt.TicTacToe()
    game.play_move(0, 0)

    with pytest.raises(ValueError):
        game.play_move(0, 0)


def test_switches_turns_correctly():
    game = ttt.TicTacToe()
    game.play_move(0, 0)
    assert game.current_turn == ttt.Players.Crosses
    game.play_move(1, 1)
    assert game.current_turn == ttt.Players.Knots


def test_detects_winner():
    game = ttt.TicTacToe()
    game.play_move(0, 0)  # Knots
    game.play_move(1, 0)  # Crosses
    game.play_move(0, 1)  # Knots
    game.play_move(1, 1)  # Crosses
    game.play_move(0, 2)  # Knots wins
    assert game.checkpoint.win_state == ttt.WinState.Knots


def test_detects_crosses_winner():
    game = ttt.TicTacToe()
    game.play_move(0, 0)  # Knots
    game.play_move(1, 0)  # Crosses
    game.play_move(0, 1)  # Knots
    game.play_move(1, 1)  # Crosses
    game.play_move(2, 2)  # Knots
    game.play_move(1, 2)  # Crosses wins
    assert game.checkpoint.win_state == ttt.WinState.Crosses


def test_detects_draw():
    game = ttt.TicTacToe()
    game.play_move(0, 0)  # Knots
    game.play_move(0, 1)  # Crosses
    game.play_move(0, 2)  # Knots
    game.play_move(1, 1)  # Crosses
    game.play_move(1, 0)  # Knots
    game.play_move(1, 2)  # Crosses
    game.play_move(2, 1)  # Knots
    game.play_move(2, 0)  # Crosses
    game.play_move(2, 2)  # Knots - Draw
    assert game.checkpoint.win_state == ttt.WinState.Draw
