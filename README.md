# P40 Telemetry Gauge sul Thermalright LCD

Estendere il controller HID Python esistente per leggere metriche GPU (TDP, temp, VRAM, tok/s) via API locale e renderizzarle come gauge animati vettoriali sul display 2.0" della Thermalright, integrando un toggle per mostrare i benchmark dei modelli attivi.

## Struttura del progetto

- `src/`: contiene il codice sorgente Python
- `assets/`: contiene risorse statiche (immagini, font, ecc.)

## Requisiti

Vedere `requirements.txt` per le dipendenze Python.

## Installazione

1. Clonare il repository
2. Installare le dipendenze: `pip install -r requirements.txt`
3. (Opzionale) Copiare `.env.example` in `.env` e configurare le variabili d'ambiente per l'API locale

## Uso

### Modalità telemetria (default)

Eseguire lo script principale per visualizzare le metriche GPU in tempo reale sul display LCD:

```bash
python src/app.py
```

### Modalità benchmark

Eseguire un benchmark manuale per misurare le prestazioni di token generation:

```bash
python src/app.py --mode benchmark
```

### Opzioni disponibili

- `--mode`: scegliere tra `telemetry` (default) e `benchmark`
- `--interval`: intervallo di aggiornamento in secondi per la modalità telemetria (default: 1.0)
- `--output-dir`: directory dove salvare i gauge SVG (utile per debug, default: `.`)

## Esempi

```bash
# Telemetria con aggiornamento ogni 2 secondi
python src/app.py --mode telemetry --interval 2.0

# Benchmark e salvataggio dei gauge in una cartella specifica
python src/app.py --mode benchmark --output-dir ./gauges
```

## Architettura

Il progetto è composto da tre moduli principali:

1. **hid_controller.py**: gestisce la comunicazione HID con il display Thermalright LCD (attualmente in modalità simulazione).
2. **gauge_renderer.py**: crea gauge vettoriali utilizzando la libreria `cairo` e li esporta come SVG.
3. **app.py**: orchestrator che legge le metriche (simulate o da API locale), chiama il renderer e invia i dati al controller HID.

## Stato

✅ COMPLETATO — 2026-06-11
- Inizializzato repository progetto
- Implementato skeleton controller HID Python
- Sviluppato renderer gauge vettoriale con toggle visualizzazione
- Aggiunto script benchmark manuale
- Tutte le fasi del piano di lavoro sono state completate

## Nota sulla privacy

Questo progetto non contiene path assoluti, dati personali o credenziali hardcoded.
Tutte le configurazioni devono essere fornite tramite variabili d'ambiente o file `.env` (non incluso nel repository).