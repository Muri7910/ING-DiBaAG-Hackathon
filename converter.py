from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
import numpy as np

# Define the k-SAT formula (example)
# For a 3-SAT problem with 3 variables and 2 clauses:
# (x1 OR x2 OR NOT x3) AND (NOT x1 OR NOT x2 OR x3)
# We can represent it as a list of clauses, each clause containing literals.
clauses =  [[1, 2, 3]]


# Function to generate the oracle for the k-SAT problem
def generate_oracle(clauses, num_qubits):
    oracle = QuantumCircuit(num_qubits)

    # Apply phase flip to solution states
    for clause in clauses:
        clause_circuit = QuantumCircuit(num_qubits)
        for literal in clause:
            if literal > 0:
                clause_circuit.cx(literal - 1, num_qubits - 1)
            else:
                clause_circuit.x(-literal - 1)
                clause_circuit.cx(-literal - 1, num_qubits - 1)
        oracle.append(clause_circuit.to_gate(), range(num_qubits))

    # Apply phase flip gate
    oracle.h(num_qubits - 1)
    oracle.x(num_qubits - 1)
    oracle.h(num_qubits - 1)

    return oracle


# Function to generate the Grover diffusion operator
def generate_diffusion(num_qubits):
    diffusion = QuantumCircuit(num_qubits)

    # Apply H gate to all qubits
    diffusion.h(range(num_qubits))

    # Apply X gate to all qubits
    diffusion.x(range(num_qubits))

    # Apply H gate to last qubit
    diffusion.h(num_qubits - 1)

    # Apply controlled Z gate (multi-controlled NOT)
    diffusion.mct(list(range(num_qubits - 1)), num_qubits - 1)

    # Apply H gate to last qubit
    diffusion.h(num_qubits - 1)

    # Apply X gate to all qubits
    diffusion.x(range(num_qubits))

    # Apply H gate to all qubits
    diffusion.h(range(num_qubits))

    return diffusion


# Function to perform the Grover iteration
def grover_iteration(oracle, diffusion, num_iterations):
    num_qubits = oracle.num_qubits
    grover_circuit = QuantumCircuit(num_qubits)

    # Apply Hadamard gates to all qubits
    grover_circuit.h(range(num_qubits))

    # Grover iteration
    for _ in range(num_iterations):
        grover_circuit.append(oracle, range(num_qubits))
        grover_circuit.append(diffusion, range(num_qubits))

    return grover_circuit


# Main function to run the Grover search algorithm
def grover_search(clauses, num_variables, num_iterations):
    num_qubits = num_variables + 1  # Number of qubits needed to represent the variables and the ancilla qubit

    # Create the oracle and diffusion operator
    oracle = generate_oracle(clauses, num_qubits)
    diffusion = generate_diffusion(num_qubits)

    # Create the Grover iteration circuit
    grover_circuit = grover_iteration(oracle, diffusion, num_iterations)

    # Measure the qubits to get the result
    grover_circuit.measure_all()

    # Simulate the circuit
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(grover_circuit, simulator)
    qobj = assemble(transpiled_circuit)
    result = simulator.run(qobj).result()
    counts = result.get_counts()

    return counts


# Example usage
num_variables = 3  # Number of variables in the k-SAT problem
num_iterations = 2  # Number of iterations for Grover's algorithm

counts = grover_search(clauses, num_variables, num_iterations)
print("Measurement results:", counts)
plot_histogram(counts)
