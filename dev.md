# Tax Collection Automation — developer guide

Version 0.1.1 targets CK3 1.20.0.4. See [README](README.md) for installation,
player instructions, compatibility and known limitations.

## Runtime structure

- `common/scripted_guis/` connects the checkbox and native interface workers to
  the mod's scripted state.
- `common/scripted_effects/`, `common/scripted_triggers/` and
  `common/script_values/` manage candidates, taxpayer comparisons and exchange
  recovery.
- `common/on_action/` schedules monthly reviews and handles supported player
  and government transitions.
- `gui/` contains the controller and the extensions to native tax windows.
- `localization/` contains the mod's player-facing text.

Opt-in belongs to the current player character. A pending monthly request does
not start a second pass while one is already in progress. Disabling automation
stops new work and lets an unfinished pair exchange restore its participants.
Completed appointments and allocations remain ordinary game state.

Collector appointments use the native candidate list, legality checks and
aptitude score. Taxpayer destinations are compared using the native gold
preview. Equal scores keep the existing appointment or assignment. The mod
preserves the player's tax decrees.

The controller uses CK3's native GUI commands for appointments and taxpayer
assignment. Window-local data must be read inside the corresponding native
window; the tax manager publishes its current owner for global guards. Callback
guards verify the expected player, active pass and native target.

## Panel controls and exchanges

An already-open tax panel is retained after a review. A panel opened solely for
background work is closed afterward. Manual tax controls, including decree
selection, are locked while a pass or recovery is running. The automation
checkbox remains available. The lock is separate from the saved opt-in flag.

CK3's **Automatically assign vassals to jurisdictions** setting is independent
of this mod's checkbox. The mod can appoint collectors and allocate taxpayers
with either native setting. Before committing a pair exchange, it saves the
native automatic-assignment and pause settings, pauses the game and temporarily
turns native automatic assignment off. It restores the saved settings after
completion or recovery.

A persistent exchange journal records the participants, original jurisdictions,
collectors, decrees and control settings. Completion is checked against actual
native assignments. If changed jurisdiction conditions prevent recovery, the
journal remains blocked and the player receives a warning.

The algorithm performs direct improvements and profitable pair exchanges. It
does not solve larger cycles or rearrange taxpayers solely to create a vacancy
for an unassigned taxpayer. Pair planning supports the eight vanilla decrees
and single-player campaigns. Unknown third-party decrees are skipped. Recovery
after succession or a player-character switch is not guaranteed.

## Compatibility work

The mod replaces these native interface files:

- `gui/window_manage_tax_slots.gui`
- `gui/window_appoint_tax_collector.gui`
- `gui/window_tax_slot_assign_vassal.gui`
- `gui/window_tax_slot_vassals.gui`
- `gui/shared/dialogs.gui`

Marked additions distinguish the mod's extensions from the upstream interface.
Review them against the actual target game's files when updating for a new CK3
version. Changing load order does not merge another mod's edits to these files.
Do not broaden the owned collector-confirmation handler to unrelated dialogs.

## Validation and publication

Use disposable native CK3 campaigns with independent profiles, saves and logs.
Exercise the actual production checkbox and native commands. Relevant checks
include an open tax panel, collector vacancies, monthly scheduling, disabled
stability, profitable exchanges, cancellation, control restoration and real
save/load recovery. Bind evidence to the complete tested runtime and harness;
static checks alone do not establish native behavior.

Hidden native runs do not establish visual layout, clipping or manual pointer
interaction. Keep those checks separate. Preserve failed attempts and record
the limits of inherited evidence. Never include personal campaign saves, local
logs, machine paths or private test profiles in a public source export.

Keep the editable player description in `publishing/description.en.md` and
regenerate README/store variants from that source. Runtime changes require a
new verified candidate. Publication-only prose changes preserve the existing
runtime and its scoped evidence. Confirm all supported languages, platform
identities, archive contents and delivered bytes before claiming a publication
complete. Preserve the artwork and code attribution in the player description.
