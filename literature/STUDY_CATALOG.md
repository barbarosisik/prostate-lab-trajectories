# Study Catalog

## TL;DR

The literature supports studying **many values and combinations**, not only PSA. The strongest direct precedents are: PSA change by about 3 months, ALP change by about 90 days, serial hemoglobin combined with PSA, inflammatory-cell ratios over treatment, and blood-count changes related to docetaxel exposure/tolerance. Most existing work uses baseline values or one fixed follow-up point; our added value is to analyze all repeated pre-cycle measurements, multiple feature types and several outcomes at successive early landmarks.

## Evidence map

| ID | Priority | Study and access | Evidence type | What it gives this project | Main limitation |
|---|---|---|---|---|---|
| LIT-001 | Core | [Armstrong et al., PCWG4 (2026)](https://doi.org/10.1200/JCO-25-02834) | Current consensus | Current terminology, patient characterization, biomarker context-of-use and endpoint framework. | Guidance, not a trajectory-effect study; legacy DREAM data were collected under older conventions. |
| LIT-002 | Core | [Scher et al., PCWG3 (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4872347/) | Consensus | Operational definitions for progression, imaging and clinical benefit; recommends cycle-level PSA, ALP, LDH, chemistry and CBC collection. | Does not establish that a marker change causes benefit. |
| LIT-003 | Core | [Scher et al., PCWG2 (2008)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4010133/) | Historical consensus | Defines PSA and radiographic progression rules likely used by the older source trials; essential for endpoint harmonization. | Older terminology and imaging conventions; use mainly to reconstruct source endpoints. |
| LIT-004 | Core | [Tannock et al., TAX327 (2004)](https://pubmed.ncbi.nlm.nih.gov/15470213/) | Randomized trial | Establishes the docetaxel-plus-prednisone treatment context and major survival, response and safety outcomes. | Treatment-era context differs from current multi-line care; not a full trajectory analysis. |
| LIT-005 | Core | [Guinney et al., DREAM survival challenge (2017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5217180/) | Pooled trial/model study | Confirms ASCENT2, MAINSAIL and VENICE as training data and ENTHUSE-33 as blinded validation; documents trial-level validation and benchmark variables. | Main published models emphasize baseline prognosis, not complete serial trajectories. |
| LIT-006 | Core | [Seyednasrollah et al., DREAM discontinuation challenge (2017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6874023/) | Pooled trial/model study | Defines tolerance as adverse-event-related discontinuation within 3 months/first four cycles; identifies the data and evaluation design for this outcome. | Baseline prediction; early discontinuation is only one part of treatment tolerance. |
| LIT-007 | Core | [Halabi et al. (2014)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3927736/) | Validated prognostic model | Provides key adjustment variables: ECOG, disease site, opioid use, LDH, albumin, hemoglobin, PSA and ALP. | Baseline-only; variables are prognostic and not necessarily modifiable or predictive of treatment benefit. |
| LIT-008 | Core | [Mahmoudian et al. (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6556990/) | DREAM data-processing study | Explicitly describes the event-level `LabValue` table, dates/reference ranges, duplicates, `NOT DONE` values and 13 commonly used labs. | Discarded follow-up values for its model, so it proves availability rather than trajectory performance. |
| LIT-009 | Core | [Deng et al. (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6976944/) | DREAM treatment-tolerance model | Shows how survival and adverse-event discontinuation can be modeled jointly and provides an open reference implementation. | Model targets stratification, not our full longitudinal pre-cycle question. |
| LIT-010 | Supporting | [Armstrong et al., TAX327 nomogram (2007)](https://pubmed.ncbi.nlm.nih.gov/17975152/) | Baseline prognostic model | Supports adjustment for metastasis sites, pain/performance, PSA, ALP and hemoglobin. | Baseline associations only. |
| LIT-011 | Direct | [Armstrong et al., PSA/pain surrogacy (2007)](https://doi.org/10.1200/JCO.2007.11.4769) | Fixed-landmark biomarker study | Tests several PSA changes by 3 months against survival and explicitly separates prognostic value from surrogacy. | PSA-only focus; a 3-month summary can miss earlier or nonlinear patterns. |
| LIT-012 | Direct | [Sonpavde et al., ALP change (2012)](https://pubmed.ncbi.nlm.nih.gov/20888271/) | Fixed-landmark biomarker study | Tests ALP normalization/increase within 90 days and adjusts for PSA change; direct template for joint marker analysis. | Restricted to bone metastases with elevated baseline ALP; not proof that changing ALP causes survival improvement. |
| LIT-013 | Direct | [Vollmer et al., serial hemoglobin and PSA (2002)](https://pubmed.ncbi.nlm.nih.gov/11948112/) | Longitudinal biomarker study | Demonstrates that serial hemoglobin trajectory parameters can add prognostic information to serial PSA. | Older treatment era and curve specification; needs modern replication. |
| LIT-014 | Supporting-direct | [Conteduca et al., persistent NLR (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4951050/) | Repeated biomarker study | Provides a simple pattern template: baseline plus persistence/change at later treatment times. | Enzalutamide rather than chemotherapy; NLR ratios can hide which component changed. |
| LIT-015 | Core-method | [van Houwelingen (2007)](https://doi.org/10.1111/j.1467-9469.2006.00529.x) | Methodology | Foundation for landmark models: at each cycle/time, use only information already observed among patients still at risk. | Requires careful landmark and prediction-window choices. |
| LIT-016 | Core-method | [Zhu, Huang and Li (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7502505/) | Methodology | Handles multiple sparse, irregularly timed biomarkers and warns against naive last-value-only modeling. | Method was demonstrated outside cancer and may be too complex for the first interpretable model. |
| LIT-017 | Supporting-method | [Pickett et al. (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8520610/) | Methodology | Compares Cox landmarking, joint models and random-survival-forest landmarking for complex longitudinal relationships. | Flexible models require strong validation and do not automatically yield clinically simple effects. |
| LIT-018 | Core-reference | [Armstrong et al., biomarker review (2012)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3445625/) | Domain review | Explains prognostic vs predictive vs surrogate biomarkers and covers PSA, LDH, ALP, hemoglobin, albumin and other markers. | Narrative review and older treatment landscape. |
| LIT-019 | Supporting-direct | [de Vries Schultink et al. (2019)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6488109/) | Pharmacodynamic/tolerance study | Shows that neutropenia can reflect docetaxel exposure; prevents simplistic labeling of every blood-count decrease as purely unfavorable. | Post-dose nadir is not the same as a pre-cycle trajectory and must not be mixed with it. |
| LIT-020 | Source context | [Petrylak et al., MAINSAIL (2015)](https://pubmed.ncbi.nlm.nih.gov/25743937/) | Source randomized trial | Defines regimen, cycle schedule, OS endpoint and adverse-event context for one DREAM source. | Experimental arm had additional toxicity; analyze comparator-arm definition carefully. |
| LIT-021 | Source context | [Tannock et al., VENICE (2013)](https://pubmed.ncbi.nlm.nih.gov/23742877/) | Source randomized trial | Defines regimen, multinational population and safety/efficacy context for one DREAM source. | Experimental aflibercept arm differs from the intended docetaxel comparator population. |
| LIT-022 | Source context | [Scher et al., ASCENT2 (2011)](https://pubmed.ncbi.nlm.nih.gov/21483004/) | Source randomized trial | Defines the docetaxel schedules and control arm contributing to DREAM. | Weekly versus 3-weekly schedules make cycle alignment a source-specific issue. |

## How the studies change our analysis plan

### Variables to prioritize, without excluding others

- Direct trajectory precedents: PSA, ALP and hemoglobin.
- Strong baseline adjustment candidates: LDH, albumin, hemoglobin, PSA, ALP, performance status, metastatic site and opioid use.
- Tolerance/exposure candidates: RBC/hemoglobin, neutrophils, WBC, platelets, creatinine/clearance, AST/ALT, calcium and total protein where available.
- Derived combinations: NLR, platelet-to-lymphocyte ratio, ALP with PSA, and hemoglobin with PSA; only when component counts and units are valid.

### Time windows to test

- Pre-cycle landmarks after cycles 1, 2, 3 and 4.
- Calendar-time sensitivity landmarks around weeks 3, 6, 9 and 12.
- Published comparisons at approximately 8 weeks and 90 days for reproducibility checks.
- Each model uses only measurements recorded before its landmark.

### Outcomes to keep separate

- Overall survival.
- Radiographic, clinical and PSA progression, retaining source-specific definitions.
- PSA and imaging response.
- Tolerance: adverse-event discontinuation, dose reduction, delay, missed cycle and severe toxicity where dated.

### Minimum feature families for every usable laboratory test

- Current level and normalized position within its reference range.
- Absolute and percentage change from baseline and prior cycle.
- Robust slope over time and over cycles.
- Acceleration/curvature when at least three observations exist.
- Volatility and time outside the reference interval.
- Missing-test and delayed-cycle indicators.

## What the literature does **not** settle

- There is no universal list of values that a patient can simply “keep low.”
- A favorable direction can differ by marker, baseline range, metastasis pattern and treatment phase.
- An association between a trajectory and an outcome is not evidence that deliberately changing the lab value changes the outcome.
- Published thresholds need replication as continuous effects and in an independent cohort.

