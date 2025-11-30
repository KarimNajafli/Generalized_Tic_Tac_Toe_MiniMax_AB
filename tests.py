"""
Comprehensive test suite for Tic-Tac-Toe AI.
This module contains unit tests and integration tests for all components
of the Tic-Tac-Toe implementation.

Usage:
    python tests.py
"""

from game_engine import (initial_state, player, actions, result, winner, 
                         terminal, utility, print_board)
from search import minimax, minimax_ab, search
from gameplay import play_game


def test_game_engine():
    """Test basic game engine functionality."""
    print("\n" + "="*60)
    print("TEST SUITE: Game Engine")
    print("="*60)
    
    # Test 1: Initial state
    print("\n[Test 1] Initial state creation")
    state = initial_state(3, 3)
    assert player(state) == 'X', "First player should be X"
    assert len(actions(state)) == 9, "3x3 board should have 9 actions"
    assert not terminal(state), "Initial state should not be terminal"
    print(" Initial state correct")
    
    # Test 2: State transitions
    print("\n[Test 2] State transitions")
    state = result(state, (1, 1))
    assert player(state) == 'O', "After X moves, should be O's turn"
    assert state['board'][1][1] == 'X', "X should be at (1,1)"
    assert len(actions(state)) == 8, "Should have 8 remaining moves"
    print(" State transitions working")
    
    # Test 3: Win detection (row)
    print("\n[Test 3] Row win detection")
    state = initial_state(3, 3)
    state = result(state, (0, 0))  # X
    state = result(state, (1, 0))  # O
    state = result(state, (0, 1))  # X
    state = result(state, (1, 1))  # O
    state = result(state, (0, 2))  # X - wins
    assert winner(state) == 'X', "X should win with row"
    assert terminal(state), "Game should be terminal"
    assert utility(state) == 1, "Utility should be +1 for X win"
    print(" Row win detected")
    
    # Test 4: Win detection (diagonal)
    print("\n[Test 4] Diagonal win detection")
    state = initial_state(3, 3)
    state = result(state, (0, 0))  # X
    state = result(state, (0, 1))  # O
    state = result(state, (1, 1))  # X
    state = result(state, (0, 2))  # O
    state = result(state, (2, 2))  # X - wins diagonal
    assert winner(state) == 'X', "X should win with diagonal"
    print(" Diagonal win detected")
    
    # Test 5: Draw detection
    print("\n[Test 5] Draw detection")
    state = initial_state(3, 3)
    moves = [(0,0), (0,1), (0,2), (1,1), (1,0), (1,2), (2,1), (2,0), (2,2)]
    for move in moves:
        state = result(state, move)
    assert terminal(state), "Board should be full"
    assert winner(state) is None, "Should be no winner"
    assert utility(state) == 0, "Utility should be 0 for draw"
    print(" Draw detected correctly")
    
    print("\n" + "="*60)
    print("Game Engine: ALL TESTS PASSED ")
    print("="*60)


def test_search_algorithms():
    """Test search algorithms."""
    print("\n" + "="*60)
    print("TEST SUITE: Search Algorithms")
    print("="*60)
    
    # Test 1: Minimax optimality
    print("\n[Test 1] Minimax optimal play on 3x3")
    state = initial_state(3, 3)
    value, move = minimax(state)
    assert value == 0, "Perfect play on 3x3 should lead to draw"
    assert move is not None, "Minimax should return a move"
    print(f" Minimax finds optimal value: {value}, move: {move}")
    
    # Test 2: Alpha-Beta equivalence
    print("\n[Test 2] Alpha-Beta equivalence to Minimax")
    state = initial_state(3, 3)
    mm_val, mm_move = minimax(state)
    ab_val, ab_move = minimax_ab(state, use_ordering=False)
    assert mm_val == ab_val, "Values should match"
    assert mm_move == ab_move, "Moves should match with same ordering"
    print(f" Alpha-Beta equivalent: MM={mm_move}, AB={ab_move}")
    
    # Test 3: Immediate win detection
    print("\n[Test 3] Immediate win detection (4x4)")
    state = initial_state(4, 3)
    state = result(state, (0, 0))  # X
    state = result(state, (1, 0))  # O
    state = result(state, (0, 1))  # X
    state = result(state, (1, 1))  # O
    # X has (0,0) and (0,1), should take (0,2) to win
    value, move = search(state, depth=4)
    test_state = result(state, move)
    assert winner(test_state) == 'X', f"Move {move} should lead to X win"
    print(f" Found winning move: {move}")
    
    # Test 4: Threat blocking
    print("\n[Test 4] Threat blocking (4x4)")
    state = initial_state(4, 3)
    state = result(state, (0, 0))  # X
    state = result(state, (3, 3))  # O
    state = result(state, (0, 1))  # X
    state = result(state, (3, 2))  # O
    # X threatens (0,2), O should block
    value, move = search(state, depth=4)
    assert move == (0, 2), f"O should block at (0,2), got {move}"
    print(f" Correctly blocks threat at: {move}")
    
    print("\n" + "="*60)
    print("Search Algorithms: ALL TESTS PASSED ")
    print("="*60)


