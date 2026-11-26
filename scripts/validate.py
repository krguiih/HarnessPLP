"""Gate de qualidade sobre a versão com harness."""
import compileall
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.architecture import inspect_variant


def main() -> int:
    ok_compile = compileall.compile_dir(str(ROOT / "harness"), quiet=1)
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py", top_level_dir=str(ROOT))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    violations = inspect_variant("harness")
    if violations:
        print("Violações: " + "; ".join(violations))
    print(f"Syntax: {'OK' if ok_compile else 'FAIL'} | Tests: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} | Architecture: {len(violations)} violations")
    return 0 if ok_compile and result.wasSuccessful() and not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
