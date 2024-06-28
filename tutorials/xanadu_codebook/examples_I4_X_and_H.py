import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)

U = np.array([[1, 1], [1, -1]]) / np.sqrt(2)

# -----------------------------------------------------
# Varying the initial state of a qubit by PauliX
# -----------------------------------------------------

@qml.qnode(dev)
def varied_initial_state(state):

    # initialzie a qubit in state 0
    qml.QubitStateVector([1, 0], wires=0)

    # if state is 1, then flipping the initial qubit
    if state == 1:
        qml.PauliX(wires=0)

    # APPLY U TO THE STATE
    qml.QubitUnitary(U, wires=0)

    return qml.state()

print('-----------------------------------------------')
print("Vary the initial state of a qubit and apply U gate with QubitUnitary: ")
state = 1
outcome = varied_initial_state(state)
print(outcome)
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Applying Hadamard gate
# -----------------------------------------------------
dev = qml.device("default.qubit", wires=1)

@qml.qnode(dev)
def apply_hadamard():

    qml.Hadamard(0)
    
    return qml.state()

print('-----------------------------------------------')
print("Applying hamadard gate: ")
outcome = apply_hadamard()
print(outcome)
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Applying Hadamard gate
# -----------------------------------------------------

@qml.qnode(dev)
def apply_hadamard_to_state(state):
    """Complete the function such that we can apply the Hadamard to
    either |0> or |1> depending on the input argument flag.
    
    Args:
        state (int): Either 0 or 1. If 1, prepare the qubit in state |1>,
            otherwise, leave it in state 0.
    
    Returns:
        array[complex]: The state of the qubit after the operations.
    """

    # KEEP THE QUBIT IN |0> OR CHANGE IT TO |1> DEPENDING ON state
    qml.QubitStateVector([1, 0], wires=0)

    # if state is 1, then flipping the initial qubit
    if state == 1:
        qml.PauliX(wires=0)

    # APPLY THE HADAMARD
    apply_hadamard()
    
    # RETURN THE STATE
    return qml.state()

print('-----------------------------------------------')
print("Applying hamadard to the state: ")
print("  + State 0:")
print(apply_hadamard_to_state(0))
print("  + State 1:")
print(apply_hadamard_to_state(1))
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Creating a simple circuit
# -----------------------------------------------------

dev = qml.device("default.qubit", wires=1)
@qml.qnode(dev)
def apply_hxh(state):
    
    qml.QubitStateVector([1, 0], wires=0)
    if state == 1:
        qml.PauliX(0)
    
    qml.Hadamard(0)
    qml.PauliX(0)
    qml.Hadamard(0)

    return qml.state()

print('-----------------------------------------------')
print("Applying the HXH circuit: ")
print("  + State 0:")
print(apply_hxh(0))
print("  + State 1:")
print(apply_hxh(1))
print('-----------------------------------------------\n')

