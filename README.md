# QuantumComputing

Struttura iniziale dello studio sperimentale di Grover: [Grover.ipynb](Grover.ipynb).
Il notebook contiene configurazione, segnaposto e schema dati; non esegue esperimenti.

## Ambiente

Ambiente verificato con Python 3.12.0; le versioni delle dipendenze dirette sono
registrate in `requirements.txt`. Per ricreare un ambiente su Windows:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m ipykernel install --user --name grover --display-name "Python (Grover)"
```

Aprire il notebook in un editor Jupyter e selezionare **Python (Grover)**.
L'ambiente locale preparato in questa fase riutilizza le librerie scientifiche
già installate tramite `--system-site-packages`; Qiskit e Aer sono nella `.venv`.
Una nuova installazione con i comandi sopra è invece isolata.

## Fase successiva

Implementare manualmente oracolo, diffusore e composizione di Grover, poi
verificarli su casi piccoli prima di introdurre gli esperimenti pianificati.
