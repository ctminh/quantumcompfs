import pennylane as qml
import matplotlib.pyplot as plt

from pennylane import numpy as np

np.random.seed(42)

'''
The MaxCut problem

Given a graph with m edges and n vertices. The target is: we seek the partition z of the vertices into two sets A and B which maximizes
    C(z) = sum_{alpha=1}^{m} C_{alpha}(z)
where, C counts the number of edges cut,
    C_{alpha} = 1 if z places one vertex from the alpha-th edge in set A and the other in set B
    C_{alpha} = 0 otherwise

For MaxCut, the objective function: C_{alpha} = 1/2 * (1 - sigma_{z}^{j} * sigma_{z}^{k})

'''

# ---------------------------------------------
# Operators
# ---------------------------------------------

n_wires = 4
graph = [(0,1), (0,3), (1,2), (2,3)]

# unitary operators
def U_B(beta):
    for wire in range(n_wires):
        qml.RX(2*beta, wires=wire)

def U_C(gamma):
    for edge in graph:
        wire0 = edge[0]
        wire1 = edge[1]
        qml.CNOT(wires=[wire0, wire1])
        qml.RZ(gamma, wires=wire1)
        qml.CNOT(wires=[wire0, wire1])

# define bit strings
def bitstring_to_int(bit_string_sample):
    bit_string = "".join(str(bs) for bs in bit_string_sample)
    return int(bit_string, base=2)

# ---------------------------------------------
# Circuit
# ---------------------------------------------
dev = qml.device("lightning.qubit", wires=n_wires, shots=1)

@qml.qnode(dev)
def circuit(gammas, betas, edge=None, n_layers=1):
    
    # use Hadamard gate to create |+> state
    for wire in range(n_wires):
        qml.Hadamard(wires=wire)

    # create p layers of unitary operators
    for i in range(n_layers):
        U_C(gammas[i])
        U_B(betas[i])

    if edge is None:
        return qml.sample() # the |+> sates as init
    
    # using PauliZ to evaluate term in the objective function using expval
    H = qml.PauliZ(edge[0]) @ qml.PauliZ(edge[1])
    expval = qml.expval(H)

    # print("Circuit expectation values: {}".format(expval))

    return expval

# ---------------------------------------------
# Optimization
# ---------------------------------------------

def qaoa_maxcut(n_layers=1):
    print("\n Num. of layers: p = {}\n".format(n_layers))

    # initialize the parameters near zero
    init_params = 0.01 * np.random.rand(2, n_layers, requires_grad=True)
    print('Init params: {}\n'.format(init_params))

    # minimize the negative of the objective function
    def objective(params):
        gammas = params[0]
        betas = params[1]
        neg_obj = 0
        for edge in graph:
            neg_obj -= 0.5 * (1 - circuit(gammas, betas, edge=edge, n_layers=n_layers))
            drawer = qml.draw(circuit)
            print(drawer(gammas,betas))
        return neg_obj

    # initialize optimizer: Adagrad works well empirically
    opt = qml.AdagradOptimizer(stepsize=0.5)

    # optimize parameters in objective
    params = init_params
    steps = 30
    for i in range(steps):
        params = opt.step(objective, params)
        print("Objective step {:3d}: params = {}, objective_cost = {:.5f}".format(i + 1, params, -objective(params)))
        exit()
        # if (i + 1) % 5 == 0:
        #     print("Objective after step {:5d}: {: .7f}".format(i + 1, -objective(params)))

    print("-----------------------------------------------\n")
    # sample measured bitstrings 100 times
    bit_strings = []
    n_samples = 100
    for i in range(0, n_samples):
        bitstring_to_num = bitstring_to_int(circuit(params[0], params[1], edge=None, n_layers=n_layers))
        bit_strings.append(bitstring_to_num)
        print("   + Sample {:3d}: param0={}, param1={}, bitstring_to_int = {}".format(i, params[0], params[1], bitstring_to_num))
    print("-----------------------------------------------\n")

    # print optimal parameters and most frequently sampled bitstring
    counts = np.bincount(np.array(bit_strings))
    most_freq_bit_string = np.argmax(counts)
    print("Optimized (gamma, beta) vectors:\n{}".format(params[:, :n_layers]))
    print("Most frequently sampled bit string is: {:04b}".format(most_freq_bit_string))

    return -objective(params), bit_strings

# perform qaoa on our graph with p=1,2 and
# keep the bitstring sample lists
# bitstrings1 = qaoa_maxcut(n_layers=1)[1]
# bitstrings2 = qaoa_maxcut(n_layers=2)[1]

# xticks = range(0, 16)
# xtick_labels = list(map(lambda x: format(x, "04b"), xticks))
# bins = np.arange(0, 17) - 0.5

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
# plt.subplot(1, 2, 1)
# plt.title("n_layers=1")
# plt.xlabel("bitstrings")
# plt.ylabel("freq.")
# plt.xticks(xticks, xtick_labels, rotation="vertical")
# plt.hist(bitstrings1, bins=bins)
# plt.subplot(1, 2, 2)
# plt.title("n_layers=2")
# plt.xlabel("bitstrings")
# plt.ylabel("freq.")
# plt.xticks(xticks, xtick_labels, rotation="vertical")
# plt.hist(bitstrings2, bins=bins)
# plt.tight_layout()
# plt.show()