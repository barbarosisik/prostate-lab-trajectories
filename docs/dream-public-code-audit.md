# DREAM Public Code Audit

## Source and purpose

The public [GuanLab prostate discontinuation repository](https://github.com/GuanLab/prostate_discontinuation) contains code from the winning DREAM discontinuation solution. It does not contain the raw patient files. The code is useful for column-name clues while the official PDS application is under review.

This is documentary evidence only. The gated dictionary and received files remain the authority.

## Useful clues found

The [original data-processing code](https://github.com/GuanLab/prostate_discontinuation/blob/master/code/OriginDataProcess.Rmd) reads `data/CoreTable_training.csv` and uses `RPT` as the patient identifier. It references core fields and baseline values including:

- Patient context: `AGEGRP2`, `BMI`, `RACE_C`, `ECOG_C`.
- Baseline laboratory values: `ALB`, `HB`, `PSA`, `ALP`, `LDH`.
- Disease context: `ANALGESICS`, `BONE`, `LYMPH_NODES`.

The public selected-feature list adds clues for other baseline laboratory fields: `ALT`, `AST`, `CA`, `CREAT`, `NEU`, `PLT`, `TBILI`, `TESTO`, `WBC`, `CREACL`, `MG`, `PHOS`, `TPRO` and `RBC`.

The [main paper code](https://github.com/GuanLab/prostate_discontinuation/blob/master/code/PaperMainCode.Rmd) confirms these core outcome and timing fields:

- `STUDYID`: trial grouping.
- `RPT`: patient identifier.
- `LKADT_P` and `DEATH`: follow-up/death information.
- `DISCONT`: discontinuation indicator.
- `ENDTRS_C`: treatment-ending reason, including adverse event, progression and completion categories in this analysis.
- `ENTRT_PC`: treatment-ending day used by the public analysis.

The code separates records by `RPT` prefixes for ASCENT2, MAINSAIL/CELGENE and VENICE.

## What the code does not prove

- It does not provide patient rows or source counts.
- It does not show the complete `LabValue` column inventory.
- It does not prove that every named baseline laboratory field has longitudinal measurements.
- It does not provide an actual chemotherapy administration table, exact administration dates or per-cycle dose events.
- Its derived early-discontinuation label is a historical challenge definition, not automatically the final treatment-tolerance outcome for this research.

## Research use

These clues informed the field-coverage plan. The safe inventory tool will enumerate every actual column immediately after access is granted. The clues do not justify cleaning, recoding or analysis before the official files are inspected.
