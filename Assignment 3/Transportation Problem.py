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
          j = np.argmin([cost_matrix[i, k] if active_cols[k] and demand[k] > 0 else float('inf') for k in range(len(demand))])
     else:
          j = col_index
          i = np.argmin([cost_matrix[k, j] if active_rows[k] and supply[k] > 0 else float('inf') for k in range(len(supply))])

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
          return "The method is not applicable due to negative values!"

     # Check if the problem is balanced
     if not check_balance(supply, demand):
          return "The problem is not balanced!"

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



# Example inputs
S = [20, 30, 25]  # Supply
C = [[19, 30, 50, 10],
     [70, 30, 40, 60],
     [40, 8, 70, 20]]  # Cost matrix
D = [15, 35, 5, 20]  # Demand

# Run the function and get the allocation matrix
allocation = vogel_approximation(S, C, D)

# Adjust Pandas display options to show all values
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

# Print the final allocation matrix
print("Vogel Approximation:")
allocation_df = pd.DataFrame(allocation, columns=[f'Demand {i+1}' for i in range(len(D))], index=[f'Supply {i+1}' for i in range(len(S))])
print(allocation_df)
