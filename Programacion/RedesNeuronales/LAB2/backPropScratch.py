import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

class NeuralNetwork:
    def __init__(self,input_size=4, hidden_size=10, output_size=3):
        self.input = None
        self.weights1 = np.random.rand(self.input.shape[1], 4)
        self.weights2 = np.random.rand(4, 1)
        self.y = y
        self.output = np.zeros(y.shape)

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))

    def backprop(self):
        d_weights2 = np.dot(self.layer1.T,
           (2*(self.y - self.output) * sigmoid_derivative(self.output)))
        d_weights1 = np.dot(self.input.T,
          (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output),
          self.weights2.T) * sigmoid_derivative(self.layer1)))

        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def train(self, X, y):
        self.output = np.zeros(y.shape)
        self.input = X
        self.y = y
        self.feedforward()
        self.backprop()

X = np.array([[0,0,1], [0,1,1], [1,0,1], [1,1,1]])
y = np.array([[0], [1], [1], [0]])
nn = NeuralNetwork(X, y)

for i in range(1500):
    nn.train(X, y)

print(nn.output)
import pandas as pd

# cargar el dataset de iris desde un archivo csv
data = pd.read_csv("iris.csv")

# separar las características (inputs) de las etiquetas (outputs)
inputs = data.drop("species", axis=1).values
outputs = data["species"].values

# entrenar la red neuronal
nn = NeuralNetwork(input_size=4, hidden_size=10, output_size=3)
nn.train(inputs, outputs, epochs=1000)

# evaluar la red neuronal con el dataset de iris
predictions = nn.predict(inputs)