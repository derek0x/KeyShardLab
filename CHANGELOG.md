# CHANGELOG

## 2022-11-05 Lab notes habit
- Added `src/note_keeper.py` to capture evening notes plus a sample entry in `data/lab_notes.md`.
- Documented the journal command for future reference.

## 2022-11-02 Validator checkpoint
- Added `src/validator.py` to flag incomplete log entries before they ship.
- Documented how to run the quick validation check in the README.

## 2022-10-27 Risk guidance refresh
- Added `data/risk_guidelines.json` so the planner can stay in sync with notes I tweak manually.
- Updated planner logic to read that file and surface the same note in every log entry.

## 2022-10-19 Deep dive — log review and sanity checks
- Added a log reader helper and documented how to replay recent bundles.
- Added lightweight unit tests for shard generation and planner routines.

## 2022-10-16 Late evening — storage planning
- Added a planner that recommends device tiers based on the shard count and risk level.
- Expanded the CLI so each bundle prints the plan and logs the suggested distribution for later review.

## 2022-10-10 Evening — project kickoff
- Captured the personal-wip idea for ShardWeaver Vault.
- Added README, lightweight CLI sketch, and core shard utilities.
- Updated gitignore, scaffolding, and usage notes to maintain a logbook feel.
