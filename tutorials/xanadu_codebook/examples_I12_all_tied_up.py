import pennylane as qml
import numpy as np

# -----------------------------------------------------
# Apply CNOT
# -----------------------------------------------------

dev = qml.device('default.qubit', wires=2)
@qml.qnode(dev)
def apply_cnot(basis_id):
    """Apply a CNOT to |basis_id>.

    Args:
        basis_id (int): An integer value identifying the basis state to construct.
      
    Returns:
        array[complex]: The resulting state after applying CNOT|basis_id>.
    """

    # Prepare the basis state |basis_id>
    bits = [int(x) for x in np.binary_repr(basis_id, width=dev.num_wires)]
    print(bits)

    qml.BasisStatePreparation(bits, wires=[0, 1])

    # APPLY THE CNOT
    qml.CNOT(wires=[0, 1])
    
    return qml.state()

# REPLACE THE BIT STRINGS VALUES BELOW WITH THE CORRECT ONES
cnot_truth_table = {
    "00" : "00",
    "01" : "01",
    "10" : "11",
    "11" : "10"
}

# Run your QNode with various inputs to help fill in your truth table
print('-----------------------------------------------')
print('Checking apply_cnot(0):')
print(apply_cnot(0))
print('-----------------------------------------------\n')


# -----------------------------------------------------
# Apply H CNOT
# -----------------------------------------------------
dev = qml.device("default.qubit", wires=2)
@qml.qnode(dev)
def apply_h_cnot():

    # APPLY THE OPERATIONS IN THE CIRCUIT
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])

    return qml.state()


# SET THIS AS 'separable' OR 'entangled' BASED ON YOUR OUTCOME
state_status = "entangled"
print('-----------------------------------------------')
print('Checking apply_h_cnot(0):')
print(apply_h_cnot())
print('-----------------------------------------------\n')


# -----------------------------------------------------
# Apply controll rotations
#   + |0> ---H----*----------Rz(w)----
#   + |0> ------Rx(t)---*-------------
#   + |0> ------------Ry(w)---*-------
# -----------------------------------------------------

dev = qml.device('default.qubit', wires=3)
@qml.qnode(dev)
def controlled_rotations(theta, phi, omega):
    """Implement the circuit above and return measurement outcome probabilities.

    Args:
        theta (float): A rotation angle
        phi (float): A rotation angle
        omega (float): A rotation angle

    Returns:
        array[float]: Measurement outcome probabilities of the 3-qubit 
        computational basis states.
    """

    # APPLY THE OPERATIONS IN THE CIRCUIT AND RETURN MEASUREMENT PROBABILITIES

    qml.Hadamard(wires=0)
    qml.CRX(theta, wires=[0, 1])
    qml.CRY(phi, wires=[1, 2])
    qml.CRZ(phi, wires=[2, 0])

    return qml.probs(wires=[0,1,2])

print('-----------------------------------------------')
print('Checking controlled_rotations(theta, phi, omega):')
theta, phi, omega = 0.1, 0.2, 0.3
print(controlled_rotations(theta, phi, omega))
print('-----------------------------------------------\n')
