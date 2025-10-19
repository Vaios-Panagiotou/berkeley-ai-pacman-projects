# 🎮 UC Berkeley CS188: Pacman AI Projects

Welcome! This repository contains my solutions for UC Berkeley’s CS188 - Introduction to Artificial Intelligence programming projects. Each project explores a different area of AI, from search algorithms to adversarial agents and constraint satisfaction problems.

---

## 🐍 Project 0: Python Tutorial

**Goal:** Get familiar with Python and the Pacman project structure.

**Implemented Files:**
- `buyLotsOfFruit.py` – Computes the total cost of a list of fruit orders.
- `shopSmart.py` – Determines which grocery store offers the lowest total cost for a given order.

---

## 🧠 Project 1: Search

**Focus:** Implement classic graph search algorithms to help Pacman navigate mazes efficiently.

**Core Files:**
- `search.py` – Core logic for search algorithms.
- `searchAgents.py` – Applications of search algorithms.

**Algorithms Implemented:**
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
    *Heuristic:* Sum of Manhattan distances to nearest unvisited corner (admissible & consistent).

- **Food Search Problem:**  
    Find optimal path for Pacman to eat all food pellets.  
    *State:* `(position, foodGrid)`  
    *Heuristic:* `mazeDistance` to farthest remaining food dot (admissible lower bound).

**How to Run:**
```bash
python autograder.py -q q1
```

---

## 👻 Project 2: Multi-Agent Search

**Focus:** Adversarial search—Pacman competes against intelligent ghosts.

**Core File:** `multiAgents.py`

**Agents Implemented:**
| Agent | Description |
|-------|-------------|
| **Reflex Agent** | Chooses actions based on heuristic evaluation (food proximity, ghost distance, scared timers, etc.). |
| **Minimax Agent** | Implements Minimax algorithm, assuming ghosts act optimally.<br> - `max-value`: Pacman’s move (maximize score)<br> - `min-value`: Ghosts’ move (minimize score) |
| **Alpha-Beta Agent** | Optimized Minimax with alpha-beta pruning.<br> - `α`: Best score for Pacman<br> - `β`: Best score for ghosts<br> - Prunes when `α ≥ β` |
| **Expectimax Agent** | Models ghosts as stochastic agents.<br> - `max-value`: Pacman’s decision<br> - `exp-value`: Expected score of all possible ghost moves |

**Enhanced Evaluation Function:**  
Weighted evaluation considering:
- Distance to nearest food
- Number of remaining pellets
- Distance to active ghosts (penalized)
- Time remaining on scared ghosts (rewarded)

**How to Run:**
```bash
python autograder.py -q q1
```

---

## ⚙️ Project 3: Constraint Satisfaction Problems (CSP)

**Problem Setup:**
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

**How to Run:**
```bash
# Solve instance 2-f24 using FC-CBJ
python main.py 2-f24 FC-CBJ

# Solve instance graph-11 using Min-Conflicts
python main.py graph-11 Min-Conflicts
```

---

## 🧭 Summary

| Project | Topic                | Focus                              |
|---------|----------------------|------------------------------------|
| 0       | Python Tutorial      | Environment setup & basic Python   |
| 1       | Search               | Graph search algorithms            |
| 2       | Multi-Agent Search   | Adversarial agents                 |
| 3       | CSP                  | Constraint satisfaction problems   |

---

*For more details, see individual project folders and code comments.*
