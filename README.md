# Cold Outreach Sanitizer & Batcher

A modular data-pipeline script designed to ingest, sanitize, and chunk raw B2B lead lists for cold outreach campaigns.

## The Problem
Uploading raw, unverified CSV data into email sequencing tools results in high bounce rates, domain blacklisting, and API rate-limit penalties.

## The Solution
This pipeline acts as a data firewall before upload. It sanitizes inputs, enforces strict Regex validation to drop role-based or malformed emails, and automatically splits massive datasets into API-safe execution chunks.

### Core Architecture & Principles Applied
* **Separation of Concerns:** Business logic (`core.py`), file I/O operations (`io_manager.py`), and execution (`main.py`) are strictly isolated.
* **Regex Validation:** Implements strict pattern matching to eliminate invalid formats and generic role-based aliases (e.g., `info@`, `support@`).
* **Memory-Safe Chunking:** Slices valid datasets into configurable, fixed-size batches (e.g., 50 leads per file) to respect email sender limits.
* **Non-Blocking Error Logging:** Uses Python's standard `logging` module to quietly write dropped/invalid records to `sanitizer.log` without crashing the runtime environment.
* **Data Privacy (PII):** The `.gitignore` is configured to strictly exclude all `*.csv` and `*.log` files to prevent the accidental exposure of Personally Identifiable Information (PII).

## Project Structure
```text
├── data/
│   ├── raw/                # Drop 'leads_dump.csv' here
│   └── processed/          # Cleaned, batched files output here
├── sanitizer/
│   ├── core.py             # Data transformation & Regex validation
│   ├── exceptions.py       # Custom domain error handling
│   └── io_manager.py       # CSV DictReader/Writer and logging
└── main.py                 # Pipeline execution entry point
