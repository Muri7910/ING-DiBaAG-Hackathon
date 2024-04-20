from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler

# Define the k-SAT problem
# Example: (x1 OR x2 OR NOT x3) AND (NOT x1 OR NOT x2 OR x3)
#k_sat_problem = [[1, 2, -3], [-1, -2, 3]]
k_sat_problem = [[1],[1,3], [-2], [-4], [3,4]]

# Define the Ising Hamiltonian
ising_model = BinaryQuadraticModel.from_ising({}, {(i, i): 0 for i in range(1, 4)})
for clause in k_sat_problem:
   # linear, quadratic = BinaryQuadraticModel.from_ising({}, {(var, var): 0 for var in clause})
   # ising_model.update(linear, quadratic)
   ising_model.update(BinaryQuadraticModel.from_ising({}, {(var, var): 0 for var in clause}))

# Run Simulated Quantum Annealing
sampler = LeapHybridSampler()
response = sampler.sample_ising(ising_model.linear, ising_model.quadratic)

# Obtain samples
samples = list(response.samples())

# Post-processing: Convert the samples to a readable format
def decode_solution(sample):
    return [sample[var] for var in range(1, 4)]

solutions = [decode_solution(sample) for sample in samples]

print("Solutions found:")
for solution in solutions:
    print(solution)
