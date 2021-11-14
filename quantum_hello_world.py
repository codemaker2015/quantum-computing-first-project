# -*- coding: utf-8 -*-
"""QuantumDemo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tbWxbmSYKZkTVQTPWKfbIYJmMcT4UCeV

# FIRST STEPS IN QISKIT

In this notebook, we are going to learn how to use Qiskit to define a simple circuit and to execute it on both simulators and the quantum computers of the IBM Quantum Experience.. 

We start by importing the necessary packages.
"""

# !pip install qiskit
# !pip install pylatexenc

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

from qiskit import *
from qiskit.visualization import *
from qiskit.tools.monitor import *

"""## Defining the circuit

Now, we are going to define a very simple circuit: we will use the $H$ gate to put a qubit in superposition and then we will measure it
"""

# Let's create a circuit to put a state in superposition and measure it

circ = QuantumCircuit(1,1) # We use one qubit and also one classical bit for the measure result 

circ.h(0) #We apply the H gate

circ.measure(range(1),range(1)) # We measure

circ.draw() #We draw the circuit

"""We can also very easily obtain the *qasm* code for the circuit."""

print(circ.qasm())

"""## Running the circuit on simulators

Once that we have defined the circuit, we can execute it on a simulator. 
"""

# Executing on the local simulator

backend_sim = Aer.get_backend('qasm_simulator') # We choose the backend

job_sim = execute(circ, backend_sim, shots=1024) # We execute the circuit, selecting the number of repetitions or 'shots'

result_sim = job_sim.result() # We collect the results

counts = result_sim.get_counts(circ) # We obtain the frequency of each result and we show them 
print(counts) 
plot_histogram(counts)

"""We can also run the circuit run the circuit with a simulator that computes the final state. For that, we need to create a circuit with no measures """

# Execution to the get the statevector

circ2 = QuantumCircuit(1,1)

circ2.h(0)

backend = Aer.get_backend('statevector_simulator') # We change the backend

job = execute(circ2, backend) # We execute the circuit with the new simulator. Now, we do not need repetitions

result = job.result() # We collect the results and access the stavector 
outputstate = result.get_statevector(circ2)
print(outputstate)

"""Finally, we can also obtain the unitary matrix that represents the action of the circuit"""

backend = Aer.get_backend('unitary_simulator') # We change the backend again

job = execute(circ2, backend) # We execute the circuit

result = job.result() # We collect the results and obtain the matrix
unitary = result.get_unitary()
print(unitary)

"""Now, we are going to use the quantum computers at the IBM Quantum Experience to use our circuit """

# Connecting to the real quantum computers
from qiskit import IBMQ
provider = IBMQ.enable_account("d781f86b7c49e47d00f5a7d7d316b35aa1a926beb5dcd74716c6351c82bf17cdb4360df36d4357584404c451c50c91e2383073a31a5eed911bf6a7631e36c98f") # We load our account 
provider.backends() # We retrieve the backends to check their status

for b in provider.backends():
    print(b.status().to_dict())

"""We can execute the circuit on IBM's quantum simulator (supports up to 32 qubits). We only need to select the appropriate backend."""

# Executing on the IBM Q Experience simulator

backend_sim = provider.get_backend('ibmq_qasm_simulator') # We choose the backend

job_sim = execute(circ, backend_sim, shots=1024) # We execute the circuit, selecting the number of repetitions or 'shots'

result_sim = job_sim.result() # We collect the results

counts = result_sim.get_counts(circ) # We obtain the frequency of each result and we show them 
print(counts) 
plot_histogram(counts)

"""To execute on one of the real quantum computers, we only need to select it as backend. We will use *job_monitor* to have live information on the job status """

# Executing on the quantum computer

backend = provider.get_backend('ibmq_armonk')

job_exp = execute(circ, backend=backend)
job_monitor(job_exp)

"""When the job is done, we can collect the results and compare them to the ones obtaine with the simulator"""

result_exp = job_exp.result()
counts_exp = result_exp.get_counts(circ)
plot_histogram([counts_exp,counts], legend=['Device', 'Simulator'])

