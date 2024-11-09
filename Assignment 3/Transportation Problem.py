import numpy as np
import pandas as pd


def check_balance(supply, demand):
    """
    Check if the transportation problem is balanced.
    """
    return sum(supply) == sum(demand)


def check_non_negative(supply, demand, cost_matrix):
    """
    Check if the supply, demand, and cost matrix contain any negative values.
    """
    if any(s < 0 for s in supply):
        return False
    if any(d < 0 for d in demand):
        return False
    if np.any(cost_matrix < 0):
        return False
    return True


def calculate_row_penalties(supply, demand, cost_matrix, active_rows, active_cols):
    """
    Calculate penalties for each active row.
    """
    row_penalties = []
    for i in range(len(supply)):
        if active_rows[i] and supply[i] > 0:
            sorted_row = np.sort([cost_matrix[i, j] for j in range(len(demand)) if active_cols[j] and demand[j] > 0])
            penalty = sorted_row[1] - sorted_row[0] if len(sorted_row) > 1 else sorted_row[0]
            row_penalties.append((penalty, i))
    return row_penalties


def calculate_col_penalties(supply, demand, cost_matrix, active_rows, active_cols):
    """
    Calculate penalties for each active column.
    """
    col_penalties = []
    for j in range(len(demand)):
        if active_cols[j] and demand[j] > 0:
            sorted_col = np.sort([cost_matrix[i, j] for i in range(len(supply)) if active_rows[i] and supply[i] > 0])
            penalty = sorted_col[1] - sorted_col[0] if len(sorted_col) > 1 else sorted_col[0]
            col_penalties.append((penalty, j))
    return col_penalties


def find_max_penalty(row_penalties, col_penalties):
    """
    Determine the maximum penalty and whether it is from a row or a column.
    """
    # Find maximum row penalty
    max_row_penalty = 0
    row_index = -1
    for penalty, i in row_penalties:
        if penalty > max_row_penalty:
            max_row_penalty = penalty
            row_index = i

    # Find maximum column penalty
    max_col_penalty = 0
    col_index = -1
    for penalty, j in col_penalties:
        if penalty > max_col_penalty:
            max_col_penalty = penalty
            col_index = j

    # Determine whether the maximum penalty is from a row or a column
    if max_row_penalty >= max_col_penalty:
        return 'row', row_index
    else:
        return 'col', col_index


def allocate_supply_demand(supply, demand, cost_matrix, active_rows, active_cols, row_index, col_index):
    """
    Allocate the minimum of supply and demand based on the chosen row or column index.
    """
    if row_index != -1:
        i = row_index
        j = np.argmin(
            [cost_matrix[i, k] if active_cols[k] and demand[k] > 0 else float('inf') for k in range(len(demand))])
    else:
        j = col_index
        i = np.argmin(
            [cost_matrix[k, j] if active_rows[k] and supply[k] > 0 else float('inf') for k in range(len(supply))])

    min_val = min(supply[i], demand[j])
    supply[i] -= min_val
    demand[j] -= min_val

    return i, j, min_val


def update_active_status(supply, demand, i, j, active_rows, active_cols):
    """
    Deactivate row or column if the supply or demand is exhausted.
    """
    if supply[i] == 0:
        active_rows[i] = False
    if demand[j] == 0:
        active_cols[j] = False


def vogel_approximation(S, C, D):
    """
    Main function for Vogel's Approximation Method.
    """
    supply = S.copy()
    demand = D.copy()
    cost_matrix = np.array(C)
    allocation = np.zeros_like(cost_matrix, dtype=float)

    # Check if the method is applicable (no negative values)
    if not check_non_negative(supply, demand, cost_matrix):
        print("The method is not applicable due to negative values!")
        raise Exception

    # Check if the problem is balanced
    if not check_balance(supply, demand):
        print("The problem is not balanced!")
        raise Exception

    active_rows = [True] * len(supply)
    active_cols = [True] * len(demand)

    while sum(supply) > 0 and sum(demand) > 0:
        row_penalties = calculate_row_penalties(supply, demand, cost_matrix, active_rows, active_cols)
        col_penalties = calculate_col_penalties(supply, demand, cost_matrix, active_rows, active_cols)

        penalty_type, index = find_max_penalty(row_penalties, col_penalties)

        if penalty_type == 'row':
            i, j, min_val = allocate_supply_demand(supply, demand, cost_matrix, active_rows, active_cols, index, -1)
        else:
            i, j, min_val = allocate_supply_demand(supply, demand, cost_matrix, active_rows, active_cols, -1, index)

        allocation[i, j] = min_val
        update_active_status(supply, demand, i, j, active_rows, active_cols)

    return allocation


