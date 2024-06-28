import pennylane as qml
import numpy as np

# -----------------------------------------------------
# Check CZ by different ways to implement
# -----------------------------------------------------

dev = qml.device("default.qubit", wires=2)

# Prepare a two-qubit state; change up the angles if you like
phi, theta, omega = 1.2, 2.3, 3.4

@qml.qnode(device=dev)
def prepare_states(phi, theta, omega):
    
    # Apply rotation gate on the first qubit
    qml.RY(theta, wires=0)
    qml.RZ(phi, wires=0)
    
    # Apply rotation gate on the second qubit
    qml.RZ(omega, wires=1)

    return qml.state()

@qml.qnode(device=dev)
def true_cz(phi, theta, omega):
    prepare_states(phi, theta, omega)

    # IMPLEMENT THE REGULAR CZ GATE HERE
    qml.CZ(wires = [0,1])
    
    return qml.state()


@qml.qnode(dev)
def imposter_cz(phi, theta, omega):
    prepare_states(phi, theta, omega)

    # IMPLEMENT CZ USING ONLY H AND CNOT
    qml.Hadamard(wires = 1)
    qml.CNOT(wires = [0,1])
    qml.Hadamard(wires = 1)
    
    return qml.state()

print('-----------------------------------------------')
print(f"True CZ output state {true_cz(phi, theta, omega)}")
print(f"Imposter CZ output state {imposter_cz(phi, theta, omega)}")
print('-----------------------------------------------\n')


# -----------------------------------------------------
# Check SWAP by different ways to implement
# -----------------------------------------------------

dev = qml.device("default.qubit", wires=2)

# Prepare a two-qubit state; change up the angles if you like
phi, theta, omega = 0.2, 2.0, 1.5

@qml.qnode(dev)
def apply_swap(phi, theta, omega):
    prepare_states(phi, theta, omega)

    # IMPLEMENT THE REGULAR SWAP GATE HERE
    qml.SWAP(wires=[0,1])

    return qml.state()

@qml.qnode(dev)
def apply_swap_with_cnots(phi, theta, omega):
    prepare_states(phi, theta, omega)

    # IMPLEMENT THE SWAP GATE USING A SEQUENCE OF CNOTS
    qml.CNOT(wires=[0,1])
    qml.CNOT(wires=[1,0])
    qml.CNOT(wires=[0,1])

    return qml.state()

print('-----------------------------------------------')
print(f"Regular SWAP state = {apply_swap(phi, theta, omega)}")
print(f"CNOT SWAP state = {apply_swap_with_cnots(phi, theta, omega)}")
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Check Toffoli gate
# -----------------------------------------------------

dev = qml.device("default.qubit", wires=3)

# Prepare first qubit in |1>, and arbitrary states on the second two qubits
phi, theta, omega = 1.2, 2.3, 3.4

@qml.qnode(dev)
def prepare_arbitrary_states(phi, theta, omega):
    # Prepare the first qubit in the |1⟩ state
    qml.PauliX(wires=0)
    
    # Apply rotation gates to the second qubit
    qml.RY(theta, wires=1)
    qml.RZ(phi, wires=1)
    
    # Apply rotation gate to the third qubit
    qml.RZ(omega, wires=2)
    
    return qml.state()
    # return qml.probs(wires=[0, 1, 2])

# A helper function just so you can visualize the initial state
# before the controlled SWAP occurs.
@qml.qnode(dev)
def no_swap(phi, theta, omega):
    prepare_arbitrary_states(phi, theta, omega)
    return qml.state()

@qml.qnode(dev)
def controlled_swap(phi, theta, omega):
    prepare_arbitrary_states(phi, theta, omega)

    # PERFORM A CONTROLLED SWAP USING A SEQUENCE OF TOFFOLIS
    qml.Toffoli(wires=[0, 1, 2])
    qml.Toffoli(wires=[0, 2, 1])
    qml.Toffoli(wires=[0, 1, 2])

    return qml.state()

print('-----------------------------------------------')
print(f"No SWAP state = {no_swap(phi, theta, omega)}")
print(f"Controlled SWAP state = {controlled_swap(phi, theta, omega)}")
print('-----------------------------------------------\n')


# -----------------------------------------------------
# MulticontrolledX gate
# -----------------------------------------------------

dev = qml.device('default.qubit', wires=4)

@qml.qnode(dev)
def four_qubit_mcx():

    # IMPLEMENT THE CIRCUIT ABOVE USING A 4-QUBIT MULTI-CONTROLLED X
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    qml.Hadamard(wires=2)

    qml.MultiControlledX(control_wires=[0,1,2], wires=3, control_values="001")

    return qml.state()

print('-----------------------------------------------')
print("MultiControlledX state:")
print(four_qubit_mcx())
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Using only Toffoli gates to implement the 3-controlled-NOT
# -----------------------------------------------------

# Wires 0, 1, 2 are the control qubits
# Wire 3 is the auxiliary qubit
# Wire 4 is the target 

dev = qml.device('default.qubit', wires=5)
@qml.qnode(dev)
def four_qubit_mcx_only_tofs():
    # We will initialize the control qubits in state |1> so you can see
    # how the output state gets changed.
    qml.PauliX(wires=0)
    qml.PauliX(wires=1)
    qml.PauliX(wires=2)

    # IMPLEMENT A 3-CONTROLLED NOT WITH TOFFOLIS

    # Map the ancillary to |ab 0>
    qml.Toffoli(wires = [0,1,3])
    
    # Map the target to |c 0 (abc)>
    qml.Toffoli(wires = [2,3,4])
    
    # Reset the ancillary to |0>
    qml.Toffoli(wires = [0,1,3])

    return qml.state()

print('-----------------------------------------------')
print("Four qubits MCX only using Toffolis:")
print(four_qubit_mcx_only_tofs())
print('-----------------------------------------------\n')