# CHAARTED Public Field Audit

## Why this source matters

CHAARTED/E3805 can test whether a signal found in the narrower PDS discovery group also appears in a different metastatic prostate-cancer setting. Its main value for this project is repeated PSA, linked treatment information, progression and survival.

The current [NCI National Clinical Trials Network data archive page](https://dctd.cancer.gov/research/networks/nctn/data-archive) routes patient-data requests through dbGaP. The older [CHAARTED trial page](https://nctn-data-archive.nci.nih.gov/node/279) remains a useful public description of the linked submissions.

## Publicly supported coverage

| Submission | Public description or dictionary evidence | What it could support | Important limit |
|---|---|---|---|
| D5 | Updated outcomes. The public dictionary lists `group_uid`, overall survival `os`, death status `dead`, cause of death `COD`, time and status for castration-resistant progression, and clinical/radiographic progression fields. | Survival and several progression outcomes. | It is an outcome table, not a repeated-lab table. |
| D7 | Baseline characteristics, prior treatments, disease factors, treatment data and PSA progression. | Adjustment variables, treatment context and PSA progression. | Exact treatment dates, cycles and field names remain unverified without the full dictionary and data. |
| D8 | Longitudinal PSA. | Repeated PSA trajectories. | This is PSA only, not a complete blood panel. Exact collection timing fields remain unverified. |
| D9 | Chemotherapy total dose. | A broad measure of treatment exposure. | A total dose does not prove when each dose was administered. |
| D11 | Additional baseline data, including pathologic stage, PSA and prior treatments, plus non-protocol treatment data. | More complete baseline adjustment and later-treatment context. | It does not publicly prove exact protocol administration dates. |
| D12 | The dictionary lists `group_uid`, `testosterone` in ng/dL and `interval_rando_to_testo` in months. | A limited additional timed laboratory marker, subject to actual row counts. | Public description alone does not establish sufficient repeated measurements. |

All listed submissions use the same blinded patient identifier, `group_uid`, according to the official trial page. This is what makes a linked analysis possible after access is granted.

## Exact fields confirmed from the public D5 dictionary

- `group_uid`: blinded patient identifier.
- `os`: months from randomization to death or last known alive.
- `dead`: death or censoring status.
- `COD`: coded cause of death.
- `TT_CRPC` and `CRPC`: time and status for PSA or clinical progression.
- `TT_clinical_PD` and `clinical_PD`: time and status for clinical progression.
- `radiographic_PD`: radiographic progression indicator.

Source: [official D5 data dictionary](https://nctn-data-archive.nci.nih.gov/system/files/dataset/NCT00309985-D5/NCT00309985-D5-Data-Dictionary.pdf).

## Feasibility conclusion

CHAARTED remains a strong broadening dataset for repeated PSA linked to survival and progression. It is not a replacement for PDS discovery because the public description does not provide repeated full blood panels. It also does not yet prove that a PSA measurement can be matched to the exact day of an actual chemotherapy administration.

The full D7, D8, D9 and D11 dictionaries and patient files must therefore be inspected before writing their cleaning rules. Until then, `treatment data` and `chemotherapy total dose` must not be interpreted as proof of per-cycle administration dates.

## Access note

During this audit, legacy static dictionary links for D7, D8, D9 and D11 redirected to the current NCI archive page when fetched. The official indexed dataset descriptions were readable, and the D5 and D12 dictionaries exposed exact fields. Exact D7, D8, D9 and D11 column inventories remain pending controlled access or a retrievable official dictionary copy.
