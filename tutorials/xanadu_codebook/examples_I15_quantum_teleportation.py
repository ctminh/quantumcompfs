import pennylane as qml
import numpy as np

# -----------------------------------------------------
# Quantum teleportation
# -----------------------------------------------------

dev = qml.device('default.qubit', wires=3)

def state_preparation():

    # OPTIONALLY UPDATE THIS STATE PREPARATION ROUTINE
    qml.Hadamard(wires=0)
    qml.Rot(0.1, 0.2, 0.3, wires=0)

@qml.qnode(dev)
def state_prep_only():
    state_preparation()
    return qml.state()
    
print('-----------------------------------------------')
print('State_preparation:')
print(state_prep_only())
print('-----------------------------------------------\n')

def entangle_qubits():

    # ENTANGLE THE SECOND QUBIT (WIRES=1) AND THE THIRD QUBIT
    qml.Hadamard(wires=1)
    qml.CNOT(wires=[1,2])

def rotate_and_controls():

    # PERFORM THE BASIS ROTATION
    qml.CNOT(wires = [0,1])
    qml.Hadamard(wires = 0)

    # PERFORM THE CONTROLLED OPERATIONS
    qml.CNOT(wires = [1,2])
    qml.CZ(wires = [0,2])

@qml.qnode(dev)
def teleportation():

    # USE YOUR QUANTUM FUNCTIONS TO IMPLEMENT QUANTUM TELEPORTATION
    state_preparation()
    entangle_qubits()
    rotate_and_controls()

    # RETURN THE STATE
    return qml.state()

print('-----------------------------------------------')
print('Quantum teleportation:')
print(teleportation())
print('-----------------------------------------------\n')

def extract_qubit_state(input_state):
    """Extract the state of the third qubit from the combined state after teleportation.
    
    Args:
        input_state (array[complex]): A 3-qubit state of the form 
            (1/2)(|00> + |01> + |10> + |11>) (a|0> + b|1>)
            obtained from the teleportation protocol.
            
    Returns:
        array[complex]: The state vector np.array([a, b]) of the third qubit.
    """

    a = 2 * input_state[0]
    b = 2 * input_state[1]
    
    return np.array([a,b])

# OPTIONALLY UPDATE THIS STATE PREPARATION ROUTINE
def state_preparation():
    qml.Hadamard(wires=0)
    qml.Rot(0.1, 0.2, 0.3, wires=0)


@qml.qnode(dev)
def teleportation():
    state_preparation()
    entangle_qubits()
    rotate_and_controls()    
    return qml.state()

# Print the extracted state after teleportation
print('-----------------------------------------------')
print('Extracting the state after teleportation:')
full_state = teleportation()
print(extract_qubit_state(full_state))
print('-----------------------------------------------\n')
