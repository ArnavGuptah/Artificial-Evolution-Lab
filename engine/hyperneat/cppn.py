import math
import random


class CPPN:

    def __init__(self):

        self.hidden = 8

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

    def gaussian(self,x):

        return math.exp(-(x*x))
    
    def sigmoid(self,x):

        return 1/(1+math.exp(-x))
    
    def sine(self,x):

        return math.sin(x)
    
    def tanh(self,x):

        return math.tanh(x)