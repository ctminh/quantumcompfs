import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)

# -----------------------------------------------------
# Applying RX gate
# -----------------------------------------------------

@qml.qnode(dev)
def apply_rx_pi(state):
    """Apply an RX gate with an angle of \pi to a particular basis state.
    
    Args:
        state (int): Either 0 or 1. If 1, initialize the qubit to state |1>
            before applying other operations.
    
    Returns:
        array[complex]: The state of the qubit after the operations.
    """
    if state == 1:
        qml.PauliX(wires=0)

    qml.RX(np.pi, wires=0)

    return qml.state()

print('-----------------------------------------------')
print("Applying apply_rx_pi(0): ")
print(apply_rx_pi(0))
print('-----------------------------------------------')
print("Applying apply_rx_pi(1): ")
print(apply_rx_pi(1))
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Applying RX to modify the amplitudes of a quantum state
# -----------------------------------------------------

@qml.qnode(dev)
def apply_rx2mod_amplitute(theta, state):
    """Apply an RX gate with an angle of theta to a particular basis state.
    
    Args:
        theta (float): A rotation angle.
        state (int): Either 0 or 1. If 1, initialize the qubit to state |1>
            before applying other operations.
    
    Returns:
        array[complex]: The state of the qubit after the operations.
    """
    if state == 1:
        qml.PauliX(wires=0)

    qml.RX(theta, wires=0)

    return qml.state()

print('-----------------------------------------------')
print("Applying apply_rx2mod_amplitute(): ")

angles = np.linspace(0, 4*np.pi, 200)
print("  + angles:")
print(angles)

output_states = np.array([apply_rx2mod_amplitute(t, 0) for t in angles])
print("  + the output states:")
print(output_states)
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Applying RY to modify the amplitudes of a quantum state
# -----------------------------------------------------

@qml.qnode(dev)
def apply_ry2mod_amplitute(theta, state):
    """Apply an RY gate with an angle of theta to a particular basis state.
    
    Args:
        theta (float): A rotation angle.
        state (int): Either 0 or 1. If 1, initialize the qubit to state |1>
            before applying other operations.
    
    Returns:
        array[complex]: The state of the qubit after the operations.
    """
    if state == 1:
        qml.PauliX(wires=0)

    qml.RY(theta, wires=0)

    return qml.state()

print('-----------------------------------------------')
print("Applying apply_ry2mod_amplitute(): ")
angles = np.linspace(0, 4*np.pi, 200)
print("  + angles:")
print(angles)

output_states = np.array([apply_ry2mod_amplitute(t, 0) for t in angles])
print("  + the output states:")
print(output_states)
print('-----------------------------------------------\n')

