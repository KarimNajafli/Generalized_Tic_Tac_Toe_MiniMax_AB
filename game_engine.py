"""
Game engine module for generalized Tic-Tac-Toe.
This module implements the core game rules for m×m Tic-Tac-Toe with k-in-a-row
win condition. It provides functions for state management, move validation,
and win detection.
"""

from typing import List, Tuple, Optional
import copy


def initial_state(m: int = 3, k: int = 3) -> dict:
    """
    Create initial empty board state.
    """
    return {
        'board': [[None for _ in range(m)] for _ in range(m)],
        'm': m,
        'k': k,
        'moves': 0
    }


def player(state: dict) -> str:
    """
    Determine whose turn it is.
    X always moves first. Players alternate turns based on the number
    of moves that have been made.
    """
    return 'X' if state['moves'] % 2 == 0 else 'O'


def actions(state: dict) -> List[Tuple[int, int]]:
    """
    Get all legal moves (empty cells).
    """
    m = state['m']
    board = state['board']
    return [(r, c) for r in range(m) for c in range(m) if board[r][c] is None]


def result(state: dict, action: Tuple[int, int]) -> dict:
    """
    Apply action to state and return new state.
    This function does not modify the original state. It creates a deep copy
    and applies the move to the copy, ensuring immutability.
    """
    r, c = action
    
    # Validate move
    if state['board'][r][c] is not None:
        raise ValueError(f"Invalid move: cell ({r}, {c}) is already occupied")
    
    # Create new state
    new_state = copy.deepcopy(state)
    new_state['board'][r][c] = player(state)
    new_state['moves'] += 1
    return new_state


def _check_line(line: List[Optional[str]], k: int) -> Optional[str]:
    """
    Check if a line contains k consecutive marks of the same player.
    This is a helper function used by winner() to check rows, columns,
    and diagonals for winning sequences.
    """
    if len(line) < k:
        return None
    
    count = 0
    current = None
    
    for cell in line:
        if cell is not None and cell == current:
            count += 1
            if count >= k:
                return current
        else:
            current = cell
            count = 1 if cell is not None else 0
    
    return None


def winner(state: dict) -> Optional[str]:
    """
    Determine if there's a winner.
    Checks all possible lines (rows, columns, and diagonals) for k consecutive
    marks of the same player. Uses a sliding window approach to efficiently
    check all diagonal segments.
    """
    board = state['board']
    m = state['m']
    k = state['k']
    
    # Check rows
    for row in board:
        w = _check_line(row, k)
        if w:
            return w
    
    # Check columns
    for c in range(m):
        col = [board[r][c] for r in range(m)]
        w = _check_line(col, k)
        if w:
            return w
    
    # Check diagonals (top-left to bottom-right)
    # Check all possible starting positions for k-length diagonals
    for start_r in range(m - k + 1):
        for start_c in range(m - k + 1):
            diag = [board[start_r + i][start_c + i] 
                   for i in range(m - max(start_r, start_c))]
            w = _check_line(diag, k)
            if w:
                return w
    
    # Check anti-diagonals (top-right to bottom-left)
    for start_r in range(m - k + 1):
        for start_c in range(k - 1, m):
            diag = [board[start_r + i][start_c - i] 
                   for i in range(min(m - start_r, start_c + 1))]
            w = _check_line(diag, k)
            if w:
                return w
    
    return None


def terminal(state: dict) -> bool:
    """
    Check if game is over.
    A game is terminal if either:
    1. There is a winner, or
    2. The board is full (all moves have been made)
    """
    return winner(state) is not None or state['moves'] == state['m'] ** 2


def utility(state: dict) -> Optional[int]:
    """
    Get utility value of terminal state.
    The utility function assigns values to terminal states:
    - +1 if X wins (maximizing player)
    - -1 if O wins (minimizing player)
    -  0 if draw
    - None if state is not terminal
    """
    if not terminal(state):
        return None
    
    w = winner(state)
    if w == 'X':
        return 1
    elif w == 'O':
        return -1
    else:
        return 0


def print_board(state: dict) -> None:
    """
    Print the current board state in a readable format.
    """
    board = state['board']
    m = state['m']
    
    print("\n  " + " ".join(str(i) for i in range(m)))
    for i, row in enumerate(board):
        print(f"{i} " + " ".join(cell if cell else '.' for cell in row))
    print()