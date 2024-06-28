import pennylane as qml
import numpy as np

# -----------------------------------------------------
# Bell states include 4 states that form the Bell basis
# -----------------------------------------------------

dev = qml.device('default.qubit', wires=2)

# Starting from the state |00>, implement a PennyLane circuit
# to construct each of the Bell basis states.

@qml.qnode(dev)
def prepare_psi_plus():

    # PREPARE (1/sqrt(2)) (|00> + |11>)
    # we use Hadamard and CNOT
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0,1])
    return qml.state()

@qml.qnode(dev)
def prepare_psi_minus():

    # PREPARE (1/sqrt(2)) (|00> - |11>)
    # we use PauliX to prepare |1>, then 
    # use Hadamard and CNOT for the state
    qml.PauliX(wires=0)
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0,1])
    return qml.state()

@qml.qnode(dev)
def prepare_phi_plus():

    # PREPARE  (1/sqrt(2)) (|01> + |10>)
    # change the control and target wires with CNOT
    qml.PauliX(wires=0)
    qml.Hadamard(wires=1)
    qml.CNOT(wires=[1,0])
    return qml.state()

@qml.qnode(dev)
def prepare_phi_minus():

    # PREPARE  (1/sqrt(2)) (|01> - |10>)
    qml.PauliX(wires=1)
    qml.Hadamard(wires=1)
    qml.PauliX(wires=0)
    qml.PauliX(wires=1)
    qml.CNOT(wires=[1,0])
    return qml.state()

psi_plus = prepare_psi_plus()
psi_minus = prepare_psi_minus()
phi_plus = prepare_phi_plus()
phi_minus = prepare_phi_minus()

print('-----------------------------------------------')
print('The Bell states:')
print(f"|ψ_+> = {psi_plus}")
print(f"|ψ_-> = {psi_minus}")
print(f"|ϕ_+> = {phi_plus}")
print(f"|ϕ_-> = {phi_minus}")
print('-----------------------------------------------\n')


# -----------------------------------------------------
# A quantum multiplexer and uniformly controlled rotation
# -----------------------------------------------------

dev = qml.device("default.qubit", wires=3)

# State of first 2 qubits
state = [0, 1]

@qml.qnode(device=dev)
def apply_control_sequence(state):
    # Set up initial state of the first two qubits
    if state[0] == 1:
        qml.PauliX(wires=0)
    if state[1] == 1:
        qml.PauliX(wires=1) 

    # Set up initial state of the third qubit - use |->
    # so we can see the effect on the output
    qml.PauliX(wires=2)
    qml.Hadamard(wires=2)
    
    # IMPLEMENT THE MULTIPLEXER

    # IF STATE OF FIRST TWO QUBITS IS 01, APPLY X TO THIRD QUBIT
    qml.MultiControlledX(control_wires=[0,1], wires=2, control_values="01")
    
    # IF STATE OF FIRST TWO QUBITS IS 10, APPLY Z TO THIRD QUBIT
    Z = np.matrix([[1,0], [0,-1]])
    qml.ControlledQubitUnitary(Z, control_wires=[0,1], wires=2, control_values="10")

    # IF STATE OF FIRST TWO QUBITS IS 11, APPLY Y TO THIRD QUBIT
    Y = np.matrix([[0,-1j],[1j,0]])
    qml.ControlledQubitUnitary(Y, control_wires=[0,1], wires=2, control_values="11")
    
    return qml.state()
    
print('-----------------------------------------------')
print('The quantum multiplexer and uniformly controlled rotation:')
print(apply_control_sequence(state))
print('-----------------------------------------------\n')