"""
Performance testing and benchmarking for Tic-Tac-Toe AI.
This module provides instrumented versions of search algorithms
and comprehensive performance analysis tools.

Usage:
    python performance_tests.py
"""

import time
import math
from typing import Tuple, Optional

from game_engine import initial_state, terminal, utility, player, actions, result, winner, print_board
from evaluation import evaluate
from search import order_moves


class SearchMetrics:
    """Container for search performance metrics."""
    
    def __init__(self):
        """Initialize metrics tracking."""
        self.nodes_explored = 0
        self.pruning_cutoffs = 0
        self.max_depth = 0
    
    def reset(self):
        """Reset all metrics to zero."""
        self.nodes_explored = 0
        self.pruning_cutoffs = 0
        self.max_depth = 0


def minimax_instrumented(state: dict, depth: int = 0, 
                         metrics: SearchMetrics = None) -> Tuple[int, Optional[Tuple[int, int]]]:
    """
    Minimax algorithm with performance instrumentation.
    Identical to regular minimax but tracks:
    - Number of nodes explored
    - Maximum depth reached
    """
    if metrics:
        metrics.nodes_explored += 1
        metrics.max_depth = max(metrics.max_depth, depth)
    
    if terminal(state):
        return utility(state), None
    
    current_player = player(state)
    legal_moves = sorted(actions(state))
    
    if current_player == 'X':
        best_value = -math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = minimax_instrumented(new_state, depth + 1, metrics)
            
            if value > best_value:
                best_value = value
                best_move = action
        
        return best_value, best_move
    else:
        best_value = math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = minimax_instrumented(new_state, depth + 1, metrics)
            
            if value < best_value:
                best_value = value
                best_move = action
        
        return best_value, best_move


