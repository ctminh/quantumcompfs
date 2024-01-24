# Refer to https://pennylane.ai/qml/demos/tutorial_qaoa_intro
# Intro to QAOA
#   + Circuits and Hamiltonians
#   + Layering circuits

import pennylane as qml
import networkx as nx
from pennylane import qaoa
from pennylane import numpy as np
from matplotlib import pyplot as plt

# hamiltonian

H = qml.Hamiltonian(
    [1, 1, 0.5],
    [qml.PauliX(0), qml.PauliZ(1), qml.PauliX(0) @ qml.PauliX(1)]
)

# implement the approximate time-evolution operator

dev = qml.device('default.qubit', wires=2)
t = 1
n = 2
@qml.qnode(dev)
def circuit():
    qml.ApproxTimeEvolution(H, t, n)
    return [qml.expval(qml.PauliZ(i)) for i in range(2)]

print('----------------------------------------------')
print(qml.draw(circuit, expansion_strategy='device')())
print('----------------------------------------------')

def circ(theta):
    qml.RX(theta, wires=0)
    qml.Hadamard(wires=1)
    qml.CNOT(wires=[0,1])

@qml.qnode(dev)
def circuit(param):
    circ(param)
    return [qml.expval(qml.PauliZ(i)) for i in range(2)]

print('----------------------------------------------')
print(qml.draw(circuit)(0.5))
print('----------------------------------------------')

# -----------------------------------------------------
# circuit layering
# -----------------------------------------------------

@qml.qnode(dev)
def circuit(params, **kwargs):
    qml.layer(circ, 3, params)
    return [qml.expval(qml.PauliZ(i)) for i in range(2)]

print('----------------------------------------------')
print(qml.draw(circuit)([0.5, 0.7, 0.9]))
print('----------------------------------------------')

# -----------------------------------------------------
# Minimum vertex cover with QAOA
# -----------------------------------------------------
'''
Our goal is to find the minimum vertex cover of a graph: a collection of vertices such that 
each edge in the graph contains at least one of the vertices in the cover. Hence, these 
vertices “cover” all the edges. We wish to find the vertex cover that has the smallest
possible number of vertices.
'''

# define the four-vertex graph
edges = [(0,1), (1,2), (2,0), (2,3)]
graph = nx.Graph(edges)
nx.draw(graph, with_labels=True)
# plt.show()

# use built-in qaoa
cost_h, mixer_h = qaoa.min_vertex_cover(graph, constrained=False)
print("Cost Hamiltonian: ", cost_h)
print("Mixer Hamiltonian: ", mixer_h)

def qaoa_layer(gamma, alpha):
    qaoa.cost_layer(gamma, cost_h)
    qaoa.mixer_layer(alpha, mixer_h)

wires = range(4)
depth = 2

def circuit(params, **kwargs):
    for w in wires:
        qml.Hadamard(wires=w)
    qml.layer(qaoa_layer, depth, params[0], params[1])

dev = qml.device('qulacs.simulator', wires=wires)

@qml.qnode(dev)
def cost_function(params):
    circuit(params)
    return qml.expval(cost_h)

optimizer = qml.GradientDescentOptimizer()
steps = 70
params = np.array([[0.5, 0.5], [0.5, 0.5]], requires_grad=True)

# optimize the circuit
for i in range(steps):
    params = optimizer.step(cost_function, params)

print("Optimal Parameters")
print(params)

# reconstruct the probability landscape
@qml.qnode(dev)
def probability_circuit(gamma, alpha):
    circuit([gamma, alpha])
    return qml.probs(wires=wires)

probs = probability_circuit(params[0], params[1])

# display a bar graph showing the probability of measuring each bitstring
# plt.style.use("seaborn")
# plt.bar(range(2 ** len(wires)), probs)
# plt.show()

