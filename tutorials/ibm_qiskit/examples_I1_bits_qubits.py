import numpy as np
import matplotlib.pyplot as plt

from numpy import array
from numpy import matmul

from IPython.display import display

from qiskit.quantum_info import Statevector
from qiskit.quantum_info import Operator
from qiskit.visualization import plot_histogram

from math import sqrt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.quantum_info.operators.predicates import matrix_equal

simulator = Aer.get_backend('statevector_simulator')

qc211 = QuantumCircuit(1)
qc211.h(0)
qc211.s(0)

assert set(g.__class__.__name__ for g, _, _ in list(qc211)).issubset({'_SingletonHGate', '_SingletonSGate'}), ('You may only use H and S gates for this problem')

simulator = Aer.get_backend('statevector_simulator')
test_states = {
    '+': [1/sqrt(2), 1/sqrt(2)], '-': [1/sqrt(2), -1/sqrt(2)],
    'i': [1/sqrt(2), 1j/sqrt(2)], '-i': [1/sqrt(2), -1j/sqrt(2)],
    '0': [1, 0], '1': [0, 1],
}
expected_transform = {
    '+': '0', 'i': '+', '0': 'i',
    '-': '1', '-i': '-', '1': '-i',
}
invalid = False

for input_name, output_name in expected_transform.items():

    print(f'Testing input |{input_name}> with expected output |{output_name}>...')

    # Simulate
    qc_test = QuantumCircuit(1)
    qc_test.initialize(test_states[input_name], 0)
    qc_test &= qc211
    state = execute(qc_test, simulator).result().get_statevector() # execute circuit
    state_name = str(state)

    for comp_name, comp_state in test_states.items():
        if matrix_equal(state, comp_state, ignore_phase=True, atol=1e-8, rtol=1e-8):
            state_name = comp_name

    if state_name == output_name:
        print(f'Correct:   |{input_name:>2}> -> |{output_name:>2}>')
    else:
        invalid = True
        print(f'Incorrect: |{input_name:>2}> -> |{state_name:>2}> (expected {output_name:>2})')

assert not invalid, 'At least one output of your circuit is wrong.'