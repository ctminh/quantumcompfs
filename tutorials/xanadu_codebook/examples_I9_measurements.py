import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)

# -----------------------------------------------------
# Measurement with Hadamard gate
# -----------------------------------------------------

@qml.qnode(dev)
def apply_h_and_measure(state):
    """Complete the function such that we apply the Hadamard gate
    and measure in the computational basis.
    
    Args:
        state (int): Either 0 or 1. If 1, prepare the qubit in state |1>,
            otherwise leave it in state 0.
    
    Returns:
        array[float]: The measurement outcome probabilities.
    """
    if state == 1:
        qml.PauliX(wires=0)

    qml.Hadamard(wires=0)

    return qml.probs(wires=0)

print('-----------------------------------------------')
print("Checking the measurement of |0>: ")
print(apply_h_and_measure(0))
print("Checking the measurement of |1>: ")
print(apply_h_and_measure(1))
print('-----------------------------------------------\n')


# prepare a state (1/2)|0> + i(sqrt(3)/2)|1>
# psi = np.array([0.5+0j, 0 + np.sqrt(3)/2j])
def prepare_psi():
    # qml.MottonenStatePreparation(psi,wires=0)
    qml.RX(np.pi/3, wires=0)
    qml.PauliX(wires=0)

# write a quantum function that sends both|0> TO |y_+> and |1> TO |y_->
def y_basis_rotation():
    qml.Hadamard(wires=0)
    qml.S(wires=0)

dev = qml.device("default.qubit", wires=1)
@qml.qnode(dev)
def measure_in_y_basis():
    
    # PREPARE THE STATE
    prepare_psi()

    # PERFORM THE ROTATION BACK TO COMPUTATIONAL BASIS
    qml.adjoint(y_basis_rotation)

    # RETURN THE MEASUREMENT OUTCOME PROBABILITIES
    return qml.probs(wires=0)

print('-----------------------------------------------')
print("Checking measure_in_y_basis: ")
print(measure_in_y_basis())
print('-----------------------------------------------\n')