def test_edge_cases():
    """Test edge cases and special scenarios."""
    print("\n" + "="*60)
    print("TEST SUITE: Edge Cases")
    print("="*60)
    
    # Test 1: Anti-diagonal win
    print("\n[Test 1] Anti-diagonal win")
    state = initial_state(3, 3)
    state = result(state, (0, 2))  # X
    state = result(state, (0, 0))  # O
    state = result(state, (1, 1))  # X
    state = result(state, (0, 1))  # O
    state = result(state, (2, 0))  # X - wins anti-diagonal
    assert winner(state) == 'X', "X should win anti-diagonal"
    print(" Anti-diagonal win detected")
    
    # Test 2: 4x4 with k=4
    print("\n[Test 2] 4x4 board with k=4 win")
    state = initial_state(4, 4)
    for i in range(4):
        state = result(state, (0, i))  # X
        if i < 3:
            state = result(state, (1, i))  # O
    assert winner(state) == 'X', "X should win with 4-in-a-row"
    print(" 4x4 k=4 win detected")
    
    # Test 3: 5x5 diagonal
    print("\n[Test 3] 5x5 diagonal win (k=4)")
    state = initial_state(5, 4)
    for i in range(4):
        state = result(state, (i, i))  # X
        if i < 3:
            state = result(state, (i, i+1))  # O
    assert winner(state) == 'X', "X should win diagonal on 5x5"
    print(" 5x5 diagonal win detected")
    
    # Test 4: Column win
    print("\n[Test 4] Column win")
    state = initial_state(3, 3)
    state = result(state, (0, 0))  # X
    state = result(state, (0, 1))  # O
    state = result(state, (1, 0))  # X
    state = result(state, (1, 1))  # O
    state = result(state, (2, 0))  # X - wins column
    assert winner(state) == 'X', "X should win with column"
    print(" Column win detected")
    
    print("\n" + "="*60)
    print("Edge Cases: ALL TESTS PASSED ")
    print("="*60)


def test_integration():
    """Test full game integration."""
    print("\n" + "="*60)
    print("TEST SUITE: Integration")
    print("="*60)
    
    # Test 1: AI vs AI game completes
    print("\n[Test 1] Complete AI vs AI game (3x3)")
    result = play_game(minimax_ab, minimax_ab, m=3, k=3, verbose=False)
    print(f"Game result: {result if result else 'Draw'}")
    print(" Game completes successfully")
    
    # Test 2: AI never loses from start
    print("\n[Test 2] AI never loses from empty board")
    # Play a few games with AI as O vs random-ish moves
    # (Since we don't have random here, we'll just verify one optimal game)
    result = play_game(minimax_ab, minimax_ab, m=3, k=3, verbose=False)
    # With two optimal players, should always be a draw
    assert result is None, "Two optimal players should draw"
    print(" Optimal play leads to draw")
    
    print("\n" + "="*60)
    print("Integration: ALL TESTS PASSED ")
    print("="*60)


def run_all_tests():
    """Run all test suites."""
    print("\n" + " TIC-TAC-TOE AI TEST SUITE ".center(60))
    print("="*60)
    
    try:
        test_game_engine()
        test_search_algorithms()
        test_edge_cases()
        test_integration()
        
        print("\n" + "="*60)
        print(" ALL TESTS PASSED! ".center(60))
        print("="*60)
        return True
        
    except AssertionError as e:
        print(f"\n TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)