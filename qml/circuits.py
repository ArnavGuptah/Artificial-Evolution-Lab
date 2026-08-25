import pennylane as qml
import numpy as np

N_QUBITS = 8
N_LAYERS = 2

dev = qml.device(

    "default.qubit",
    wires=N_QUBITS

)

def initialize_weights():

    return np.random.uniform(

        0,
        2 * np.pi,
        (N_LAYERS, N_QUBITS)

    )

weight_shapes = {"weights": (N_LAYERS, N_QUBITS)}

@qml.qnode(dev)

def embedding_circuit(inputs, weights):

    for i in range(N_QUBITS):

        qml.RY(
            inputs[i],
            wires=i
        )

    for i in range(N_QUBITS - 1):

        qml.CNOT(wires=[i, i + 1])

    for layer in range(N_LAYERS):

        for qubit in range(N_QUBITS):

            qml.RY(
                weights[layer][qubit],
                wires=qubit
            )

        for qubit in range(N_QUBITS - 1):

            qml.CNOT(wires=[qubit, qubit + 1])

    return qml.state()

@qml.qnode(dev, interface="torch", diff_method="backprop")

def variational_circuit(inputs, weights):

    for i in range(N_QUBITS):

        qml.RY(inputs[i], wires=i)

    for i in range(N_QUBITS - 1):
    
        qml.CNOT(wires=[i, i+1])

    for layer in range(N_LAYERS):

        for qubit in range(N_QUBITS):

            qml.RY(

                weights[layer][qubit],

                wires=qubit

            )

        for qubit in range(N_QUBITS - 1):

            qml.CNOT(

                wires=[qubit, qubit + 1]

            )

    return [

        qml.expval(qml.PauliZ(i))

        for i in range(N_QUBITS)

    ]

@qml.qnode(dev, interface="torch", diff_method="backprop")

def vqc_circuit(inputs, weights):

    # Encode classical features
    for i in range(N_QUBITS):

        qml.RY(
            inputs[i],
            wires=i
        )

    # Variational layers
    for layer in range(N_LAYERS):

        for i in range(N_QUBITS):

            qml.RY(
                weights[layer][i],
                wires=i
            )

        for i in range(N_QUBITS - 1):

            qml.CNOT(wires=[i, i + 1])

    return [

        qml.expval(qml.PauliZ(i))

        for i in range(N_QUBITS)

    ]


    