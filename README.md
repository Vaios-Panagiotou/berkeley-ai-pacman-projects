# UC Berkeley CS188: Pacman AI Projects

This repository contains my solutions for UC Berkeley's CS188 - Introduction to Artificial Intelligence programming projects. Each project covers a different area of artificial intelligence, ranging from search algorithms to adversarial agents and constraint satisfaction problems.

---

## Project 0: Python Tutorial

**Goal:** Familiarize with Python and the project structure.

**Files:**
- `buyLotsOfFruit.py`: Calculates the total cost of fruit orders.
- `shopSmart.py`: Finds the grocery store with the lowest total cost for an order.

---

## Project 1: Search

**Focus:** Implement graph search algorithms to navigate Pacman through mazes.

**Files:**
- `search.py`: Core logic for the search algorithms.
- `searchAgents.py`: Applications of the search algorithms.

**Algorithms:**
| Algorithm | Description |
|-----------|-------------|
| **DFS**   | Depth-First Search: Explores as far as possible along each branch before backtracking. Uses a Stack. |
| **BFS**   | Breadth-First Search: Explores all nodes at the current depth before moving deeper. Uses a Queue. Guarantees shortest path. |
| **UCS**   | Uniform Cost Search: Expands the least-cost node using a PriorityQueue. Finds minimum-cost path. |
| **A\***    | Combines path cost `g(n)` and heuristic estimate `h(n)` for optimal path. Uses a PriorityQueue. |

**Key Problems:**
- **Corners Problem:**  
    Find the shortest path visiting all four corners.  
    *State:* `(position, visited_corners)`  
    *Heuristic:* Sum of Manhattan distances to nearest unvisited corner.

- **Food Search Problem:**  
    Find the optimal path for Pacman to eat all food pellets.  
    *State:* `(position, foodGrid)`  
    *Heuristic:* `mazeDistance` to farthest remaining food dot.

**Running the code:**
```bash
python autograder.py -q q1
```

---

## Project 2: Multi-Agent Search

**Focus:** Adversarial search where Pacman competes against ghosts.

**File:** `multiAgents.py`

**Agents:**
| Agent | Description |
|-------|-------------|
| **Reflex Agent** | Chooses actions based on heuristic evaluation (food proximity, ghost distance, scared timers). |
| **Minimax Agent** | Minimax algorithm, assuming ghosts act optimally.<br> - `max-value`: Pacman’s move (maximize score)<br> - `min-value`: Ghosts’ move (minimize score) |
| **Alpha-Beta Agent** | Optimized Minimax with alpha-beta pruning.<br> - `α`: Best score for Pacman<br> - `β`: Best score for ghosts<br> - Prunes when `α ≥ β` |
| **Expectimax Agent** | Models ghosts as stochastic agents.<br> - `max-value`: Pacman’s decision<br> - `exp-value`: Expected score of all possible ghost moves |

**Evaluation Function Weights:**  
- Distance to nearest food
- Number of remaining pellets
- Distance to active ghosts (penalized)
- Time remaining on scared ghosts (rewarded)

**Running the code:**
```bash
python autograder.py -q q1
```

---

## Project 3: Constraint Satisfaction Problems (CSP)

**Setup:**
- **Variables:** Radio links requiring frequencies
- **Domains:** Available frequency values
- **Constraints:** Absolute differences between linked frequencies (e.g., `|f₁ - f₂| > k`)

**Algorithms & Heuristics:**
| Algorithm | Description |
|-----------|-------------|
| **Forward Checking (FC)** | After each assignment, prunes inconsistent values from neighbors. |
| **Maintaining Arc Consistency (MAC)** | Uses AC-3 to enforce global consistency after each step. |
| **FC with Conflict-Directed Backjumping (FC-CBJ)** | On conflict, jumps back to source variable rather than backtracking one level. |
| **Min-Conflicts** | Starts with full assignment, iteratively reduces conflicts by changing problematic variable. |

**Variable Ordering Heuristic:**
- **Dom/Wdeg:** Chooses variable with smallest ratio of domain size to weighted degree (`dom / wdeg`). Constraint weights increase with each conflict.

**Running the code:**
```bash
# Solve instance 2-f24 using FC-CBJ
python main.py 2-f24 FC-CBJ

# Solve instance graph-11 using Min-Conflicts
python main.py graph-11 Min-Conflicts
```

---

## Summary

| Project | Topic                | Focus                              |
|---------|----------------------|------------------------------------|
| 0       | Python Tutorial      | Environment setup & basic Python   |
| 1       | Search               | Graph search algorithms            |
| 2       | Multi-Agent Search   | Adversarial agents                 |
| 3       | CSP                  | Constraint satisfaction problems   |

---

*For more details, see individual project folders and code comments.*