def largest_costs_in_rows(cost_matrix, active_rows, active_cols):
    u = [None] * len(cost_matrix)
    for i in range(len(cost_matrix)):
        if active_rows[i]:
            u[i] = max([cost_matrix[i][j] for j in range(len(cost_matrix[i])) if active_cols[j]])
    return u


def largest_costs_in_cols(cost_matrix, active_rows, active_cols):
    cost_matrix = cost_matrix.T
    v = [None] * len(cost_matrix)
    for i in range(len(cost_matrix)):
        if active_cols[i]:
            v[i] = max([cost_matrix[i][j] for j in range(len(cost_matrix[i])) if active_rows[j]])
    return v


def compute_reduced_cost(cost_matrix, u, v, active_rows, active_cols):
    costs = np.array([[None] * len(active_cols) for _ in range(len(active_rows))])
    for i in range(len(u)):
        for j in range(len(v)):
            if active_rows[i] and active_cols[j]:
                costs[i][j] = cost_matrix[i][j] - (u[i] + v[j])
    return costs


def find_min_number(matrix):
    i = j = -1
    min_num = 1000000
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y]:
                if matrix[x][y] < min_num:
                    i = x
                    j = y
                    min_num = matrix[x][y]
    return i, j

def russel_approximation(S, C, D):
    """
    Main function for Russel's Approximation Method.
    """
    supply = S.copy()
    demand = D.copy()
    cost_matrix = np.array(C)
    allocation = np.zeros_like(cost_matrix, dtype=float)

    # Check if the method is applicable (no negative values)
    if not check_non_negative(supply, demand, cost_matrix):
        print("The method is not applicable due to negative values!")
        raise Exception

    # Check if the problem is balanced
    if not check_balance(supply, demand):
        print("The problem is not balanced!")
        raise Exception

    active_rows = [True] * len(supply)
    active_cols = [True] * len(demand)

    while sum(supply) > 0 and sum(demand) > 0:
        U = largest_costs_in_rows(cost_matrix, active_rows, active_cols)
        V = largest_costs_in_cols(cost_matrix, active_rows, active_cols)

        reduced_cost = compute_reduced_cost(cost_matrix, U, V, active_rows, active_cols)
        i, j = find_min_number(reduced_cost)
        alloc = min(supply[i], demand[j])
        allocation[i, j] = alloc
        supply[i] -= alloc
        demand[j] -= alloc
        update_active_status(supply, demand, i, j, active_rows, active_cols)

    return allocation


for n in range(1, 4):
    data = open(f"tests/input{n}.txt", "r").readlines()

    c = np.array([float(j) for j in data[0].split()], float)
    A = np.array([[float(j) for j in row.split()] for row in data[1:-3]], float)
    x = np.array([float(j) for j in data[-3].split()], float)
    b = np.array([float(j) for j in data[-2].split()], float)

    # Example inputs
    S = [int(j) for j in data[0].split()]  # Supply
    C = [[int(i) for i in j.split()] for j in data[1:len(S) + 1]]  # Cost matrix
    D = [int(j) for j in data[len(S) + 1].split()]  # Demand

    print(f"Input №{n}")
    try:
        print("\nVogel Approximation:")
        # Run the function and get the allocation matrix
        allocation = vogel_approximation(S, C, D)

        # Adjust Pandas display options to show all values
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 1000)

        # Print the final allocation matrix

        allocation_df = pd.DataFrame(allocation, columns=[f'Demand {i + 1}' for i in range(len(D))],
                                     index=[f'Supply {i + 1}' for i in range(len(S))])
        print(allocation_df)
    except Exception:
        pass

    try:
        print("\nRussel Approximation:")
        # Run the function and get the allocation matrix
        allocation = russel_approximation(S, C, D)

        # Adjust Pandas display options to show all values
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 1000)

        # Print the final allocation matrix

        allocation_df = pd.DataFrame(allocation, columns=[f'Demand {i + 1}' for i in range(len(D))],
                                     index=[f'Supply {i + 1}' for i in range(len(S))])
        print(allocation_df)
    except Exception:
        pass
    print("\n")
