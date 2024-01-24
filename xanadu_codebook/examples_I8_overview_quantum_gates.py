import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)

# -----------------------------------------------------
# Prepare a state: 1/sqrt(2) |0> + 1/sqrt(2) e^{5/2 i pi} |1>
# -----------------------------------------------------

@qml.qnode(dev)
def prepare_state_1():

    qml.Hadamard(wires=0)
    qml.T(wires=0)
    qml.T(wires=0)
    qml.T(wires=0)
    qml.T(wires=0)
    qml.T(wires=0)

    return qml.state()

print('-----------------------------------------------')
print("Checking prepare_state_1(): ")
print(prepare_state_1())
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Prepare a state: sqrt(3)/2 |0> - i/2 |1>
# -----------------------------------------------------

@qml.qnode(dev)
def prepare_state_2():

    qml.RX(np.pi/3, wires=0)

    return qml.state()

print('-----------------------------------------------')
print("Checking prepare_state_2(): ")
print(prepare_state_2())
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Prepare a state: 
# (0.52889389 - 0.14956775i) |0> + (0.6726317 + 0.49545818i) |1>
# using qml.MottonenStatePreparation
# -----------------------------------------------------
v = np.array([0.52889389-0.14956775j, 0.67262317+0.49545818j])
@qml.qnode(dev)
def prepare_state_3(state=v):
    
    qml.MottonenStatePreparation(v,wires=0)
    return qml.state()

# This will draw the quantum circuit and allow you to inspect the output gates
print('-----------------------------------------------')
print("Checking prepare_state_3(): ")
print(prepare_state_3(v))
print()
print(qml.draw(prepare_state_3, expansion_strategy='device')(v))
print('-----------------------------------------------\n')