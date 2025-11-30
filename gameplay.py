"""
Game play interface for Tic-Tac-Toe.
This module provides utilities for playing games between AI agents
or between an AI and a human player.
"""

from typing import Optional, Callable
from game_engine import initial_state, terminal, player, actions, result, winner, print_board


def play_game(agent1_fn: Callable, agent2_fn: Optional[Callable] = None, 
              m: int = 3, k: int = 3, verbose: bool = True) -> Optional[str]:
    """
    Play a complete game of Tic-Tac-Toe.
    This function manages a full game between two agents (or an agent and a human).
    It handles turn alternation, move validation, and game completion detection.
    """
    state = initial_state(m, k)
    
    while not terminal(state):
        if verbose:
            print_board(state)
            print(f"Player {player(state)}'s turn")
        
        # Get move from appropriate agent
        if player(state) == 'X':
            _, move = agent1_fn(state)
        else:
            if agent2_fn:
                _, move = agent2_fn(state)
            else:
                # Human input
                move = get_human_move(state)
        
        if verbose:
            print(f"Move: {move}")
        
        # Apply move
        state = result(state, move)
    
    # Game over
    if verbose:
        print_board(state)
        w = winner(state)
        if w:
            print(f"Winner: {w}")
        else:
            print("Draw!")
    
    return winner(state)


def get_human_move(state: dict) -> tuple:
    """
    Get move input from human player.
    Prompts the user to enter a move and validates it against legal moves.
    Continues prompting until a legal move is entered.
    """
    legal = actions(state)
    print(f"Legal moves: {legal}")
    
    while True:
        try:
            move_str = input("Enter move as (row, col): ")
            move = eval(move_str)
            
            if move in legal:
                return move
            else:
                print(f"Invalid move. Please choose from: {legal}")
        except:
            print("Invalid format. Please enter as (row, col), e.g., (1, 1)")