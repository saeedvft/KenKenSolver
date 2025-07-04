import time
import random


class Cage:
    def __init__(self, cells, operation, target):
        self.cells = cells
        self.operation = operation
        self.target = target

############################
#####generate KenKen########

def calculate_target(grid, cells, operation):
    if operation == '*':
        sum = 1
        for cell in cells:
            sum *= grid[cell[0]][cell[1]]
        return sum
    if operation == '+':
        sum = 0
        for cell in cells:
            sum += grid[cell[0]][cell[1]]
        return sum
    if operation == '-':
        sum = 0
        values = []
        for cell in cells:
            values.append(grid[cell[0]][cell[1]])
        if len(values) != 1:
            return max(values) - min(values)
        return values[0]
    if operation == '/':
        values = []
        for cell in cells:
            values.append(grid[cell[0]][cell[1]])
        if len(values) != 1:
            return max(values) / min(values)
        return values[0]
            

def generate_random_cages(grid, size):
    cages = []
    visited = [[False] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if not visited[i][j]:
                cage_size = random.randint(1, size)
                cells = [(i, j)]
                visited[i][j] = True

                while len(cells) < cage_size:
                    x, y = cells[-1]
                    neighbors = [(x + dx, y + dy) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]
                                 if 0 <= x + dx < size and 0 <= y + dy < size and not visited[x + dx][y + dy]]
                    if neighbors:
                        next_cell = random.choice(neighbors)
                        cells.append(next_cell)
                        visited[next_cell[0]][next_cell[1]] = True
                    else:
                        break

                operation = random.choice(['+', '*']) if cage_size > 2 else random.choice(['+', '-', '*', '/'])
                target = calculate_target(grid, cells, operation)
                cages.append(Cage(cells, operation, target))

    return cages


def is_valid(grid, row, col, number, size):
    for i in range(size):
        if grid[row][i] == number or grid[i][col] == number:
            return False
    return True

def fill_KenKen(grid, size):
    allowed_nums = [k + 1 for k in range(size)] 
    for i in range(size):
        for j in range(size):
            if grid[i][j] == 0:
                for _ in range(size):
                    number = random.choice(allowed_nums)
                    if is_valid(grid, i, j, number, size):
                        grid[i][j] = number
                        if fill_KenKen(grid, size):
                            return True
                        grid[i][j] = 0
                return False
    # If we reach here, the grid is successfully filled
    return True

def generate_KenKen(size):
    grid = [[0] * size for _ in range(size)]
    
    if fill_KenKen(grid, size):
        return grid
    else:
        return None
################################


################################
###solve KenKen backtracking####

def solve_kenken(grid, cages):
    size = len(grid)
    current_cell = find_unassigned_location(grid)
    cell_x = current_cell[0]
    cell_y = current_cell[1]
    if cell_x == -1:
        return True    
    
    for number in range(1, size + 1):
        if is_safe_kenken(grid, cell_x, cell_y, number, cages):
            grid[cell_x][cell_y] = number
            if solve_kenken(grid, cages):
                return True
            grid[cell_x][cell_y] = 0
    return False

def find_cage(cages, row, col):
    for cage in cages:
        if (row, col) in cage.cells:
            return cage
    return None 

def find_values(grid, cage):
    return [grid[i][j] for i,j in cage.cells if grid[i][j] != 0]

def is_safe_kenken(grid, row, col, num, cages):
    # Check row, column and cage numbers uniqueness
    for i in range(len(grid)):
        if grid[row][i] == num or grid[i][col] == num:
            return False
        
    curr_cage = find_cage(cages, row, col)
    grid[row][col] = num
    values = find_values(grid, curr_cage)
    if validate_cage_operation(curr_cage.operation, values, curr_cage.target, curr_cage):
        grid[row][col] = 0
        return True
    grid[row][col] = 0
    return False


def validate_cage_operation(operation, values, target, cage):
    if operation == '+':
        return sum(values) == target if len(values) == len(cage.cells) else sum(values) <= target
    elif operation == '*':
        product = 1
        for v in values:
            product *= v
        return product == target if len(values) == len(cage.cells) else product <= target
    elif operation == '-':
        if len(values) == len(cage.cells):
            if len(cage.cells) == 1:
                return values[0] == target
            return abs(values[0] - values[1]) == target
    elif operation == '/':
        if len(values) == len(cage.cells):
            if len(cage.cells) == 1:
                return values[0] == target
            return max(values) / min(values) == target
    return True


def find_unassigned_location(grid):
    # Find the first empty cell in the grid
    size = len(grid)
    for x in range(size):
        for y in range(size):
            if grid[x][y] == 0:
                return x, y
    return -1,-1
########################


