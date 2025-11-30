# Generalized Tic-Tac-Toe 

## Running the Code
```bash
# Play against AI (3×3)
python main.py

# Run all tests
python main.py --test

# Run performance benchmarks
python main.py --benchmark

# Watch AI vs AI
python main.py --ai-vs-ai

# Play on 4×4 board, 3-in-a-row
python main.py --board 4 --win 3
```

## 1. Executive Summary

This project implements a generalized Tic-Tac-Toe engine and AI capable of playing on m×m boards with k-in-a-row win conditions. Key features:

 Complete game engine with efficient k-in-a-row detection
 Minimax with Alpha-Beta pruning
 Depth-limited search and heuristic evaluation for larger boards
 Intelligent move ordering for pruning efficiency
 Guaranteed optimal play on 3×3 boards

The agent scales to larger boards (4×4, 5×5) while maintaining tactical soundness.

---

## 2. Implementation Overview

### Architecture

## Game Engine ##

 Functions: `initial_state`, `player`, `actions`, `result`, `winner`, `terminal`, `utility`

## Search Algorithms ##

 `minimax`, `minimax_ab`, `search` (depth-limited with heuristic)

## Strategic Components ##

 `evaluate`, `order_moves` (prioritizes strong moves for pruning)

## Key Design Decisions ##

 Immutable states for safe exploration
 Sliding-window k-in-a-row detection
 Heuristic: counts potential winning sequences with quadratic weighting + center control bonuses
 Move ordering: 1) immediate wins, 2) heuristic evaluation, 3) center positions, 4) lexicographic tie-break

---

## 3. Performance Analysis

## 3×3 Board

3×3 Board: Minimax vs Alpha-Beta Performance

## Algorithm            Time (s)     Nodes        Cutoffs      Move
## ----------------------------------------------------------------------
## Minimax              22.1820      549,946      N/A          (0, 0)
## Alpha-Beta           0.8492       18,297       8,180        (0, 0)
## Alpha-Beta+Order     0.3533       1,908        852          (1, 1)

 ## Performance Analysis:
   • Speedup (AB vs MM): 26.12x
   • Node reduction: 96.7%
   • Ordering improvement: 2.40x faster
   • Pruning effectiveness: 44.7%

## 4×4 Board (depth=3)

## 4×4 Board: Move Ordering Impact

## Configuration        Time (s)     Nodes        Cutoffs
## ------------------------------------------------------------
## No ordering          7.2047       109,952      49,638
## With ordering        1.4193       2,241        1,028

## Move Ordering Benefits:
   • Time reduction: 5.08x faster
   • Node reduction: 98.0%
   • Cutoff increase: 0.02x more

## Scalability
## Scalability Test: Different Board Sizes

## Configuration             Time (s)     Nodes        First Move
## ----------------------------------------------------------------------
## 3×3, full search          0.3784       1908         (1, 1)
## 4×4 (k=3), depth=3        0.1622       ~4096        (2, 2)
## 4×4 (k=4), depth=3        0.0911       ~4096        (2, 2)
## 5×5 (k=4), depth=2        0.1274       ~625         (2, 2)

---

## 4. Algorithm Analysis

## Minimax

 Time: O(b^d), Space: O(d)
 Complete and optimal, but slow

## Alpha-Beta Pruning

 Best: O(b^(d/2)), Worst: O(b^d)
 Observed 96% node reduction with move ordering

## Move Ordering

 Priority: 1) immediate wins, 2) heuristic evaluation, 3) positional/center preference
 Early exploration of strong moves → earlier cutoffs, prevents blunders

---

## 5. Heuristic Evaluation

## Design

 Scores potential sequences: quadratic weighting by number of pieces
 Center bonus: ±0.5 points

## Properties

 Symmetric: eval(X) = -eval(O)
 Monotonic: more pieces → higher score
 Bounded: [-100, +100], below terminal values ±1000

## Limitations

 Ignores forced sequences, tempo, forks, deep defensive patterns
 Depth-limited search mitigates most tactical issues

---

## 6. Testing & Validation

## Core Functionality

 Moves, win/draw detection, Minimax/Alpha-Beta equivalence, threat blocking, full games
 Edge cases: diagonals, various board sizes and k values
 All tests pass

## Optimality (3×3)

 Never loses, always draws/wins against random or optimal opponents

## Scalability (4×4, 5×5)

 Finds immediate wins, blocks threats, avoids blunders
 Depth-limited, no guarantee of optimality

---

## 7. Limitations & Future Work

 Full Minimax impractical beyond 3×3; depth limiting required
 Heuristic misses deep tactics; no opening/endgame database
 No transposition table, iterative deepening, or parallel search
* No real-time move guarantees

