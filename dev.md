# Tax Collection Automation — developer guide

Public release 0.3.0 targets CK3 1.20.1.1 and exports the gameplay implementation of 0.3.0-dev.8. README is the player-facing description.

## Goal and policy

Gold income is the optimization objective. This is not a configurable appointment or jurisdiction-layout assistant. The player selects tax decrees; the mod chooses collectors and taxpayers under the native eligibility and capacity rules. Collector ranking uses decree-specific priorities and aptitude. Taxpayer moves use observed native gold previews. These heuristics do not prove a global optimum.

## Why the interface must participate

The required tax appointment/assignment commands and complete final-income calculations are not all available as ordinary script effects and values. Native window models supply legal candidates, jurisdiction state and live tax previews; native GUI commands perform mutations. Reading a model outside its valid window or before refresh can return stale data. The controller therefore owns a bounded interaction pass, pauses game time, validates each command's target and waits for provider readiness. This is the reason for visible pauses and temporarily unavailable manual tax controls compared with Council Assignment Automation and Court Automation.

Window ownership, pass generation, player identity and transaction journals separate stale callbacks from current work. Off requests cancellation and rollback/cleanup rather than abandoning an in-flight write. Completion and safe cancellation restore the previous pause/speed state. The mod does not assume that a missing response means a write succeeded.

## When reconciliation runs

Explicit enablement starts a review. Changes to vacancy or unassigned-taxpayer identities and selected-decree callbacks can request another. Court arrival/adulthood only retry vacancy handling. There is no recurring monthly full scan or promise to replace every incumbent whenever aptitude changes. The legacy monthly callback consumes old work without rescheduling itself.

Serving collectors and assigned taxpayers can be rearranged. Taxpayer transfer batches associated with collector reassignment use a freshly validated complete matrix; paths without that guarantee retain individual execution. Collector appointments still use native appointment commands. Candidate lists and legal destinations remain native. User-selected tax decrees are not automatically replaced.

## Performance and recovery

DEV7 reduced a targeted repeated regression scenario from 19/18/19 seconds to 7/7/7 seconds by batching safe taxpayer transfer commands and reusing ready source windows. This is a scenario-specific measurement, not a promised runtime for every realm. Final DEV8 adds load recovery and a bounded wait for stalled read-only optional previews. After a bounded wait without progress, optional taxpayer rearrangement can be deferred only when the assignment and income invariants allow safe completion. Actual-write completion checks are never skipped.

Unfinished legacy 0.1.x exchange state is held rather than silently interpreted as a new transaction. Players should finish such work with the old version before upgrading, retaining a save backup. Generic recovery after every possible interrupted transaction, succession or character switch is not guaranteed.

## Source-bound verification

The DEV8 acceptance on CK3 1.20.1.1 contains 33 fresh assertions: 15 exact-save load/recovery, 9 intentionally withheld read-only callback checks and 9 normal fire-all/enable/disable checks. The owner subsequently confirmed in-game operation and requested publication. The final lightweight performance review made no gameplay changes. The publication record links these immutable local reports and the source-to-GAME comparison.

All nine game languages are checked statically for key/variant coverage, valid syntax, substitutions and applicable regex compatibility. Localization and publication-copy corrections do not change the accepted gameplay files. GAME-PROD inherits the DEV8 native evidence after comparison; there is no redundant export-only engine run.

## Compatibility and contributions

The five vanilla GUI overrides and two native tax-definition files are listed in README. Custom tcr* GUI/script modules implement the controller and native bridge. Changes to gameplay or callback ordering require the project's isolated native CK3 testing workflow. Publication metadata and translated strings use the shared publication contract. Reports should include the game/mod version, mod list, affected save and the tax-panel state; do not commit private saves or machine-specific paths to this repository.
