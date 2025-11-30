"""
Adversarial search algorithms for Tic-Tac-Toe AI.
This module implements various search strategies:
- Plain Minimax (exhaustive search)
- Minimax with Alpha-Beta pruning (optimized)
- Depth-limited search with heuristic evaluation
"""

from typing import Tuple, Optional, List, Callable
import math
from game_engine import terminal, utility, player, actions, result
from evaluation import evaluate


def order_moves(state: dict, moves: List[Tuple[int, int]], 
                use_heuristic: bool = True) -> List[Tuple[int, int]]:
    """
    Order moves for better alpha-beta pruning efficiency.
    Move ordering is crucial for alpha-beta pruning effectiveness. This function
    prioritizes moves that are more likely to be good, leading to earlier cutoffs.
    Priority Strategy:
    1. Immediate wins (highest priority)
    2. Moves with best heuristic evaluation
    3. Center positions (positional advantage)
    4. Lexicographic ordering (for determinism)
    """
    if not use_heuristic:
        # Just use lexicographic ordering for determinism
        return sorted(moves)
    
    from game_engine import winner  # Import here to avoid circular dependency
    
    m = state['m']
    center = m // 2
    current = player(state)
    
    def move_priority(move: Tuple[int, int]) -> Tuple[int, float, int, int]:
        """Calculate priority tuple for sorting."""
        r, c = move
        
        # Check if this move wins immediately
        new_state = result(state, move)
        if winner(new_state) == current:
            return (0, 0, r, c)  # Highest priority
        
        # Evaluate resulting position
        eval_score = -evaluate(new_state) if current == 'O' else evaluate(new_state)
        
        # Distance from center (lower is better)
        dist = abs(r - center) + abs(c - center)
        
        return (1, -eval_score, dist, r)
    
    return sorted(moves, key=move_priority)


def minimax(state: dict) -> Tuple[int, Optional[Tuple[int, int]]]:
    """
    Plain Minimax algorithm without pruning.
    Performs exhaustive search of the entire game tree to find the optimal move.
    Guaranteed to be optimal but computationally expensive for large search spaces.
    Time Complexity: O(b^d) where b = branching factor, d = depth
    Space Complexity: O(d) for recursion stack
    """
    if terminal(state):
        return utility(state), None
    
    current_player = player(state)
    legal_moves = sorted(actions(state))  # Deterministic ordering
    
    if current_player == 'X':  # Maximizing player
        best_value = -math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = minimax(new_state)
            
            if value > best_value:
                best_value = value
                best_move = action
        
        return best_value, best_move
    
    else:  # Minimizing player (O)
        best_value = math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = minimax(new_state)
            
            if value < best_value:
                best_value = value
                best_move = action
        
        return best_value, best_move


def minimax_ab(state: dict, alpha: float = -math.inf, beta: float = math.inf, 
               use_ordering: bool = True) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Minimax with Alpha-Beta pruning.
    Optimized version of Minimax that prunes branches that cannot affect the
    final decision. Maintains optimality while significantly reducing the number
    of nodes explored.
    Alpha-Beta Pruning:
    - Alpha: Best value maximizer can guarantee (lower bound)
    - Beta: Best value minimizer can guarantee (upper bound)
    - Prune when alpha >= beta (remaining branches won't be chosen)
    Best Case: O(b^(d/2)) with perfect move ordering
    Worst Case: O(b^d) with terrible move ordering
    """
    if terminal(state):
        return utility(state), None
    
    current_player = player(state)
    
    # Use move ordering if enabled, otherwise lexicographic for determinism
    if use_ordering:
        legal_moves = order_moves(state, actions(state), use_heuristic=True)
    else:
        legal_moves = sorted(actions(state))
    
    if current_player == 'X':  # Maximizing player
        best_value = -math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = minimax_ab(new_state, alpha, beta, use_ordering)
            
            if value > best_value:
                best_value = value
                best_move = action
            
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # Beta cutoff: MIN won't allow this branch
        
        return best_value, best_move
    
    else:  # Minimizing player (O)
        best_value = math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = minimax_ab(new_state, alpha, beta, use_ordering)
            
            if value < best_value:
                best_value = value
                best_move = action
            
            beta = min(beta, best_value)
            if beta <= alpha:
                break  # Alpha cutoff: MAX won't allow this branch
        
        return best_value, best_move


def search(state: dict, depth: int, eval_fn: Callable = evaluate, 
           alpha: float = -math.inf, beta: float = math.inf) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Depth-limited Minimax with Alpha-Beta pruning and heuristic evaluation.
    For large game trees where exhaustive search is impractical, this function
    limits the search depth and uses a heuristic evaluation function to estimate
    the value of non-terminal positions at the depth limit.
    Strategy:
    - Search to specified depth limit
    - Use heuristic evaluation at leaf nodes
    - Prioritize immediate wins/losses (±1000 vs heuristic ±100)
    - Apply alpha-beta pruning for efficiency
    - Use move ordering for better pruning
    """
    # Check terminal state
    if terminal(state):
        u = utility(state)
        # Return large values for actual wins/losses to prioritize them
        # over heuristic evaluations
        if u == 1:
            return 1000, None
        elif u == -1:
            return -1000, None
        else:
            return 0, None
    
    # Depth limit reached: use heuristic evaluation
    if depth == 0:
        return eval_fn(state), None
    
    current_player = player(state)
    legal_moves = order_moves(state, actions(state), use_heuristic=True)
    
    if current_player == 'X':  # Maximizing player
        best_value = -math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = search(new_state, depth - 1, eval_fn, alpha, beta)
            
            if value > best_value:
                best_value = value
                best_move = action
            
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # Beta cutoff
        
        return best_value, best_move
    
    else:  # Minimizing player (O)
        best_value = math.inf
        best_move = None
        
        for action in legal_moves:
            new_state = result(state, action)
            value, _ = search(new_state, depth - 1, eval_fn, alpha, beta)
            
            if value < best_value:
                best_value = value
                best_move = action
            
            beta = min(beta, best_value)
            if beta <= alpha:
                break  # Alpha cutoff
        
        return best_value, best_move