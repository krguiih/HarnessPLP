"""Benchmark observável dos dois artefatos; não simula usuários/agentes."""
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.architecture import inspect_variant
from tests.contracts import scenarios


def evaluate(variant: str) -> dict:
    entries = {}
    for name, fn in scenarios(variant).items():
        try:
            fn()
            entries[name] = {"passed": True, "error": None}
        except Exception as exc:
            entries[name] = {"passed": False, "error": f"{type(exc).__name__}: {exc}"}
    violations = inspect_variant(variant)
    return {
        "passed": sum(x["passed"] for x in entries.values()),
        "errors": sum(not x["passed"] for x in entries.values()),
        "architectural_violations": len(violations),
        "violations": violations,
        "scenarios": entries,
        "human_interventions": None,
    }


def main() -> None:
    result = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "method": "comparison of prewritten didactic implementations; not a controlled AI-agent trial",
        "human_interventions_note": "Not observed. A null does not mean zero.",
        "baseline": evaluate("baseline"),
        "harness": evaluate("harness"),
    }
    (ROOT / "results").mkdir(exist_ok=True)
    out = ROOT / "results" / "comparison.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nRelatório: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