def minimax_ab_instrumented(state: dict, alpha: float = -math.inf, 
                            beta: float = math.inf, depth: int = 0, 
                            metrics: SearchMetrics = None, 
                            use_ordering: bool = True) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Alpha-Beta with performance instrumentation.
    Tracks nodes explored, pruning cutoffs, and depth in addition
    to computing the optimal move.
    """
    if metrics:
        metrics.nodes_explored += 1
        metrics.max_depth = max(metrics.max_depth, depth)
    
    if terminal(state):
        return utility(state), None
    
    current_player = player(state)
    legal_moves = (order_moves(state, actions(state), use_heuristic=use_ordering) 
                  if use_ordering else sorted(actions(state)))
    
    if current_player == 'X':
        best_value = -math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = minimax_ab_instrumented(new_state, alpha, beta, 
                                              depth + 1, metrics, use_ordering)
            
            if value > best_value:
                best_value = value
                best_move = action
            
            alpha = max(alpha, best_value)
            if beta <= alpha:
                if metrics:
                    metrics.pruning_cutoffs += 1
                break
        
        return best_value, best_move
    else:
        best_value = math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = minimax_ab_instrumented(new_state, alpha, beta, 
                                              depth + 1, metrics, use_ordering)
            
            if value < best_value:
                best_value = value
                best_move = action
            
            beta = min(beta, best_value)
            if beta <= alpha:
                if metrics:
                    metrics.pruning_cutoffs += 1
                break
        
        return best_value, best_move


def test_3x3_performance():
    """Compare Minimax vs Alpha-Beta performance on 3x3 board."""
    print("\n" + "="*70)
    print("3×3 Board: Minimax vs Alpha-Beta Performance")
    print("="*70)
    
    state = initial_state(3, 3)
    
    # Test Minimax
    print("\n  Running Minimax (plain)...")
    metrics_mm = SearchMetrics()
    start = time.time()
    value_mm, move_mm = minimax_instrumented(state, metrics=metrics_mm)
    time_mm = time.time() - start
    
    # Test Alpha-Beta without ordering
    print("  Running Alpha-Beta (no ordering)...")
    metrics_ab = SearchMetrics()
    start = time.time()
    value_ab, move_ab = minimax_ab_instrumented(state, metrics=metrics_ab, 
                                                use_ordering=False)
    time_ab = time.time() - start
    
    # Test Alpha-Beta with ordering
    print("  Running Alpha-Beta (with ordering)...")
    metrics_ab_ord = SearchMetrics()
    start = time.time()
    value_ab_ord, move_ab_ord = minimax_ab_instrumented(state, metrics=metrics_ab_ord, 
                                                        use_ordering=True)
    time_ab_ord = time.time() - start
    
    # Display results
    print(f"\n{'Algorithm':<20} {'Time (s)':<12} {'Nodes':<12} {'Cutoffs':<12} {'Move':<10}")
    print("-"*70)
    print(f"{'Minimax':<20} {time_mm:<12.4f} {metrics_mm.nodes_explored:<12,} {'N/A':<12} {str(move_mm):<10}")
    print(f"{'Alpha-Beta':<20} {time_ab:<12.4f} {metrics_ab.nodes_explored:<12,} {metrics_ab.pruning_cutoffs:<12,} {str(move_ab):<10}")
    print(f"{'Alpha-Beta+Order':<20} {time_ab_ord:<12.4f} {metrics_ab_ord.nodes_explored:<12,} {metrics_ab_ord.pruning_cutoffs:<12,} {str(move_ab_ord):<10}")
    
    # Analysis
    print(f"\n Performance Analysis:")
    print(f"   • Speedup (AB vs MM): {time_mm/time_ab:.2f}x")
    print(f"   • Node reduction: {(1 - metrics_ab.nodes_explored/metrics_mm.nodes_explored)*100:.1f}%")
    print(f"   • Ordering improvement: {time_ab/time_ab_ord:.2f}x faster")
    print(f"   • Pruning effectiveness: {(metrics_ab.pruning_cutoffs/metrics_ab.nodes_explored)*100:.1f}%")


def test_4x4_move_ordering():
    """Test move ordering impact on 4x4 board."""
    print("\n" + "="*70)
    print("4×4 Board: Move Ordering Impact")
    print("="*70)
    
    state = initial_state(4, 3)
    # Create interesting position
    state = result(state, (1, 1))
    state = result(state, (0, 0))
    state = result(state, (2, 2))
    
    print("\n  Testing without move ordering...")
    metrics_no_ord = SearchMetrics()
    start = time.time()
    value_no, move_no = minimax_ab_instrumented(state, metrics=metrics_no_ord, 
                                                use_ordering=False)
    time_no = time.time() - start
    
    print("  Testing with move ordering...")
    metrics_ord = SearchMetrics()
    start = time.time()
    value_ord, move_ord = minimax_ab_instrumented(state, metrics=metrics_ord, 
                                                  use_ordering=True)
    time_ord = time.time() - start
    
    print(f"\n{'Configuration':<20} {'Time (s)':<12} {'Nodes':<12} {'Cutoffs':<12}")
    print("-"*60)
    print(f"{'No ordering':<20} {time_no:<12.4f} {metrics_no_ord.nodes_explored:<12,} {metrics_no_ord.pruning_cutoffs:<12,}")
    print(f"{'With ordering':<20} {time_ord:<12.4f} {metrics_ord.nodes_explored:<12,} {metrics_ord.pruning_cutoffs:<12,}")
    
    print(f"\n Move Ordering Benefits:")
    print(f"   • Time reduction: {time_no/time_ord:.2f}x faster")
    print(f"   • Node reduction: {(1 - metrics_ord.nodes_explored/metrics_no_ord.nodes_explored)*100:.1f}%")
    print(f"   • Cutoff increase: {(metrics_ord.pruning_cutoffs/metrics_no_ord.pruning_cutoffs):.2f}x more")


def test_scalability():
    """Test performance across different board sizes."""
    print("\n" + "="*70)
    print("Scalability Test: Different Board Sizes")
    print("="*70)
    
    configs = [
        (3, 3, None, "3×3, full search"),
        (4, 3, 3, "4×4 (k=3), depth=3"),
        (4, 4, 3, "4×4 (k=4), depth=3"),
        (5, 4, 2, "5×5 (k=4), depth=2"),
    ]
    
    print(f"\n{'Configuration':<25} {'Time (s)':<12} {'Nodes':<12} {'First Move':<15}")
    print("-"*70)
    
    for m, k, depth, desc in configs:
        state = initial_state(m, k)
        
        start = time.time()
        if depth is None:
            # Full search with Alpha-Beta
            metrics = SearchMetrics()
            value, move = minimax_ab_instrumented(state, metrics=metrics)
            nodes = metrics.nodes_explored
        else:
            # Depth-limited search
            from search import search
            value, move = search(state, depth)
            nodes = "~" + str(int((m*m) ** depth))
        elapsed = time.time() - start
        
        print(f"{desc:<25} {elapsed:<12.4f} {str(nodes):<12} {str(move):<15}")


def run_all_performance_tests():
    """Run complete performance test suite."""
    print("\n" + " TIC-TAC-TOE AI PERFORMANCE ANALYSIS ".center(70))
    
    test_3x3_performance()
    test_4x4_move_ordering()
    test_scalability()
    
    print("\n" + "="*70)
    print(" End of Performance Tests ".center(70))
    print("="*70)


if __name__ == "__main__":
    run_all_performance_tests()