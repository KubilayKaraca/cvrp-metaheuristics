# Origin: written by Claude (AI). See ai_usage.md, Section 5.
"""Team seed calculation (Task 2b).

Rule from the project text: the random seed is the sum of the last four
digits of all team members' student IDs.

Two readings are possible, so both are supported (set "seed_mode" in team.json):
  * "last4_number" (default): take the last four digits as one 4-digit number
    and add these numbers, e.g. 20221234 -> 1234.
  * "last4_digits": add the last four digits one by one, e.g. 20221234 -> 1+2+3+4.
"""
import json
import sys
from pathlib import Path


def last_four(student_id: str) -> str:
    digits = "".join(ch for ch in str(student_id) if ch.isdigit())
    if len(digits) < 4:
        raise ValueError(f"Student ID {student_id!r} has fewer than 4 digits")
    return digits[-4:]


def team_seed(members, mode="last4_number"):
    """Return (seed, list of per-member terms)."""
    terms = []
    for m in members:
        tail = last_four(m["student_id"])
        if mode == "last4_number":
            terms.append(int(tail))
        elif mode == "last4_digits":
            terms.append(sum(int(c) for c in tail))
        else:
            raise ValueError(f"Unknown seed_mode {mode!r}")
    return sum(terms), terms


def load_team(path="team.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    team = load_team(sys.argv[1] if len(sys.argv) > 1 else "team.json")
    seed, terms = team_seed(team["members"], team.get("seed_mode", "last4_number"))
    for m, t in zip(team["members"], terms):
        print(f"{m['name']:<25} {m['student_id']:>12}  -> {t}")
    print(f"seed = {' + '.join(map(str, terms))} = {seed}")
