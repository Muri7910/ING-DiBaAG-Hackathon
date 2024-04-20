from pysat.formula import CNF
from pysat.solvers import Glucose3

# Define the k-SAT problem
# Example: (x1 OR x2 OR NOT x3) AND (NOT x1 OR NOT x2 OR x3)
k_sat_problem = [[1],[1,3], [-2], [-4], [3,4]]

# Create a CNF formula
formula = CNF()

# Add clauses to the CNF formula
for clause in k_sat_problem:
    formula.append(clause)

# Initialize the solver (Glucose3 solver in this case)
solver = Glucose3()

# Add the CNF formula to the solver
solver.append_formula(formula.clauses)

# Solve the k-SAT problem
solution = solver.solve()

if solution:
    # If a solution is found, get the variable assignments
    variable_assignments = solver.get_model()
    print("Satisfying assignment:", variable_assignments)
else:
    print("No solution found.")