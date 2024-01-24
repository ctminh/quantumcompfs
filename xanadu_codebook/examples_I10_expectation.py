import pennylane as qml
import numpy as np

dev = qml.device("default.qubit", wires=1)

# -----------------------------------------------------
# Design and run a PennyLane circuit that performs
#   |0> --Rx(pi/4)--H--Z--<Y>
# where, <Y> is the measurement of PauliY
# -----------------------------------------------------

@qml.qnode(dev)
def circuit():
    qml.RX(np.pi/4, wires=0)
    qml.Hadamard(wires=0)
    qml.PauliZ(wires=0)

    return qml.expval(qml.PauliY(wires=0))

print('-----------------------------------------------')
print("Checking the circuit about: |0> --Rx(pi/4)--H--Z--<Y> ")
print(print(circuit()))
print('-----------------------------------------------\n')

# -----------------------------------------------------
# In the previous sections, we computed measurement outcome probabilities and expectation values analytically. 
# Of course, this is impossible to do on hardware. When we run a circuit and take a measurement, we get a single data point 
# that tells us in which state we observed a qubit for a particular run. Since this process is random, in order to get 
# a clearer picture of the statistics we must perform the experiment many, many times. Each time is typically called a shot, 
# or a sample. We can sample from the output distribution in order to estimate expectation values and measurement outcome 
# probabilities in situations where it isn't possible to do so analytically.
# -----------------------------------------------------

# An array to store your results
shot_results = []

# Different numbers of shots
shot_values = [100, 1000, 10000, 100000, 1000000]
for shots in shot_values: 

    # CREATE A DEVICE, CREATE A QNODE, AND RUN IT
    dev = qml.device('default.qubit', wires=1, shots=shots)
    @qml.qnode(dev)
    def circuit():
        qml.RX(np.pi/4, wires=0)
        qml.Hadamard(wires=0)
        qml.PauliZ(wires=0)
        return qml.expval(qml.PauliY(wires=0))

    # STORE RESULT IN SHOT_RESULTS ARRAY
    shot_results.append(circuit())

print('-----------------------------------------------')
print(qml.math.unwrap(shot_results))
print('-----------------------------------------------\n')

# -----------------------------------------------------
# Try to access the samples directly
# -----------------------------------------------------
dev = qml.device("default.qubit", wires=1, shots=100000)
@qml.qnode(dev)
def circuit():
    qml.RX(np.pi/4, wires=0)
    qml.Hadamard(wires=0)
    qml.PauliZ(wires=0)

    return qml.sample(qml.PauliY(wires=0))

def compute_expval_from_samples(samples):
    """Compute the expectation value of an observable given a set of 
    sample outputs. You can assume that there are two possible outcomes,
    1 and -1. 
    
    Args: 
        samples (array[float]): 100000 samples representing the results of
            running the above circuit.
        
    Returns:
        float: the expectation value computed based on samples.
    """

    estimated_expval = 0
    count_plus_1 = np.count_nonzero(samples == 1)
    count_minus_1 = np.count_nonzero(samples == -1)
    sum_plus_and_minus_1 = count_minus_1 + count_plus_1
    assert(sum_plus_and_minus_1 == len(samples))

    # USE THE SAMPLES TO ESTIMATE THE EXPECTATION VALUE
    estimated_expval = (1*count_plus_1 + (-1)*count_minus_1) / len(samples)

    return estimated_expval

print('-----------------------------------------------')
samples = circuit()
print("Array of the obtained samples: ")
print(samples)
print("Expval: ")
print(compute_expval_from_samples(samples))
print('-----------------------------------------------\n')

# -----------------------------------------------------
# The relationship between variance and shots: to explore how the accuracy of 
# the expectation value depends on the number of shots
# -----------------------------------------------------

def variance_experiment(n_shots):
    """Run an experiment to determine the variance in an expectation
    value computed with a given number of shots.
    
    Args:
        n_shots (int): The number of shots
        
    Returns:
        float: The variance in expectation value we obtain running the 
        circuit 100 times with n_shots shots each.
    """

    # To obtain a variance, we run the circuit multiple times at each shot value.
    n_trials = 100
    n_results = []

    ##################
    # YOUR CODE HERE #
    ##################

    # CREATE A DEVICE WITH GIVEN NUMBER OF SHOTS
    dev = qml.device("default.qubit", wires=1, shots=n_shots)

    # DECORATE THE CIRCUIT BELOW TO CREATE A QNODE
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        return qml.expval(qml.PauliZ(wires=0))

    # RUN THE QNODE N_TRIALS TIMES AND RETURN THE VARIANCE OF THE RESULTS
    for t in range(n_trials): 
        expval = circuit()
        n_results.append(expval)
    
    return np.var(n_results)


def variance_scaling(n_shots):
    """Once you have determined how the variance in expectation value scales
    with the number of shots, complete this function to programmatically
    represent the relationship.
    
    Args:
        n_shots (int): The number of shots
        
    Returns:
        float: The variance in expectation value we expect to see when we run
        an experiment with n_shots shots.
    """

    estimated_variance = 0

    ##################
    # YOUR CODE HERE #
    ##################

    # ESTIMATE THE VARIANCE BASED ON SHOT NUMBER
    estimated_variance = 1 / n_shots

    return estimated_variance

# Various numbers of shots; you can change this
shot_vals = [10, 20, 40, 100, 200, 400, 1000, 2000, 4000]

# Used to plot your results
print('-----------------------------------------------')
results_experiment = [variance_experiment(shots) for shots in shot_vals]
print("Array of results_experiment: ")
print(results_experiment)

results_scaling = [variance_scaling(shots) for shots in shot_vals]
print("Array of results_scaling: ")
print(results_scaling)
print('-----------------------------------------------\n')

# plot = plotter(shot_vals, results_experiment, results_scaling)