# Quantum teleportation emulation
# Source: http://dataespresso.com/en/2018/07/29/Tutorial-Getting-started-with-Quantum-Teleportation-Python/

from projectq.ops import All, H, CNOT, Measure, X, Z
from projectq import MainEngine

def create_bell_pair(engine):
    # Allocate 2 qubits
    qubit_one = engine.allocate_qubit()
    qubit2 = engine.allocate_qubit()

    ''' 
        Hadamard gate to put Qubit one in superposition
        This sets the value of a equal probability of being 1 or 0
        '''
    H | qubit_one

    '''
    CNOT gate to flip the second Qubit conditionally
    on the first qubit being in the state |1⟩
    '''
    CNOT | (qubit_one, qubit2)

    return qubit_one, qubit2



def create_message(quantum_engine='',qubit_one='', message_value = 0):

    qubit_to_send = quantum_engine.allocate_qubit()
    if message_value == 1:
        '''
        setting the qubit to positive if message_value is 1
        by flipping the base state with a Pauli-X gate.
        '''
        X | qubit_to_send


    # entangle the original qubit with the message qubit
    CNOT | (qubit_to_send, qubit_one)

    '''
    1 - Put the message qubit in superposition 
    2 - Measure out the two values to get the classical bit value
        by collapsing the state. 
    '''
    H | qubit_to_send
    Measure | qubit_to_send
    Measure | qubit_one

    # The qubits are now turned into normal bits we can send through classical channels
    classical_encoded_message = [int(qubit_to_send), int(qubit_one)]

    return classical_encoded_message


def message_reciever(quantum_engine, message, qubit2):
    '''
    Pauli-X and/or Pauli-Z gates are applied to the Qubit,
    conditionally on the values in the message.
    '''
    if message[1] == 1:
        X | qubit2
    if message[0] == 1:
        Z | qubit2

    '''
    Measuring the Qubit and collapsing the state down to either 1 or 0
    '''
    Measure | qubit2

    quantum_engine.flush()

    recieved_bit = int(qubit2)
    return recieved_bit

def send_receive(bit=0):

    # Create bell pair
    qubit_one, qubit_two = create_bell_pair(quantum_engine)

    # Entangle the bit with the first qubit
    classical_encoded_message = create_message(quantum_engine=quantum_engine, qubit_one=qubit_one, message_value=bit)

    # Teleport the bit and return it back
    return message_reciever(quantum_engine, classical_encoded_message, qubit_two)


def send_full_message(message='DataEspresso.com'):
    # Convert the string into binary values
    binary_encoded_message = [bin(ord(x))[2:].zfill(8) for x in message]
    print('Message to send: ', message)
    print('Binary message to send: ', binary_encoded_message)

    '''
    The binary message is divided into a list of each word represented in binary.
    We iterate through each word, and then each bit in the letter.
    Then we append the bits to an list to get back the letter representation
    '''
    received_bytes_list = []
    for letter in binary_encoded_message:
        received_bits = ''
        for bit in letter:
            received_bits = received_bits + str(send_receive(int(bit)))
        received_bytes_list.append(received_bits)

    binary_to_string = ''.join([chr(int(x, 2)) for x in received_bytes_list])
    print('Received Binary message: ', received_bytes_list)
    print('Received message: ', binary_to_string)



# Init engine
quantum_engine = MainEngine()

message = 'Quantum Break'
send_full_message(message)

