>**Presentazione del progetto / Project Presentation:** [Visualizza le slide (PDF)](docs/Gestionale_Ristorante_Presentation.pdf)

# Gestionale Ristorante

[Italiano](#italiano) · [English](#english)

---

# Italiano

Applicazione CLI (Command-Line Interface) in Python orientata agli oggetti per la gestione operativa di un ristorante: catalogo piatti, disponibilità, stato tavoli, ciclo di vita degli ordini e reportistica sulle vendite.

Progettato con una separazione netta tra modelli di dominio, servizi applicativi, eccezioni dedicate e interfaccia testuale, con attenzione alla coerenza dei dati e alla leggibilità del codice.

## Funzionalità principali

- **Gestione Menu e Catalogo (`MenuService`, `Menu`, `Piatto`, `Bevanda`)**: caricamento dati iniziali, aggiunta piatti con ID progressivo, ricerca per ID normalizzato (`1` / `"001"`), filtro per categoria, ricerca per nome, modifica prezzo, gestione disponibilità, rimozione e formattazione menu (`[BEVANDA]`).
- **Gestione Tavoli (`TavoliService`, `Tavolo`)**: censimento tavoli con numero e capienza posti, stato libero/occupato e ricerca rapida.
- **Gestione Ordini (`OrdiniService`, `Ordine`)**: apertura ordine con occupazione tavolo, aggiunta/rimozione piatti o porzioni, chiusura ordine con calcolo totale, liberazione tavolo e archiviazione nello storico.
- **Report e Statistiche (`ReportService`)**: incasso totale, scontrino medio, quantità vendute per piatto, piatto più venduto, classifica piatti e incasso per categoria.

## Struttura del progetto

```text
GESTIONALE_RISTORANTE/
├── cli/
│   ├── __init__.py
│   ├── input_utils.py
│   └── interfaccia.py
├── data/
│   ├── __init__.py
│   └── dati_iniziali.py
├── models/
│   ├── __init__.py
│   ├── menu.py
│   ├── ordine.py
│   ├── piatto.py
│   └── tavolo.py
├── services/
│   ├── __init__.py
│   ├── menu_service.py
│   ├── ordini_service.py
│   ├── report_service.py
│   └── tavoli_service.py
├── utils/
│   ├── __init__.py
│   └── formattatori.py
├── exceptions.py
├── main.py
├── prova_test.py
├── .gitignore
├── LICENSE
└── README.md
```

- **`models/`**: entità e collezioni del dominio (`Piatto`, `Bevanda`, `Menu`, `Tavolo`, `Ordine`) con normalizzazione ID e invarianti.
- **`services/`**: orchestrazione dei casi d'uso (`MenuService`, `TavoliService`, `OrdiniService`, `ReportService`).
- **`cli/` & `utils/`**: interazione CLI, validazione input utente (`chiedi_testo`, `chiedi_intero`, `chiedi_prezzo`, `chiedi_conferma`) e formattazione output.
- **`data/`**: dati iniziali preconfigurati per il catalogo e i tavoli.
- **`exceptions.py` & `main.py`**: eccezioni specifiche di dominio ed entry point dell'applicazione.

## Requisiti e avvio

- **Python 3.10+** (nessuna dipendenza esterna obbligatoria per l'esecuzione base).
- **Nota:** su alcuni sistemi Linux/macOS o ambienti virtuali potrebbe essere necessario usare python3 al posto di python.

Avvio dalla radice del progetto:

```bash
python main.py
```

## Regole di dominio e gestione degli errori

- **Piatti (`PiattoNonTrovatoError`, `PiattoNonDisponibileError`)**: impedisce di operare su ID inesistenti o aggiungere piatti non disponibili a un ordine.
- **Tavoli (`TavoloOccupatoError`)**: impedisce di aprire un nuovo ordine su un tavolo già occupato.
- **Ordini (`OrdineNonTrovatoError`, `OrdineChiusoError`, `DatiNonValidiError`)**: vieta la chiusura di ordini vuoti, blocca modifiche su ordini chiusi e valida ID, quantità e prezzi.

## Test

Esecuzione della suite di verifica dalla radice:

```bash
python -B prova_test.py
```

## Sviluppi futuri

- Persistenza su file (JSON/CSV) o database SQLite.
- Estensione della suite di test con `pytest`.
- Esportazione dei report di vendita.

## Autore e Contatti

- **Autore**: `Natalia Mardare`
- **GitHub**: `https://github.com/nataliamardare4`
- **LinkedIn**: `https://www.linkedin.com/in/nataliamardare`

## Copyright e Licenza

- **Copyright**: Copyright © 2026 `Natalia Mardare`.
- **Licenza**: Progetto open-source distribuito sotto licenza **MIT** (consulta il file [`LICENSE`](LICENSE) nella cartella radice per i termini completi).

---

# English

Object-oriented Python CLI (Command-Line Interface) application for restaurant operations: menu catalog, dish availability, table status, order lifecycle, and sales reporting.

Designed with a clear separation between domain models, application services, custom exceptions, and text interface, focusing on data consistency and code clarity.

## Key Features

- **Menu & Catalog Management (`MenuService`, `Menu`, `Piatto`, `Bevanda`)**: initial data loading, adding dishes with sequential IDs, lookup by normalized ID (`1` / `"001"`), category filtering, name search, price updates, availability toggling, item removal, and formatted menu rendering (`[BEVANDA]`).
- **Table Management (`TavoliService`, `Tavolo`)**: table setup with number and seat capacity, free/occupied status tracking, and lookup.
- **Order Management (`OrdiniService`, `Ordine`)**: opening orders while occupying the table, adding/removing dishes or portions, closing orders with total calculation, releasing the table, and archiving into history.
- **Reports & Analytics (`ReportService`)**: total revenue, average ticket, units sold per dish, top-selling dish, top dishes ranking, and revenue by category.

## Project Structure

```text
GESTIONALE_RISTORANTE/
├── cli/
│   ├── __init__.py
│   ├── input_utils.py
│   └── interfaccia.py
├── data/
│   ├── __init__.py
│   └── dati_iniziali.py
├── models/
│   ├── __init__.py
│   ├── menu.py
│   ├── ordine.py
│   ├── piatto.py
│   └── tavolo.py
├── services/
│   ├── __init__.py
│   ├── menu_service.py
│   ├── ordini_service.py
│   ├── report_service.py
│   └── tavoli_service.py
├── utils/
│   ├── __init__.py
│   └── formattatori.py
├── exceptions.py
├── main.py
├── prova_test.py
├── .gitignore
├── LICENSE
└── README.md
```

- **`models/`**: domain entities and collections (`Piatto`, `Bevanda`, `Menu`, `Tavolo`, `Ordine`) with ID normalization and state invariants.
- **`services/`**: application use-case orchestration (`MenuService`, `TavoliService`, `OrdiniService`, `ReportService`).
- **`cli/` & `utils/`**: CLI interaction, validated user prompts (`chiedi_testo`, `chiedi_intero`, `chiedi_prezzo`, `chiedi_conferma`), and output formatting.
- **`data/`**: initial seed data for menu items and tables.
- **`exceptions.py` & `main.py`**: custom domain exceptions and application entry point.

## Requirements & Run

- **Python 3.10+** (no external dependencies required for core execution).

Run from the project root:

```bash
python main.py
```

## Domain Rules & Error Handling

- **Dishes (`PiattoNonTrovatoError`, `PiattoNonDisponibileError`)**: prevents lookups on missing IDs or adding unavailable dishes to an order.
- **Tables (`TavoloOccupatoError`)**: prevents opening a new order on an already occupied table.
- **Orders (`OrdineNonTrovatoError`, `OrdineChiusoError`, `DatiNonValidiError`)**: blocks closing empty orders, prevents modifying closed orders, and validates IDs, quantities, and prices.

## Testing

Run the test suite from the project root:

```bash
python -B prova_test.py
```

## Future Improvements

- File persistence (JSON/CSV) or SQLite database storage.
- Expanding automated tests with `pytest`.
- Sales report export.

## Author & Contact

- **Author**: `Natalia Mardare`
- **GitHub**: `https://github.com/nataliamardare4`
- **LinkedIn**: `https://www.linkedin.com/in/nataliamardare`

## Copyright & License

- **Copyright**: Copyright © 2026 `Natalia Mardare`.
- **License**: Open-source project released under the **MIT License** (see the [`LICENSE`](LICENSE) file in the project root for full terms).