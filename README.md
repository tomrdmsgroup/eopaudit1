# EOP Audit Application Skeleton

This repository contains a runnable skeleton for the EOP Audit pipeline following the required sequence **Transactions → Signals → Situations → Visibility → Narrative**. The build only affects visibility/reporting; detection and interpretation remain unchanged until official policies are provided.

## Getting started

### Prerequisites
- Python 3.11+

### Installation
No external dependencies are required. From the repository root:

```bash
python -m eopaudit.app sample_data/transactions.json --output-dir output
```

The command runs the pipeline against the provided sample transactions and writes outputs to `output/`:
- `signals.json`
- `situations.json`
- `visibility.json`
- `narrative.txt`

## Architecture
- **Ingestion** (`eopaudit/pipeline/ingestion.py`): loads transactions and enriches them via provider interfaces.
- **Layer-1 Signals** (`eopaudit/pipeline/signals.py`): emits a signal inventory for each transaction, annotated with fiscal period data from the calendar provider.
- **Layer-2 Situations** (`eopaudit/pipeline/situations.py`): placeholder framework that groups signals and marks them as pending definition until the V7 situation catalog is supplied.
- **Visibility Gate** (`eopaudit/pipeline/visibility.py`): applies Layer-3 policy provider results to gate what becomes visible; defaults to withholding when policy is absent.
- **Narrative** (`eopaudit/pipeline/narrative.py`): compiles visibility records into a narrative view while keeping execution scope visibility-only.

## Providers
Stub implementations are supplied for calendar, chart of accounts, identity resolution, and Layer-3 policy in `eopaudit/providers/`. Replace these with real providers when data is available. All provider outputs flow through the pipeline stages and are persisted for inspection.

## MISSING INPUTS
- Layer-2 situation definitions and mappings from the V7 documents (required to replace placeholder grouping in `eopaudit/pipeline/situations.py`).
- Layer-3 policy rules and visibility configurations (required to replace stub behavior in `eopaudit/pipeline/visibility.py` and `eopaudit/providers/policy.py`).
- Chart of Accounts data source (required for enrichment in `eopaudit/pipeline/ingestion.py` and `eopaudit/providers/chart_of_accounts.py`).
- Identity resolution directory or service (required for counterparty canonicalization in `eopaudit/pipeline/ingestion.py` and `eopaudit/providers/identity.py`).
- Authoritative fiscal calendar (required to replace stub monthly calendar in `eopaudit/providers/calendar.py`).
