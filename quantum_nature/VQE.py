import matplotlib.pyplot as plt
import numpy as np

import qiskit_algorithms
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.minimum_eigensolvers import VQE, NumPyMinimumEigensolver, MinimumEigensolverResult
from qiskit.primitives import Estimator

from qiskit_nature import settings
from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import ParityMapper
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer

settings.tensor_unwrapping = False
settings.use_pauli_sum_op = False

# create molecule
driver = PySCFDriver(atom='Li 0 0 0; H 0 0 1.3', basis='sto3g')

# get second quantized Hamiltonian
problem = driver.run()
hamiltonian = problem.hamiltonian.second_q_op()

# map to qubit Hamiltonian
qubit_mapper = ParityMapper(num_particles=problem.num_particles)
qubit_hamiltonian = qubit_mapper.map(hamiltonian)
print(qubit_hamiltonian.num_qubits)

# activate space transformer
active_space_transformer = ActiveSpaceTransformer(num_electrons=2, num_spatial_orbitals=3)
as_problem = active_space_transformer.transform(problem)
as_hamiltonian = qubit_mapper.map(as_problem.hamiltonian.second_q_op())
print(as_hamiltonian.num_qubits)

# exact solution
exact_solver = NumPyMinimumEigensolver()
exact_result = exact_solver.compute_minimum_eigenvalue(as_hamiltonian)
print(exact_result)

# ---------------------------------------------------------------------
# VQE in practice
# ---------------------------------------------------------------------

# setup ansatz
initial_state = HartreeFock(
    num_spatial_orbitals=problem.num_spatial_orbitals,
    num_particles=problem.num_particles,
    qubit_mapper=qubit_mapper
)

ansatz = UCCSD(
    num_spatial_orbitals=problem.num_spatial_orbitals,
    num_particles=problem.num_particles,
    qubit_mapper=qubit_mapper,
    initial_state=initial_state
)

# setup optimizer
optimizer = COBYLA(maxiter=2500)
energies = []
def callback(nfew, x, fx, *args):
    energies.append(fx)

# Setup VQE
estimator = Estimator()
vqe_solver = VQE(estimator, ansatz, optimizer, callback=callback)
result = vqe_solver.compute_minimum_eigenvalue(qubit_hamiltonian)
result = problem.interpret(result)
vqe_energy = result.total_energies[0]

