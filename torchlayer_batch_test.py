import torch
from qml.vqc import VQC


model = VQC()
X = torch.rand(4, 8)
print(model.model(X))