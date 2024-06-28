import pennylane as qml

def my_quantum_function(params):

    # single qubit operations with no input parameters
    qml.Gate1(wires=0)
    qml.Gate2(wires=1)

    # a single qubit operation with an input parameter
    qml.Gate3(params[0], wires=0)

    # two qubit operation with no input parameter on wires 0 and 1
    qml.TwoQubitGate1(wires=[0, 1])

    # two qubit operation with an input parameter on wires 0 and 1
    qml.TwoQubitGate2(params[1], wires=[0, 1])

    # return the result of a measurement
    return qml.Measurement(wires=[0, 1])

def my_circuit1(theta, phi):

    qml.CNOT(wires=[0, 1])
    qml.RX(theta, wires=2)
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[2, 0])
    qml.RY(phi, wires=1)

    return qml.probs(wires=[0, 1, 2])

meas_outcome = my_circuit1(0.8, 0.6)
print('-----------------------------------------------')
print("Measurement outcome - my_circuit1: ")
print(meas_outcome)
print('-----------------------------------------------\n')

# need a device to run the quantum simulator
# dev = qml.device('device.name', wires=num_qubits)
# dev = qml.device('default.qubit', wires=["wire_a", "wire_b"])
dev = qml.device("default.qubit", wires=3)

# construct a Qnode to perform computation
# my_qnode = qml.QNode(my_circuit, dev)

@qml.qnode(dev)
def my_circuit2(theta, phi, omega):

    # Here are two examples, so you can see the format:
    qml.RX(theta, wires=0)
    qml.RY(phi, wires=1)
    qml.RZ(omega, wires=2)
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[1, 2])
    qml.CNOT(wires=[2, 0])

    return qml.probs(wires=[0, 1, 2])

# This creates a QNode, binding the function and device
# my_qnode = qml.QNode(my_circuit2, dev)

# We set up some values for the input parameters
theta, phi, omega = 0.1, 0.2, 0.3

# Now we can execute the QNode by calling it like we would a regular function
resource_calculator = qml.specs(my_circuit2)
outcome = my_circuit2(theta, phi, omega)
print('-----------------------------------------------')
print("Measurement outcome running on QNode for my_circuit2: ")
print(outcome)
print('-----------------------------------------------\n')