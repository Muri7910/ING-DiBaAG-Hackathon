from qiskit import Aer, QuantumCircuit, transpile, assemble
from qiskit.aqua.algorithms import QAOA
from qiskit.optimization.applications import sat
from qiskit.optimization.algorithms import MinimumEigenOptimizer

# Define the k-SAT problem
# Example: (x1 OR x2 OR NOT x3) AND (NOT x1 OR NOT x2 OR x3)
k_sat_problem = [[1, 2, -3], [-1, -2, 3]]
#formula = """
#    ( (x1) and (x1 or x3) and (not x2) and (not x4) and (x3 or x4) )
#"""
#[[1],[1,3], [-2], [-4], [3,4]]

# Map the k-SAT problem to an Ising Hamiltonian
qubit_op, offset = sat.sat_to_ising(k_sat_problem)

# Define the QAOA instance
qaoa = QAOA(qubit_op, optimizer=None, p=1)

# Define the minimum eigen optimizer
optimizer = MinimumEigenOptimizer(qaoa)

# Solve the k-SAT problem
result = optimizer.solve()

# Post-processing: Convert the result to a readable format
solution = sat.sample_to_solution(result.samples[0])

print("Optimal solution:", solution)