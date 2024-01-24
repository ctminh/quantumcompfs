import pennylane as qml
import numpy as np

# -----------------------------------------------------
# Multi-qubit system
# -----------------------------------------------------

dev = qml.device('default.qubit', wires=3)
@qml.qnode(dev)
def make_basis_state(basis_id):
    """Produce the 3-qubit basis state corresponding to |basis_id>.
    
    Note that the system starts in |000>.

    Args:
        basis_id (int): An integer value identifying the basis state to construct.
        
    Returns:
        array[complex]: The computational basis state |basis_id>.
    """

    # convert to binary
    basis_id_binary = np.base_repr(basis_id).zfill(3)
    print(basis_id_binary)
    
    # convert binary string to list
    list_basis_id = list(basis_id_binary)
    print(list_basis_id)
    
    # convert list to integer values
    final_list = [int(x) for x in list_basis_id]
    print(final_list)

    # prepare the correct computational basis state
    for i in range(len(final_list)):
        if final_list[i] == 1:
            qml.PauliX(wires=i)
    
    return qml.state()

basis_id = 3

print('-----------------------------------------------')
print('Make basis state:')
print(f"Output state = {make_basis_state(basis_id)}")
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Create a state: |+1> = |+> dotproduct |1>, and return
# the measurments with Y and Z
# -----------------------------------------------------
dev = qml.device('default.qubit', wires=2)
@qml.qnode(dev)
def two_qubit_circuit():

    # PREPARE |+>|1>
    qml.Hadamard(wires=0)
    qml.PauliX(wires=1)

    # RETURN TWO EXPECTATION VALUES, Y ON FIRST QUBIT, Z ON SECOND QUBIT
    return (qml.expval(qml.PauliY(0)), qml.expval(qml.PauliZ(1)))

print('-----------------------------------------------')
print('two_qubit_circuit:')
print(two_qubit_circuit())
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Create a state: |1-> = |1> dotproduct |->, and return
# the measurments with Y and Z
# -----------------------------------------------------
dev = qml.device("default.qubit", wires=2)
@qml.qnode(dev)
def create_one_minus():

    # Prepare |1>|->
    qml.PauliX(wires=0)
    qml.PauliX(wires=1)
    qml.Hadamard(wires=1)

    # Return expected value of Z \otimes X
    return qml.expval(qml.PauliZ(0) @ qml.PauliX(1))

print('-----------------------------------------------')
print('create_one_minus:')
print(create_one_minus())
print('-----------------------------------------------\n')


# -----------------------------------------------------
# two versions of a circuit
#   + ver1: |0> --Rx(phi)---<Z>
#           |0> --Rx(2phi)--<Z>
#   + ver2: Z tensorproduct Z
# -----------------------------------------------------
dev = qml.device('default.qubit', wires=2)
@qml.qnode(dev)
def circuit_1(theta):
    """Implement the circuit and measure Z I and I Z.
    
    Args:
        theta (float): a rotation angle.
        
    Returns:
        float, float: The expectation values of the observables Z I, and I Z
    """
    qml.RX(theta, wires=0)
    qml.RY(2*theta, wires=1)

    return (qml.expval(qml.PauliZ(0)), qml.expval(qml.PauliZ(1)))


@qml.qnode(dev)
def circuit_2(theta):
    """Implement the circuit and measure Z Z.
    
    Args:
        theta (float): a rotation angle.
        
    Returns:
        float: The expectation value of the observable Z Z
    """ 

    qml.RX(theta, wires=0)
    qml.RY(2*theta, wires=1)  
 
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))


def zi_iz_combination(ZI_results, IZ_results):
    """Implement a function that acts on the ZI and IZ results to
    produce the ZZ results. How do you think they should combine?

    Args:
        ZI_results (array[float]): Results from the expectation value of 
            ZI in circuit_1.
        IZ_results (array[float]): Results from the expectation value of 
            IZ in circuit_2.

    Returns:
        array[float]: A combination of ZI_results and IZ_results that 
        produces results equivalent to measuring ZZ.
    """

    combined_results = np.zeros(len(ZI_results))
    
    return ZI_results * IZ_results

theta = np.linspace(0, 2 * np.pi, 100)

# Run circuit 1, and process the results
circuit_1_results = np.array([circuit_1(t) for t in theta])
ZI_results = circuit_1_results[:, 0]
IZ_results = circuit_1_results[:, 1]

print('-----------------------------------------------')
print('circuit_1_results:')
print(ZI_results)
print(IZ_results)

combined_results = zi_iz_combination(ZI_results, IZ_results)
print('combined_circuit_1_results:')
print(combined_results)
print('-----------------------------------------------')

# Run circuit 2
ZZ_results = np.array([circuit_2(t) for t in theta])
print('ZZ_results:')
print(ZZ_results)
print('-----------------------------------------------\n')

# Plot your results
# plot = plotter(theta, ZI_results, IZ_results, ZZ_results, combined_results)