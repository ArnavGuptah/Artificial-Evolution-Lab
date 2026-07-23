import pennylane as qml
import torch

print("START")

dev = qml.device("default.qubit", wires=2)

@qml.qnode(dev, interface="torch")
def circuit(inputs, weights):

    qml.RX(inputs[0], wires=0)
    qml.RY(inputs[1], wires=1)

    qml.CNOT(wires=[0, 1])

    qml.RY(weights[0], wires=0)
    qml.RY(weights[1], wires=1)

    return [
        qml.expval(qml.PauliZ(0)),
        qml.expval(qml.PauliZ(1))
    ]

print("QNODE OK")

weight_shapes = {
    "weights": (2,)
}

layer = qml.qnn.TorchLayer(
    circuit,
    weight_shapes
)

print("TORCHLAYER OK")

x = torch.rand(2)

print("INPUT =", x)

y = layer(x)

print("OUTPUT =", y)

print("END")