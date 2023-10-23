import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)

U = np.array([[1, 1], [1, -1]]) / np.sqrt(2)

@qml.qnode(dev)
def apply_u():

    # Use QubitUnitary to apply U to the qubit
    qml.QubitUnitary(U, wires=0)

    # Return the state
    return qml.state()

print('-----------------------------------------------')
print("Aplly U gate with QubitUnitary: ")
outcome = apply_u()
print(outcome)
print('-----------------------------------------------\n')



