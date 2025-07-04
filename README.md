# KenKenSolver

A Python-based solver for KenKen puzzles, implementing both Backtracking and Constraint Satisfaction Problem (CSP) algorithms to solve puzzles of varying sizes. This project is part of the Artificial Intelligence course assignment (First Practical Series) under Dr. Mohammadi.

## Overview

KenKen (also known as Calcudoku) is a logic-based number puzzle similar to Sudoku but with a mathematical twist. Introduced by Japanese mathematician Tetsuya Miyamoto, KenKen involves filling a square grid with numbers that satisfy arithmetic constraints within "cages." This solver generates random KenKen puzzles and solves them using two methods: Backtracking and CSP.

### Rules of KenKen
1. **Unique Numbers**: Each row and column in an NxN grid must contain unique numbers from 1 to N (e.g., 1, 2, 3, 4 for a 4x4 grid).
2. **Cages**: The grid is divided into non-overlapping cages, each with a target number and an arithmetic operation (+, -, *, /). Numbers in the cage must combine to meet the target using the specified operation.
   - **Addition (+)**: Sum of numbers equals the target.
   - **Subtraction (-)**: Absolute difference between two numbers equals the target (used for two-cell cages).
   - **Multiplication (*)**: Product of numbers equals the target.
   - **Division (/)**: Division of the larger number by the smaller equals the target (used for two-cell cages).
3. **Goal**: Fill the grid such that all row, column, and cage constraints are satisfied.

## Features
- Generates random KenKen puzzles of sizes NxN (e.g., 4x4 to 7x7).
- Solves puzzles using two algorithms:
  - **Backtracking**: Recursively assigns numbers and backtracks on invalid assignments.
  - **Constraint Satisfaction Problem (CSP)**: Uses domain constraints for each cell, checking row, column, and cage constraints.
- Includes helper functions to ensure valid number placement and cage constraint satisfaction.
- Performance analysis comparing execution times of both algorithms across multiple runs.

## Installation

### Prerequisites
- Python 3.8+
- Required libraries: `numpy` (for matrix operations and random generation)
- Jupyter Notebook (for running the provided notebook)

### Setup
 1. Clone the repository:
	   ```bash
	   git clone https://github.com/saeedvft/KenKenSolver.git
	   cd KenKenSolver
	```
 2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
 3. Ensure Jupyter Notebook is installed:
	 ```bash
	pip install jupyter
	```
### Usage
- **Generate a Puzzle:**
Run the notebook or script to generate a random KenKen puzzle:
	```bash
	jupyter notebook KenKenSolver.ipynb
	```
	The generate_KenKen function creates an NxN grid initialized with zeros, fills it with numbers using fill_grid_with_numbers, and defines random cages using generate_random_cages.
	
- **Solve a Puzzle:**
	Use the Backtracking or CSP solver functions to solve the puzzle. Example:
	 ```bash
	from kenken_solver import solve_kenken_backtracking, solve_kenken_csp
	grid, cages = generate_KenKen(size=4)
	solve_kenken_backtracking(grid, cages)  # or solve_kenken_csp(grid, cages)
	```
- **Performance Analysis:**
	Run the notebook to execute both solvers multiple times (at least twice for sizes 4 to 7) and compute the mean and variance of execution times. Results are displayed in a table.

## Implementation Details

#### Puzzle Generation

-   generate_KenKen(size): Creates an NxN grid and random cages.
-   fill_grid_with_numbers(grid): Uses backtracking to fill the grid with unique numbers per row and column.
-   is_safe_to_place(grid, row, col, num): Checks if a number can be placed in a cell without violating row/column uniqueness.
-   fill_grid_backtracking(grid): Implements backtracking to fill the grid.
-   generate_random_cages(grid): Provided function to create random cages (not implemented by the user).
-   calculate_target(cage, grid): Computes the target value for a cage based on its operation and numbers.

#### Backtracking Solver

-   find_unassigned_location(grid): Returns the coordinates of an empty cell (returns (-1, -1) if none).
-   solve_kenken_backtracking(grid, cages): Solves the puzzle by assigning numbers and backtracking when constraints are violated.

#### CSP Solver

-   solve_kenken_csp(grid, cages): Assigns values to cells from their domains, enforcing row, column, and cage constraints using constraint propagation and backtracking.
