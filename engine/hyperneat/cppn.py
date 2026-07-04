import math
import random


class CPPN:

    def __init__(self):

        self.hidden = 8

        self.max_hidden = 32

        self.input_size = 6

        self.output_size = 1

        self.w1 = [

            [
                random.uniform(-1,1)
                for _ in range(self.input_size)
            ]

            for _ in range(self.hidden)
        ]

        self.w2 = [
            random.uniform(-1,1)
            for _ in range(self.hidden)
        ]

        self.hidden_bias = [
            random.uniform(-1,1)
            for _ in range(self.hidden)
        ]

        self.activations = [

            random.choice([

                "gaussian",
                "sine",
                "tanh",
                "sigmoid"

            ])

            for _ in range(self.hidden)

        ]

        self.output_bias = random.uniform(-1,1)

        self.fitness = 0.0

        self.age = 0

        self.id = random.randint(0, 1_000_000)

    def gaussian(self,x):

        return math.exp(-(x*x))
    
    def sigmoid(self,x):

        return 1/(1+math.exp(-x))
    
    def sine(self,x):

        return math.sin(x)
    
    def tanh(self,x):

        return math.tanh(x)
    
    def forward(self, inputs):

        hidden = []

        for neuron, bias in zip(self.w1, self.hidden_bias):

            s = bias

            for w, x in zip(neuron, inputs):

                s += w * x

            activation = self.activations[len(hidden)]

            if activation == "gaussian":

                value = self.gaussian(s)

            elif activation == "sine":

                value = self.sine(s)

            elif activation == "sigmoid":

                value = self.sigmoid(s)

            else:

                value = self.tanh(s)

            hidden.append(value)

        output = self.output_bias

        for h, w in zip(hidden, self.w2):

            output += h * w

        return self.tanh(output)

    def mutate(self):

        if self.fitness > 18:

            mutation_rate = 0.04
            sigma = 0.08

        elif self.fitness > 12:

            mutation_rate = 0.08
            sigma = 0.15

        else:

            mutation_rate = 0.15
            sigma = 0.25

        if self.age > 3000:

            mutation_rate *= 0.75
            sigma *= 0.75

    # Mutate input → hidden weights
        for i in range(self.hidden):

            for j in range(self.input_size):

                if random.random() < mutation_rate:

                    self.w1[i][j] += random.gauss(0, sigma)

                    self.w1[i][j] = max(
                        -2.0,
                        min(2.0, self.w1[i][j])
                    )

        # Mutate hidden → output weights
        for i in range(self.hidden):

            if random.random() < mutation_rate:

                self.w2[i] += random.gauss(0, sigma)

                self.w2[i] = max(
                    -2.0,
                    min(2.0, self.w2[i])
                )

        for i in range(self.hidden):

            if random.random() < mutation_rate:

                self.hidden_bias[i] += random.gauss(0, sigma)

                self.hidden_bias[i] = max(
                    -2.0,
                    min(2.0, self.hidden_bias[i])
                )

        if random.random() < mutation_rate:

            self.output_bias += random.gauss(0, sigma)

            self.output_bias = max(
                -2.0,
                min(2.0, self.output_bias)
            )

        # Occasionally grow the CPPN

        grow_probability = (
            0.04
            if self.fitness < 10
            else 0.01
        )

        if random.random() < grow_probability:

            self.add_hidden_neuron()

        if random.random() < 0.03:

            i = random.randrange(self.hidden)

            self.activations[i] = random.choice([

                "gaussian",
                "sine",
                "tanh",
                "sigmoid"

            ])

    def add_hidden_neuron(self):

        if self.hidden >= self.max_hidden:
            return
        
        if self.hidden > 16 and self.fitness < 8:
            return

        self.hidden += 1

        self.w1.append([
            random.uniform(-1, 1)
            for _ in range(self.input_size)
        ])

        self.w2.append(
            random.uniform(-1, 1)
        )

        self.hidden_bias.append(
            random.uniform(-1, 1)
        )

        self.activations.append(

            random.choice([

                "gaussian",
                "sine",
                "tanh",
                "sigmoid"

            ])

        )