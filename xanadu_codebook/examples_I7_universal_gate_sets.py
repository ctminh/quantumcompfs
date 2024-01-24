import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)

# -----------------------------------------------------
# Adjusting the angels to transform RZ-RX-RZ to H
# -----------------------------------------------------

# Adjust the values of phi, theta, omega
phi, theta, omega = np.pi/2, np.pi/2, np.pi/2

@qml.qnode(dev)
def hadamard_with_rz_rx():
    qml.RZ(phi, wires=0)
    qml.RX(theta, wires=0)
    qml.RZ(omega, wires=0)
    return qml.state()

@qml.qnode(dev)
def apply_hadamard():
    qml.Hadamard(0)
    return qml.state()

print('-----------------------------------------------')
print("Checking hadamard_with_rz_rx(): ")
print(hadamard_with_rz_rx())
print(apply_hadamard())
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Converting H-S-conj(T)-Y by using only RZ, RX
# -----------------------------------------------------
phi, theta, omega = np.pi/2, np.pi/2, np.pi/2

@qml.qnode(dev)
def origin_circuit():
    qml.Hadamard(0)
    qml.S(0)
    qml.adjoint(qml.T(wires=0))
    qml.PauliY(0)
    
    return qml.state()

@qml.qnode(dev)
def convert_to_rz_rx():
    
    qml.RZ(phi, wires=0)
    qml.RX(theta, wires=0)
    qml.RZ(omega, wires=0)
    
    qml.RZ(np.pi/2, wires=0)
    qml.RZ(-np.pi/4, wires = 0)
    
    qml.RZ(np.pi,wires=0)
    qml.RX(np.pi, wires=0)

    return qml.state()

print('-----------------------------------------------')
print("Converting H-S-conj(T)-Y by convert_to_rz_rx():")
print(convert_to_rz_rx())
print("Checking with the original circuit:")
print(origin_circuit())
print('-----------------------------------------------\n')