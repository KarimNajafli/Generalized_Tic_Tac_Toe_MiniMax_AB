"""
Main entry point for Tic-Tac-Toe AI.
Provides command-line interface for running games, tests, and benchmarks.

Usage:
    python main.py              # Play against AI
    python main.py --test       # Run test suite
    python main.py --benchmark  # Run performance tests
    python main.py --ai-vs-ai   # Watch AI play itself
"""

import sys
from game_engine import initial_state
from search import minimax_ab, search
from gameplay import play_game


def play_human_vs_ai(m=3, k=3):
    """Start a game: Human (X) vs AI (O)."""
    print("\n" + "="*60)
    print("HUMAN vs AI".center(60))
    print("="*60)
    print(f"\nBoard: {m}×{m}, Win: {k}-in-a-row")
    print("AI is X (move first), You are O")
    print("Enter moves as (row, col), e.g., (1, 1)\n")
    
    if m == 3:
        agent = minimax_ab
    else:
        agent = lambda state: search(state, depth=3)
    
    play_game(minimax_ab, agent2_fn=None, m=m, k=k, verbose=True)


def play_ai_vs_ai(m=3, k=3):
    """Watch AI play against itself."""
    print("\n" + "="*60)
    print("AI vs AI".center(60))
    print("="*60)
    print(f"\nBoard: {m}×{m}, Win: {k}-in-a-row\n")
    
    if m == 3:
        agent1 = minimax_ab
        agent2 = minimax_ab
    else:
        agent1 = lambda state: search(state, depth=3)
        agent2 = lambda state: search(state, depth=3)
    
    play_game(agent1, agent2, m=m, k=k, verbose=True)


def run_tests():
    """Run the test suite."""
    print("\n" + "="*60)
    print("RUNNING TEST SUITE".center(60))
    print("="*60)
    
    from tests import run_all_tests
    success = run_all_tests()
    
    if success:
        print("\n All tests passed!")
        return 0
    else:
        print("\n Some tests failed")
        return 1


def run_benchmarks():
    """Run performance benchmarks."""
    print("\n" + "="*60)
    print("RUNNING PERFORMANCE BENCHMARKS".center(60))
    print("="*60)
    
    from performance_tests import run_all_performance_tests
    run_all_performance_tests()
    return 0


def print_help():
    """Print usage information."""
    print("""
Tic-Tac-Toe AI - Generalized m×m board with k-in-a-row

Usage:
    python main.py                    Play against AI (3×3)
    python main.py --board 4 --win 3  Play on 4×4, 3-in-a-row
    python main.py --ai-vs-ai         Watch AI vs AI
    python main.py --test             Run test suite
    python main.py --benchmark        Run performance tests
    python main.py --help             Show this help

Options:
    --board M      Board size (default: 3)
    --win K        Win condition (default: 3)
    --ai-vs-ai     AI plays against itself
    --test         Run test suite
    --benchmark    Run performance benchmarks
    --help         Show this help message
""")


def main():
    """Main entry point."""
    args = sys.argv[1:]
    
    # Parse arguments
    if '--help' in args or '-h' in args:
        print_help()
        return 0
    
    if '--test' in args:
        return run_tests()
    
    if '--benchmark' in args:
        return run_benchmarks()
    
    # Parse board size and win condition
    m = 3
    k = 3
    
    try:
        if '--board' in args:
            idx = args.index('--board')
            m = int(args[idx + 1])
        
        if '--win' in args:
            idx = args.index('--win')
            k = int(args[idx + 1])
    except (IndexError, ValueError):
        print("Error: Invalid board size or win condition")
        print_help()
        return 1
    
    # Run game
    if '--ai-vs-ai' in args:
        play_ai_vs_ai(m, k)
    else:
        play_human_vs_ai(m, k)
    
    return 0


if __name__ == "__main__":
    exit(main())