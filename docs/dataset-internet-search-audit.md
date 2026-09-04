# Dataset Internet Search Audit

**Audit date:** 2026-08-26

## Bottom line

No legitimate public dataset found in this search fully replaces the Prostate Cancer DREAM training data for the fixed research question. The official DREAM release remains the only verified source with repeated routine blood tests, docetaxel-treated metastatic prostate cancer patients and survival information in one package.

MSK-CHORD is the best legitimate dataset that can be downloaded directly without the failed PDS, Synapse or Vivli sign-in flows. It can support a useful partial analysis of treatments, repeated PSA, imaging, progression and survival, but it does not provide the full routine blood panel or actual chemotherapy-cycle administrations required for the main analysis.

No patient-level rows were downloaded or opened during this audit.

## Original DREAM files

The official [Project Data Sphere contribution](https://data.projectdatasphere.org/projectdatasphere/html/content/0abbd47a-dcfb-42c2-a036-af1898ea3c1c) remains the authoritative release. It lists `AllProvidedFiles_149.zip`, the data dictionary and the training, leaderboard and final-scoring packages for 2,070 patients. The official [Synapse project](https://www.synapse.org/Synapse:syn2813558) is the alternate official route, but the signed-in account lacks permission for the combined training resource.

Exact-filename searches across common research repositories did not locate a licensed mirror. The DREAM DOI record points back to Project Data Sphere and supplies no separate content download.

One public participant GitHub repository contains copies of the training CSV files. It has no license, no redistribution permission and no adequate provenance statement. It was treated as an unauthorized copy. No CSV content was opened or downloaded, and it must not be used without written permission from the data owner.

## Best direct candidate: MSK-CHORD

The official [MSK-CHORD paper](https://www.nature.com/articles/s41586-024-08167-5) reports a multi-cancer clinical dataset that includes 3,211 prostate cancer patients. It contains treatment information, tumor-marker results, imaging-derived disease information and overall survival. The paper states that the release is available under a Creative Commons BY-NC-ND 4.0 license through [cBioPortal](https://www.cbioportal.org/study/summary?id=msk_chord_2024).

Verified public metadata:

- Direct official archive: `https://datahub.assets.cbioportal.org/msk_chord_2024.tar.gz`
- Archive size reported by the server: 46,876,803 bytes
- Aggregate cBioPortal event counts across the whole multi-cancer release: 24,028 treatment events and 16,611 laboratory events
- Published prostate cohort size: 3,211 patients
- Available longitudinal laboratory tracks are tumor markers such as PSA, CEA, CA15-3 and CA19-9, not a routine complete blood count or chemistry panel
- Treatment data provide course start and stop intervals, not verified infusion-by-infusion administrations, dose changes or missed cycles

**Verdict:** Strong partial broadening source. It can support prostate treatment, repeated PSA, disease-status and survival work. It cannot replace the full DREAM blood-test trajectory analysis or satisfy the actual pre-chemotherapy-cycle linkage gate.

## Other legitimate candidates

### AACR GENIE BPC Prostate v1.0-public

The official [analytic data guide](https://www.aacr.org/wp-content/uploads/2026/03/GENIE-BPC-Prostate-v1.0-public-Analytic-Data-Guide.pdf) documents 1,116 prostate cancer patients, including stage-IV patients, systemic treatment histories, imaging and medical-oncologist assessments, progression measures and overall survival. The release includes many docetaxel-treated patients.

Its longitudinal tumor-marker dataset contains PSA and testosterone for prostate cancer. Searches of the complete 188-page field guide found no hemoglobin, white blood cell, alkaline phosphatase or other routine blood-panel variables. Drug start and stop intervals are present, but dosing is not.

**Verdict:** Valuable PSA, treatment and outcome broadening source, but not a full blood-test replacement. The complete post-processed files are hosted on Synapse, so this route may still involve account requirements.

### Metastatic Prostate Cancer Project

The [Metastatic Prostate Cancer Project](https://mpcproject.org/Methods.pdf) is a legitimate public cBioPortal study with 123 participants. Aggregate metadata show 64 treatment events and 53 laboratory events. Its official dictionary identifies PSA as the laboratory test and provides treatment course start and stop dates.

**Verdict:** Small, PSA-only and incomplete for the fixed question. It may be useful for a later method demonstration, but it is weaker than MSK-CHORD.

### CHAARTED/E3805

The NCI route remains scientifically useful for repeated PSA, progression and survival. Public documentation still does not prove repeated full blood panels or exact chemotherapy administration dates. Patient-level access is controlled through the current NCI/dbGaP process.

**Verdict:** Keep as planned controlled broadening. It is not an immediate public download and not a DREAM replacement.

### Open Zenodo prostate cohort

The open [600-patient Zenodo dataset](https://zenodo.org/records/15007105) includes albumin, lymphocyte count, CRP, NLR, PSA follow-up, recurrence, metastasis and survival. Its treatment fields focus on surgery, radiation and hormone therapy. It is not a chemotherapy cohort and does not contain serial pre-cycle routine labs.

**Verdict:** Legitimate and directly downloadable, but scientifically unsuitable for the fixed question.

### SWOG S0421 and general hospital datasets

The public SWOG S0421 release dictionary has patient characteristics, pain and quality-of-life follow-up, but no repeated blood-test or chemotherapy-administration tables. General hospital datasets such as MIMIC contain inpatient laboratory results but do not provide a coherent metastatic prostate chemotherapy cohort with outpatient cycle timing and the required cancer outcomes.

**Verdict:** Do not use as replacements.

## Safe recommendation

1. Keep PDS DREAM as the preferred discovery source and preserve the existing approved account as a fallback.
2. Stop the Vivli route for now, as requested by the user.
3. With explicit user approval, download the official MSK-CHORD archive into ignored restricted local storage.
4. Before extraction, reread the repository safety instructions, record the archive size and SHA-256 checksum, list paths safely and confirm the license.
5. Run only the aggregate inventory first. Do not print patient identifiers or patient rows.
6. Use MSK-CHORD only for a feasibility or broadening analysis unless the real file audit proves more laboratory coverage than the public documentation shows.

