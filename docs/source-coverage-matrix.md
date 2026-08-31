# Source Coverage Matrix

## Reading this matrix

- **Yes (public)**: confirmed in official public source documentation; actual column values still require source-file verification.
- **Partial (public)**: some required information is documented, but the full outcome/feature family is not supported.
- **Unknown**: must be resolved from the gated dictionary or actual source files.
- **No listed table**: the official release inventory contains no table at the required grain; an unlisted column could still change the conclusion and will be checked.
- **Not yet audited**: intentionally deferred until the PDS column audit is complete.

## Planned-source matrix

| Source | Intended role | Serial labs | Actual chemotherapy cycles/doses | Overall survival | Progression | Response | Treatment tolerance | Current verdict |
|---|---|---|---|---|---|---|---|---|
| PDS DREAM training: ASCENT2, MAINSAIL, VENICE | Discovery | Yes (public), through day 84 | Unknown; no administration table listed | Yes (public), patient-level | Unknown | Partial/unknown; lesion events exist with ASCENT2 exception | Partial: patient-level early AE discontinuation; no AE event table listed | Package secured in private cloud storage; latest handoff requires next-agent plan explanation and approval first; local audit not run |
| PDS DREAM ENTHUSE-33/AZ leaderboard/final | Potential validation | Baseline only in original challenge release; current final package unknown | Unknown | Withheld in original challenge release; current visibility unknown | Unknown | Baseline/event visibility unknown | Outcome withheld in original challenge release | Do not select as validation until current package is audited |
| CHAARTED/E3805 D5/D7/D8/D9/D11 | Controlled broadening | D8 is officially described as longitudinal PSA | Partial (public): D7 has treatment data and D9 has total dose; exact administrations are not proven | Yes (public): D5 has `os` and `dead` | Yes/partial (public): D5 has CRPC, clinical and radiographic progression fields; D7 has PSA progression | PSA response may be derived only after D8 timing and fields are verified | Unknown | Strong PSA broadening source; patient-level access is routed through dbGaP |
| Vivli FIRSTANA/PROSELICA/TROPIC | Independent validation candidate | Advertised trial data are insufficient evidence | Unknown | Expected | Unknown by exact definition | Unknown | Unknown | Column-level enquiry required after PDS audit |
| Flatiron Prostate Panoramic | Real-world validation candidate | Vendor verification required for all CBC/CMP, not PSA only | Vendor verification required | Expected but exact death source needed | Vendor-defined/abstracted; exact dates needed | Unknown | Dose/delay/reduction/AE fields require verification | Do not purchase/select before variable-list audit |

## PDS trial-level coverage

| Trial label | PDS `STUDYID` | Patients | Role in original challenge | Longitudinal lab window | Lesion events | Outcome visibility | Timing caveat |
|---|---|---:|---|---|---|---|---|
| ASCENT2 | `ASCENT2` | 476 | Training | Through day 84 (public) | No event-level lesion table | Training outcomes included (public) | Weekly versus three-weekly trial schedules require arm- and schedule-specific cycle definitions; some reference dates use consent |
| MAINSAIL | `CELGENE` | 526 | Training | Through day 84 (public) | Yes (public) | Training outcomes included (public) | Lab/vital/lesion reference is generally first treatment date; verify exceptions |
| VENICE | `EFC6546` | 598 | Training | Through day 84 (public) | Yes (public) | Training outcomes included (public) | Lesion/vital reference may be randomization rather than first treatment |
| ENTHUSE-33 | `AZ` | 470 | 157 leaderboard + 313 final scoring | Baseline only in original challenge evaluation files | Yes in documented table family | Dependent outcomes withheld in original challenge | Current PDS final-scoring package contents must be inspected before assuming validation is possible |

## PDS table-by-requirement matrix

| Required information | `CoreTable` | `LabValue` | `LesionMeasure` | `PriorMed` | `MedHistory` | `VitalSign` | Current coverage conclusion |
|---|---|---|---|---|---|---|---|
| Patient/trial join | Expected | Expected | Expected | Expected | Expected | Expected | Candidate keys require actual uniqueness/unmatched audit |
| Laboratory name/result/unit/status/range | Baseline summaries only | Primary source | No | No | No | No | Event-level source exists; exact complete column inventory is gated |
| Laboratory collection day | No | `LBDT_PC` | No | No | No | No | Relative timing exists, reference-date exceptions documented |
| Cycle/visit label | Unknown | `VISIT` expected from public baseline logic | `VISIT` | No | Screening | `VISIT` | May support nominal-cycle analyses; not proof of actual administration |
| Actual chemotherapy administration date | No listed event table | No documented administration field | No | No | No | No | Not established |
| Actual/planned dose and dose reduction | Treatment IDs only | No | No | No | No | No | Not established |
| Delay or missed cycle | No listed event table | Missing/visit patterns only | No | No | No | Visit patterns only | Cannot be defined reliably from public evidence |
| Overall survival | `DEATH`, `LKADT_P` | No | No | No | No | No | Patient-level OS/censoring publicly documented for training |
| Radiographic progression | Unknown | No | Measurements only | No | No | No | Not established; lesion events are not automatically progression events |
| Clinical progression | Unknown | No | No | No | No | No | Not established |
| PSA progression/response | Unknown outcome field | PSA lab values | No | No | No | No | Trajectory can be derived; source-defined endpoint is unknown |
| Imaging response | Unknown | No | Measurements/standard results | No | No | No | Partial; response criteria/date fields need audit |
| AE-related early discontinuation | `DISCONT`, `ENTRT_PC`, `ENDTRS_C` | No | No | No | No | No | Historical DREAM endpoint supported at patient level |
| Adverse-event term/grade/date | No listed event table | No | No | No | No | No | Not supported by listed release tables |
| Baseline covariates | Primary summaries | Baseline labs | Baseline lesions except ASCENT2 raw absence | Baseline medications | Baseline diagnoses except ASCENT2 raw absence | Baseline vital signs | Broad baseline adjustment context is publicly documented |

## Critical unresolved questions

1. What are all columns, types and missing-value codes in dictionary `syn3348062`?
2. What is the exact patient identifier and is `STUDYID` + patient ID sufficient across all six tables?
3. Does `LabValue.VISIT` encode cycle number consistently enough to reproduce cycles 1–4?
4. Is any actual treatment-administration date/dose information embedded in `CoreTable` or another supplied column despite the absence of a treatment event table?
5. How many patients/tests have at least two, three and four observations, per trial and cycle?
6. Can a result be aligned to the next **actual** administration, or only to nominal calendar/visit landmarks?
7. Are progression and response endpoint fields present beyond lesion measurements and PSA values?
8. Does the current PDS final-scoring package expose ENTHUSE-33 outcomes or longitudinal data that were originally withheld?

These questions must be answered before the cleaning and restructuring specification is written.

## Waiting-period evidence

- [`chaarted-public-field-audit.md`](chaarted-public-field-audit.md) records the public D5, D7, D8, D9, D11 and D12 coverage and the limits of that evidence.
- [`dream-public-code-audit.md`](dream-public-code-audit.md) records column clues from the public winning-solution code without treating them as an official dictionary.
- [`raw-data-inventory-tool.md`](raw-data-inventory-tool.md) documents the aggregate-only inspection tool prepared for the approved files.
