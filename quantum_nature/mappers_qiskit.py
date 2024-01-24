from qiskit_nature.second_q.operators import FermionicOp
from qiskit_nature.second_q.mappers import JordanWignerMapper
import qiskit_nature

qiskit_nature.settings.use_pauli_sum_op = False

op = FermionicOp({"+_1 -_2": 1.0}, num_spin_orbitals=4)
print(op)

mapper = JordanWignerMapper()
qop = mapper.map(op)
print(qop)