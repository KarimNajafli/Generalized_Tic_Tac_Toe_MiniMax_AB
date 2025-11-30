"""
Heuristic evaluation module for Tic-Tac-Toe AI.
This module provides heuristic evaluation functions for non-terminal game states.
The evaluation is used in depth-limited search to estimate the value of positions
where exhaustive search is impractical.
"""

from typing import List, Optional, Tuple
from game_engine import terminal, utility


def evaluate(state: dict) -> float:
    """
    Heuristic evaluation function for non-terminal states.
    This function estimates the value of a position based on:
    1. Potential winning sequences for both players
    2. Center control (strategic positional advantage)
    """
    # Check terminal states first
    if terminal(state):
        u = utility(state)
        return u if u is not None else 0
    
    board = state['board']
    m = state['m']
    k = state['k']
    
    score = 0.0
    
    # Evaluate all lines (rows, columns, diagonals)
    score += _evaluate_rows(board, m, k)
    score += _evaluate_columns(board, m, k)
    score += _evaluate_diagonals(board, m, k)
    score += _evaluate_anti_diagonals(board, m, k)
    
    # Add center control bonus
    score += _center_control_bonus(board, m)
    
    return score


def _count_sequences(line: List[Optional[str]], k: int) -> Tuple[int, int]:
    """
    Count potential k-in-a-row sequences for both players in a line.
    Uses a sliding window approach to evaluate all k-length segments.
    Only counts sequences that are not blocked by the opponent.
    """
    x_score = 0
    o_score = 0
    
    # Check all k-length windows
    for i in range(len(line) - k + 1):
        window = line[i:i + k]
        x_count = window.count('X')
        o_count = window.count('O')
        
        # Score only if window is not blocked by opponent
        if x_count > 0 and o_count == 0:
            # Quadratic weighting: more pieces = exponentially better
            x_score += x_count ** 2
        elif o_count > 0 and x_count == 0:
            o_score += o_count ** 2
    
    return x_score, o_score


def _evaluate_rows(board: List[List[Optional[str]]], m: int, k: int) -> float:
    """
    Evaluate all rows on the board.
    """
    score = 0.0
    for row in board:
        x_s, o_s = _count_sequences(row, k)
        score += x_s - o_s
    return score


def _evaluate_columns(board: List[List[Optional[str]]], m: int, k: int) -> float:
    """
    Evaluate all columns on the board.
    """
    score = 0.0
    for c in range(m):
        col = [board[r][c] for r in range(m)]
        x_s, o_s = _count_sequences(col, k)
        score += x_s - o_s
    return score


def _evaluate_diagonals(board: List[List[Optional[str]]], m: int, k: int) -> float:
    """
    Evaluate all top-left to bottom-right diagonals.
    """
    score = 0.0
    for start_r in range(m - k + 1):
        for start_c in range(m - k + 1):
            diag = [board[start_r + i][start_c + i] 
                   for i in range(m - max(start_r, start_c))]
            x_s, o_s = _count_sequences(diag, k)
            score += x_s - o_s
    return score


def _evaluate_anti_diagonals(board: List[List[Optional[str]]], m: int, k: int) -> float:
    """
    Evaluate all top-right to bottom-left diagonals.
    """
    score = 0.0
    for start_r in range(m - k + 1):
        for start_c in range(k - 1, m):
            diag = [board[start_r + i][start_c - i] 
                   for i in range(min(m - start_r, start_c + 1))]
            x_s, o_s = _count_sequences(diag, k)
            score += x_s - o_s
    return score


def _center_control_bonus(board: List[List[Optional[str]]], m: int) -> float:
    """
    Calculate center control bonus.
    The center position is strategically valuable as it allows the most
    potential winning lines. This function adds a small bonus for controlling
    the center.
    """
    center = m // 2
    if board[center][center] == 'X':
        return 0.5
    elif board[center][center] == 'O':
        return -0.5
    return 0.0