from qml.kernel import QuantumKernel
import numpy as np

kernel = QuantumKernel()

x1 = np.random.rand(8)
x2 = np.random.rand(8)

print("Similarity(x1,x2):")
print(kernel.similarity(x1, x2))

print()

print("Similarity(x1,x1):")
print(kernel.similarity(x1, x1))

print()

X = np.random.rand(5, 8)

K = kernel.kernel_matrix(X)

print("Kernel Matrix:")

print(K)

print()

print("Shape:")

print(K.shape)