############################
#####solve KenKen CSP#######
def solve_kenken_csp(grid, cages):
    """
    Function to solve the KenKen grid using Constraint Satisfaction Problem (CSP)
    """

    def create_domains(grid):
        """
        Function to create domains for each cell in the grid
        """
        size = len(grid)
        domains = {(i, j): set(range(1, size + 1)) for i in range(size) for j in range(size)}

        for cage in cages:
            for (i, j) in cage.cells:
                if cage.operation == '+':
                    domains[(i, j)] = set(range(1, size + 1))  # All numbers are possible
                elif cage.operation == '*':
                    domains[(i, j)] = {val for val in range(1, size + 1) if cage.target % val == 0}
                elif cage.operation in ('-', '/'):
                    domains[(i, j)] = set(range(1, size + 1))
        return domains

    def is_valid_assignment(i, j, val, assignment):
        """
        Checks if assigning a value to (i, j) is valid in terms of KenKen rules.
        """
        size = len(grid)

        # Row and Column uniqueness
        for k in range(size):
            if assignment.get((i, k)) == val or assignment.get((k, j)) == val:
                return False

        # Assign value to check cage constraints
        assignment[(i, j)] = val

        # Cage constraints
        for cage in cages:
            if (i, j) in cage.cells:
                values = [assignment.get((i, j)) for i, j in cage.cells if assignment.get((i, j)) != 0]
                
                if cage.operation == '+':
                    if len(values) == len(cage.cells) and sum(values) != cage.target:
                        assignment[(i, j)] = 0
                        return False
                    elif sum(values) > cage.target:
                        assignment[(i, j)] = 0
                        return False
                elif cage.operation == '*':
                    product = 1
                    for v in values:
                        product *= v
                    if len(values) == len(cage.cells) and product != cage.target:
                        assignment[(i, j)] = 0
                        return False
                    elif product > cage.target:
                        assignment[(i, j)] = 0
                        return False
                elif cage.operation == '-':
                    if len(values) == len(cage.cells):
                        if len(cage.cells) == 1:
                            if values[0] != cage.target:
                                assignment[(i, j)] = 0
                                return False
                        elif abs(values[0] - values[1]) != cage.target:
                            assignment[(i, j)] = 0
                            return False
                elif cage.operation == '/':
                    if len(values) == len(cage.cells):
                        if len(cage.cells) == 1:
                            if values[0] != cage.target:
                                assignment[(i, j)] = 0
                                return False
                        elif max(values) / min(values) != cage.target:
                            assignment[(i, j)] = 0
                            return False

        # Reset assignment before returning True
        assignment[(i, j)] = 0
        return True

    def update_domains(i, j, val, domains):
        """
        Function to update domains after an assignment
        """
        size = len(grid)
        new_domains = {k: v.copy() for k, v in domains.items()}  # Create a copy for backtracking

        # Remove assigned value from other cells in the same row and column
        for k in range(size):
            new_domains[(i, k)].discard(val)
            new_domains[(k, j)].discard(val)

        return new_domains

    def find_unassigned_location(assignment):
        """
        Function to find an unassigned location in the grid
        """
        for (i, j) in assignment:
            if assignment[(i, j)] == 0:
                return i, j
        return -1, -1

    def solve_csp(assignment, domains):
        """
        Recursive function to solve grid with CSP and domain updates
        """
        # Find an unassigned cell
        location = find_unassigned_location(assignment)
        if location[0] == -1:
            return True

        i, j = location
        for val in domains[(i, j)].copy():  # Work with a copy of domain values to avoid modification
            if is_valid_assignment(i, j, val, assignment):
                assignment[(i, j)] = val
                new_domains = update_domains(i, j, val, domains)  # Update domains for next step

                if solve_csp(assignment, new_domains):
                    return True

                # Backtrack: remove the assignment and restore domains
                assignment[(i, j)] = 0

        return False
    
    # Create initial domains for each cell in the grid
    domains = create_domains(grid)
    assignment = {(i, j): 0 for i in range(len(grid)) for j in range(len(grid))}

    # Solve the KenKen grid using CSP with domain updates
    if solve_csp(assignment, domains):
        solved_grid = [[assignment[(i, j)] for j in range(len(grid))] for i in range(len(grid))]
        return solved_grid
    else:
        return None


# Example Usage
for k in range(4):
    print(k)
    size = 6
    grid = generate_KenKen(size)
    if grid:
        for row in grid:
            print(row)
    else:
        print("No solution found")


    kenken_cages = generate_random_cages(grid, size)

    # print("Generated KenKen Cages:")
    # for cage in kenken_cages:
    #     print(f"Cage Cells: {cage.cells}, Operation: {cage.operation}, Target: {cage.target}")
    # print("-----------------------")

    backtrack_grid = [[0 for _ in range(size)] for _ in range(size)]
    start_time = time.time()
    if solve_kenken(backtrack_grid, kenken_cages):
        print("Solved KenKen Puzzle (BackTracking):")
        end_time = time.time()
        for row in backtrack_grid:
            print(row)
        execution_time = end_time - start_time
        print(f"Execution Time: {execution_time:.6f} seconds")
    else:
        print("No solution found using BackTracking.")
    # print("-----------------------")


    csp_grid = [[0 for _ in range(size)] for _ in range(size)]
    csp_start_time = time.time()
    solved_grid = solve_kenken_csp(csp_grid, kenken_cages)
    if solved_grid:
        print("Solved KenKen Puzzle (CSP):")
        csp_end_time = time.time()
        for row in solved_grid:
            print(row)
        execution_time = csp_end_time - csp_start_time
        print(f"Execution Time: {execution_time:.6f} seconds")
    else:
        print("No solution found using CSP.")
    print("-----------------------")
    solve_kenken_csp(csp_grid, kenken_cages)

    



