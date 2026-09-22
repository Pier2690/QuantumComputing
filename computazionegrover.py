# /// script
# dependencies = [
#     "qiskit",
#     "qiskit-aer",
#     "numpy"
# ]
# ///

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

backend = AerSimulator(method="statevector")
shots = 1024

q = QuantumRegister(9, 'q')
c = ClassicalRegister(8, 'c')
qc = QuantumCircuit(q, c)

# 1. Inizializzazione dei qubit di lavoro in sovrapposizione e dell'ancilla in |->
qc.h(q[0:8])
qc.x(q[8])
qc.h(q[8])

# 2. Per 8 qubit occorrono 12 iterazioni per amplificare la probabilità
iterations = 12

for _ in range(iterations):
    # --- A. ORACOLO (per il target |11111111>) ---
    # Si usa qc.mcx fornendo la lista dei qubit di controllo e il qubit target
    qc.mcx(q[0:8], q[8])

    # --- B. DIFFUSORE DI GROVER ---
    qc.h(q[0:8])
    qc.x(q[0:8])
    
    # Inversione di fase attorno alla media
    qc.mcx(q[0:8], q[8])
    
    qc.x(q[0:8])
    qc.h(q[0:8])

# 3. Misurazione dei primi 8 qubit
qc.measure(q[0:8], c[0:8])

# Esecuzione e stampa dei risultati
job = backend.run(qc, shots=shots)
job_result = job.result()
counts = job_result.get_counts(qc)

print("Risultati della misurazione:", counts)