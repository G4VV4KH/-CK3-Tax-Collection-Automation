"""Independent arithmetic oracle for recorded native income/legality matrices.

Input JSON has slots {id: capacity} and taxpayers {id: {slot: id|null,
gold: {eligible_slot_id: native_preview_decimal}, fixed: optional_bool}}.
Missing gold entries mean ineligible, never zero income. No native state is
inferred from an unrecorded preview. This checks direct/pair improvements only;
it deliberately does not label their absence a global optimum.
"""
from collections import Counter
from decimal import Decimal
import argparse
import json
from pathlib import Path


def audit(matrix):
    slots = matrix["slots"]
    taxpayers = matrix["taxpayers"]
    occupied = Counter(p["slot"] for p in taxpayers.values() if p["slot"] is not None)
    invalid = []
    for slot, count in occupied.items():
        if slot not in slots or count > slots[slot]:
            invalid.append(f"Capacity violated: {slot}={count}/{slots.get(slot)}")
    values = {}
    for payer, item in taxpayers.items():
        values[payer] = {slot: Decimal(str(gold)) for slot, gold in item["gold"].items()}
        if item["slot"] is not None and item["slot"] not in values[payer]:
            invalid.append(f"Current assignment lacks a legal native preview: {payer}->{item['slot']}")
        for slot in values[payer]:
            if slot not in slots:
                invalid.append(f"Unknown destination: {payer}->{slot}")
    if invalid:
        return {"status": "INVALID_ASSIGNMENT_OR_MATRIX", "errors": invalid, "global_optimum_verified": False}

    def current_gold(payer):
        slot = taxpayers[payer]["slot"]
        return Decimal(0) if slot is None else values[payer][slot]

    direct, pairs = [], []
    for payer, item in taxpayers.items():
        if item.get("fixed", False):
            continue
        for destination, gold in values[payer].items():
            if destination != item["slot"] and occupied[destination] < slots[destination]:
                gain = gold - current_gold(payer)
                if gain > 0:
                    direct.append({"payer": payer, "destination": destination, "gain": str(gain)})

    identifiers = sorted(taxpayers)
    for index, first in enumerate(identifiers):
        a = taxpayers[first]
        if a.get("fixed", False) or a["slot"] is None:
            continue
        for second in identifiers[index + 1:]:
            b = taxpayers[second]
            if b.get("fixed", False) or b["slot"] is None or a["slot"] == b["slot"]:
                continue
            if b["slot"] not in values[first] or a["slot"] not in values[second]:
                continue
            gain = values[first][b["slot"]] + values[second][a["slot"]] - current_gold(first) - current_gold(second)
            if gain > 0:
                pairs.append({"first": first, "second": second, "gain": str(gain)})
    return {
        "status": "IMPROVEMENT_REMAINS" if direct or pairs else "NO_DIRECT_OR_PAIR_IMPROVEMENT",
        "native_recorded_total_gold": str(sum((current_gold(p) for p in taxpayers), Decimal(0))),
        "profitable_direct_moves": direct,
        "profitable_pair_swaps": pairs,
        "global_optimum_verified": False,
        "scope": "Only supplied legal native previews and supplied capacities; three-way cycles are outside this oracle's acceptance scope.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.matrix.read_text(encoding="utf-8-sig")))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "NO_DIRECT_OR_PAIR_IMPROVEMENT" else 1)
