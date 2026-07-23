import pennylane as qml

N_QUBITS = 8

dev = qml.device(

    "default.qubit",

    wires=N_QUBITS

)

@qml.qnode(dev)

def feature_circuit(features):

    for i in range(N_QUBITS):

        qml.RY(features[i], wires=i)

    for i in range(N_QUBITS - 1):
    
        qml.CNOT(wires=[i, i+1])

    return [

        qml.expval(qml.PauliZ(i))

        for i in range(N_QUBITS)

    ]

    