# Random number generator
# using Hadamard logic gate
# Source: http://dataespresso.com/en/2018/07/22/Tutorial-Generating-random-numbers-with-a-quantum-computer-Python/

from projectq.ops import H, Measure
from projectq import MainEngine

"""
This Function creates a new qubit,
applies a Hadamard gate to put it in superposition,
and then measures the qubit to get a random
1 or 0.
"""
def get_random_number(quantum_engine):
    qubit = quantum_engine.allocate_qubit()
    H | qubit
    Measure | qubit
    random_number = int(qubit)
    return random_number


# Storage for results
random_numbers_list = []

# Initialize engine
quantum_engine = MainEngine()

# Generate 10 random numbers
for i in range(10):
    # calling the random number function and append the return to the list
    random_numbers_list.append(get_random_number(quantum_engine))

# Flushes the quantum engine from memory
quantum_engine.flush()

print('Results', random_numbers_list)
