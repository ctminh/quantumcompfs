import numpy as np
import cmath

# Here are the vector representations of |0> and |1>, for convenience

def normalize_state(alpha, beta):
    """Compute a normalized quantum state given arbitrary amplitudes.
    
    Args:
        alpha (complex): The amplitude associated with the |0> state.
        beta (complex): The amplitude associated with the |1> state.
        
    Returns:
        array[complex]: A vector (numpy array) with 2 elements that represents
        a normalized quantum state.
    """

    N_conj = alpha*alpha.conjugate() + beta*beta.conjugate()
    N = np.sqrt(N_conj)

    norm_alpha = alpha / N
    norm_beta = beta / N

    # create the vector which is normalized
    vec_result = np.array([norm_alpha, norm_beta])
    
    # return the normalized vector
    return vec_result


def inner_product(state_1, state_2):
    """Compute the inner product between two states.
    
    Args:
        state_1 (array[complex]): A normalized quantum state vector
        state_2 (array[complex]): A second normalized quantum state vector
        
    Returns:
        complex: The value of the inner product <state_1 | state_2>.
    """
 
    bra_state2 = state_2.conjugate()
    bra_state1 = state_1.conjugate()

    # compute the inner product
    inn_prod = bra_state1 @ state_2
    
    return inn_prod


def measure_state(state, num_meas):
    """Simulate a quantum measurement process.

    Args:
        state (array[complex]): A normalized qubit state vector. 
        num_meas (int): The number of measurements to take
        
    Returns:
        array[int]: A set of num_meas samples, 0 or 1, chosen according to the probability 
        distribution defined by the input state.
    """

    # normalize the states
    norm_state = normalize_state(state[0], state[1])
    # print(norm_state)

    # calculate the probabilities
    prob_distribution = norm_state * norm_state
    # print(prob_distribution)
    
    # compute the measurement probabilities
    measurement_outcomes = []
    for i in range(num_meas):
        random_number = np.random.random()  # generate a random number between 0 and 1
        outcome = 0 if random_number < prob_distribution[0] else 1
        measurement_outcomes.append(outcome)

    # return a list of measurement
    # print(measurement_outcomes)
 
    return measurement_outcomes

U = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
# U = np.array([[0, 1], [1, 0]])
def apply_u(state):
    """Apply a quantum operation.

    Args:
        state (array[complex]): A normalized quantum state vector. 
        
    Returns:
        array[complex]: The output state after applying U.
    """

    outcome_state = U @ state
    
    return outcome_state

def initialize_state():
    """Prepare a qubit in state |0>.
    
    Returns:
        array[float]: the vector representation of state |0>.
    """

    qubit_state0 = np.array([1, 0], dtype=complex)
    
    return qubit_state0

def quantum_algorithm():
    """Use the functions above to implement the quantum algorithm described above.
    
    Try and do so using three lines of code or less!
    
    Returns:
        array[int]: the measurement results after running the algorithm 100 times
    """

    # initialize a qubit in state 0
    qubit_state = initialize_state()
    print("- Init a qubit at state |0>: ", qubit_state)

    # apply U gate
    appU_state = apply_u(qubit_state)
    print("- Apply U gate to the sate: ", appU_state)

    # simulate measuring the qubit 100 times
    meas_outcome = measure_state(appU_state, 100)
    print("- Outcome after 100x measurements: ", meas_outcome)

    return meas_outcome

alpha = complex(2.0, 1.0)
beta = complex(-0.3, 0.4)
qstate = normalize_state(alpha, beta)

print('------------------------------------------------------------------')
print('Ex1. Normalizing a qubit state: ')
print(qstate)
print('------------------------------------------------------------------\n')

print('------------------------------------------------------------------')
print('Ex2. Inner product: ')
ket_0 = np.array([1, 0])
ket_1 = np.array([0, 1])
print(f"<0|0> = {inner_product(ket_0, ket_0)}")
print(f"<0|1> = {inner_product(ket_0, ket_1)}")
print(f"<1|0> = {inner_product(ket_1, ket_0)}")
print(f"<1|1> = {inner_product(ket_1, ket_1)}")
print('------------------------------------------------------------------\n')

print('------------------------------------------------------------------')
print('Ex3. Measuring qubit states: ')
state = np.array([0.8, 0.6])
rand_outcomes = measure_state(state, 10)
print(rand_outcomes)
print('------------------------------------------------------------------\n')

print('------------------------------------------------------------------')
print('Ex4. Applying U gate: ')
state = np.array([0.8, 0.6])
applyu_outcomes = apply_u(state)
print(applyu_outcomes)
print('------------------------------------------------------------------\n')

print('------------------------------------------------------------------')
print('Ex5. Simulating a simple qubit: ')
quantum_algorithm()
print('------------------------------------------------------------------\n')