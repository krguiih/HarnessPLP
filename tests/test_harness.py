import unittest
from tests.contracts import scenarios


class HarnessContracts(unittest.TestCase):
    pass


for _name, _case in scenarios("harness").items():
    setattr(HarnessContracts, f"test_{_name}", lambda self, case=_case: case())
