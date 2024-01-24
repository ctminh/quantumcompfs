import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)

# -----------------------------------------------------
# Varying the initial state of a qubit by PauliX
# -----------------------------------------------------

@qml.qnode(dev)
def apply_z_to_plus():
    """Write a circuit that applies PauliZ to the |+> state and returns
    the state.

    Returns:
        array[complex]: The state of the qubit after the operations.
    """

    # use hadamard to generate the |+> state
    qml.Hadamard(wires=0)
    # qml.QubitStateVector([1, 0], wires=0)
    # qml.QubitStateVector([0, 1], wires=0)

    # apply pauli Z
    qml.PauliZ(wires=0)

    # return the state
    return qml.state()

print('-----------------------------------------------')
print("Applying the HXH circuit: ")
print(apply_z_to_plus())
print('-----------------------------------------------\n')

# -----------------------------------------------------
# 
# -----------------------------------------------------

@qml.qnode(dev)
def fake_z():
    """Use RZ to produce the same action as Pauli Z on the |+> state.

    Returns:
        array[complex]: The state of the qubit after the operations.
    """

    # create the |+> state
    qml.Hadamard(wires=0)

    # apply RZ
    qml.RZ(np.pi, wires=0)

    # return the state
    return qml.state()

print('-----------------------------------------------')
print("Applying the RZ gate: ")
print(fake_z())
print('-----------------------------------------------\n')

# -----------------------------------------------------
# 
# -----------------------------------------------------

@qml.qnode(dev)
def many_rotations():
    """Implement the circuit depicted above and return the quantum state.

    Returns:
        array[complex]: The state of the qubit after the operations.
    """

    # IMPLEMENT THE CIRCUIT
    qml.Hadamard(wires=0)
    qml.S(wires=0)
    qml.adjoint(qml.T(wires=0))
    qml.RZ(0.3, wires=0)
    qml.adjoint(qml.S(wires=0))

    # RETURN THE STATE
    return qml.state()

print('-----------------------------------------------')
print("Applying many rotation: ")
print(many_rotations())
print('-----------------------------------------------\n')

# -----------------------------------------------------
# 
# -----------------------------------------------------

dev = qml.device('default.qubit', wires=3)

@qml.qnode(dev)
def too_many_ts():
    """You can implement the original circuit here as well, it may help you with
    testing to ensure that the circuits have the same effect.

    Returns:
        array[float]: The measurement outcome probabilities.
    """
    # for wire = 0
    qml.Hadamard(wires=0)
    qml.T(wires=0)
    qml.T(wires=0)
    qml.Hadamard(wires=0)
    qml.adjoint(qml.T(wires=0))
    qml.adjoint(qml.T(wires=0))
    qml.Hadamard(wires=0)

    # for wire = 1
    qml.Hadamard(wires=1)
    qml.T(wires=1)
    qml.Hadamard(wires=1)
    qml.T(wires=1)
    qml.T(wires=1)
    qml.T(wires=1)
    qml.T(wires=1)
    qml.Hadamard(wires=1)

    # for wire = 2
    qml.Hadamard(wires=2)
    qml.adjoint(qml.T(wires=2))
    qml.Hadamard(wires=2)
    qml.adjoint(qml.T(wires=2))
    qml.adjoint(qml.T(wires=2))
    qml.adjoint(qml.T(wires=2))
    qml.Hadamard(wires=2)

    return qml.probs(wires=[0, 1, 2])

@qml.qnode(dev)
def just_enough_ts():
    """Implement an equivalent circuit as the above with the minimum number of 
    T and T^\dagger gates required.

    Returns:
        array[float]: The measurement outcome probabilities.
    """

    # Wire 0
    qml.Hadamard(wires=0)
    qml.S(wires=0)
    qml.Hadamard(wires=0)
    qml.adjoint(qml.S(wires=0))
    qml.Hadamard(wires=0)

    # Wire 1
    qml.Hadamard(wires=1)
    qml.T(wires=1)
    qml.Hadamard(wires=1)
    # qml.S(wires=1)
    # qml.S(wires=1)
    # two S can be a Z
    qml.PauliZ(wires=1)
    qml.Hadamard(wires=1)

    # Wire 2
    qml.Hadamard(wires=2)
    qml.adjoint(qml.T(wires=2))
    qml.Hadamard(wires=2)
    qml.adjoint(qml.S(wires=2))
    qml.adjoint(qml.T(wires=2))
    qml.Hadamard(wires=2)

    return qml.probs(wires=[0, 1, 2])

print('-----------------------------------------------')
print("Applying too_many_ts(): ")
print(too_many_ts())
print('-----------------------------------------------')
print("Applying just_enough_ts(): ")
print(just_enough_ts())
print('-----------------------------------------------')

# FILL IN THE CORRECT VALUES FOR THE ORIGINAL CIRCUIT
original_depth = 8
original_t_count = 13
original_t_depth = 6
print('-----------------------------------------------')
print("  + original_depth: ", original_depth)
print("  + original_t_count: ", original_t_count)
print("  + original_t_depth: ", original_depth)
print('-----------------------------------------------\n')

# FILL IN THE CORRECT VALUES FOR THE NEW, OPTIMIZED CIRCUIT
optimal_depth = 6
optimal_t_count = 3
optimal_t_depth = 2
print('-----------------------------------------------')
print("  + optimal_depth: ", optimal_depth)
print("  + optimal_t_count: ", optimal_t_count)
print("  + optimal_t_depth: ", optimal_t_depth)
print('-----------------------------------------------\n')
