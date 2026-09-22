# /// script
# dependencies = [
#     "qiskit",
#     "qiskit-aer",
#     "qiskit-ibm-runtime",
#     "matplotlib",
#     "numpy"
# ]
# ///

import time
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error
from qiskit.providers.fake_provider import GenericBackendV2

def build_grover_circuit(n_qubits=8, iterations=12):
    """Costruisce il circuito dell'algoritmo di Grover per n_qubits + 1 ancilla."""
    q = QuantumRegister(n_qubits + 1, 'q')
    c = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(q, c, name="Grover_8bit")

    # 1. Inizializzazione
    qc.h(q[0:n_qubits])
    qc.x(q[n_qubits])
    qc.h(q[n_qubits])

    # 2. Iterazioni di Grover
    for _ in range(iterations):
        # Oracolo per |1...1>
        qc.mcx(q[0:n_qubits], q[n_qubits])

        # Diffusore
        qc.h(q[0:n_qubits])
        qc.x(q[0:n_qubits])
        qc.mcx(q[0:n_qubits], q[n_qubits])
        qc.x(q[0:n_qubits])
        qc.h(q[0:n_qubits])

    # 3. Misurazione dei soli qubit dati
    qc.measure(q[0:n_qubits], c[0:n_qubits])
    return qc

def run_experiment():
    n_qubits = 8
    shots = 1024
    iterations = 12
    target_state = "1" * n_qubits

    print("==================================================")
    print(f"  BENCHMARK ALGORITMO DI GROVER ({n_qubits} QUBIT)  ")
    print("==================================================\n")

    circuit = build_grover_circuit(n_qubits, iterations)

    # -------------------------------------------------------------
    # MODALITÀ 1: Simulazione Ideale Locale (Statevector)
    # -------------------------------------------------------------
    print("--> 1. Esecuzione: Simulazione Ideale (Statevector)...")
    sim_ideal = AerSimulator(method="statevector")
    t0 = time.time()
    job_ideal = sim_ideal.run(circuit, shots=shots)
    counts_ideal = job_ideal.result().get_counts()
    time_ideal = time.time() - t0

    prob_ideal = (counts_ideal.get(target_state, 0) / shots) * 100
    print(f"    Tempo: {time_ideal:.4f} s | Probabilità Target ({target_state}): {prob_ideal:.2f}%\n")

    # -------------------------------------------------------------
    # MODALITÀ 2: Simulazione Tensor Network (Matrix Product State)
    # -------------------------------------------------------------
    print("--> 2. Esecuzione: Simulazione Tensor-Network (MPS)...")
    sim_mps = AerSimulator(method="matrix_product_state")
    transpiled_mps = transpile(circuit, sim_mps, optimization_level=1)
    t0 = time.time()
    job_mps = sim_mps.run(transpiled_mps, shots=shots)
    counts_mps = job_mps.result().get_counts()
    time_mps = time.time() - t0

    prob_mps = (counts_mps.get(target_state, 0) / shots) * 100
    print(f"    Tempo: {time_mps:.4f} s | Probabilità Target ({target_state}): {prob_mps:.2f}%\n")

    # -------------------------------------------------------------
    # MODALITÀ 3: Simulazione con Rumore (Fake Backend / Hardware)
    # -------------------------------------------------------------
    print("--> 3. Esecuzione: Simulazione con Rumore (Fake Backend 127-qubit)...")
    fake_backend = GenericBackendV2(num_qubits=127, seed=42)
    
    # Transpilazione per l'architettura rumorosa
    transpiled_circuit = transpile(circuit, fake_backend, optimization_level=1)
    
    sim_noisy = AerSimulator.from_backend(fake_backend)
    t0 = time.time()
    job_noisy = sim_noisy.run(transpiled_circuit, shots=shots)
    counts_noisy = job_noisy.result().get_counts()
    time_noisy = time.time() - t0

    prob_noisy = (counts_noisy.get(target_state, 0) / shots) * 100
    print(f"    Tempo: {time_noisy:.4f} s | Probabilità Target ({target_state}): {prob_noisy:.2f}%")
    print(f"    Profondità circuito traspilato: {transpiled_circuit.depth()}")
    print(f"    Numero totale di porte: {sum(transpiled_circuit.count_ops().values())}\n")

    # -------------------------------------------------------------
    # TABELLA RIASSUNTIVA DEI RISULTATI
    # -------------------------------------------------------------
    print("==================================================")
    print("               RIEPILOGO CONFRONTO                ")
    print("==================================================")
    print(f"{'Modalità':<25} | {'Tempo (s)':<10} | {'P(Successo)':<12}")
    print("-" * 55)
    print(f"{'1. Ideale (Statevector)':<25} | {time_ideal:<10.4f} | {prob_ideal:.2f}%")
    print(f"{'2. Tensor-Network (MPS)':<25} | {time_mps:<10.4f} | {prob_mps:.2f}%")
    print(f"{'3. Con Rumore (Hardware)':<25} | {time_noisy:<10.4f} | {prob_noisy:.2f}%")
    print("==================================================")

if __name__ == "__main__":
    run_experiment()

# -------------------------------------------------------------------
# NOTE PER LA RELAZIONE FINALE (solo commenti, non eseguiti)
# -------------------------------------------------------------------
# ### Struttura per la Relazione Finale (PDF / Jupyter Notebook)
#
# ### Seguendo le linee guida del docente, la tua relazione dovrà essere
# articolata in questo modo:
#
# 1. **Piattaforma Utilizzata**:
#    * **Framework**: Qiskit 1.x + Qiskit Aer.
#    * **Ambiente**: Python locale (Visual Studio Code / Jupyter Notebook).
#    * **Simulatori usati**: AerSimulator (metodi statevector e
#      matrix_product_state) e GenericBackendV2 (per la modellazione del
#      rumore quantistico).
#
# 2. **Descrizione dell'Algoritmo**:
#    * Spiegazione dell'Algoritmo di Grover (ricerca in database non
#      strutturato con accelerazione quadratica O(sqrt(N))).
#    * Dettaglio dell'oracolo (U_omega) e del diffusore (D).
#    * Spiegazione della scelta di 12 iterazioni per n=8
#      (approx pi/4 * sqrt(256) = 12.56).
#
# 3. **Discussione e Analisi dei Risultati**:
#    * **Confronto delle prestazioni**: Tabella con tempi di esecuzione e
#      frequenze di successo.
#    * **Analisi dell'effetto del rumore**: spiegare perché nella
#      simulazione con rumore la probabilità cala, dovuto all'elevato
#      numero di porte CNOT/CX generate dalla decompilazione della porta
#      multi-controllata mcx.
#
# Eseguendo lo script generato tramite il comando
# "py grover_experiment_benchmark.py", avrai tutti i dati numerici e le
# metriche pronte per la compilazione della relazione.
# -------------------------------------------------------------------