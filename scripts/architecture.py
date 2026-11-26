"""Validação arquitetural em AST, sem dependências externas."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inspect_variant(variant: str) -> list[str]:
    path = ROOT / variant / "domain.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    violations = []
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
    for name in ("OrderPlaced", "PaymentConfirmed", "OrderShipped", "OrderState"):
        cls = classes.get(name)
        frozen = False
        if cls:
            for decorator in cls.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == "dataclass":
                    frozen = any(keyword.arg == "frozen" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in decorator.keywords)
        if not frozen:
            violations.append(f"{name}: dataclass não é frozen")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name.split('.')[0] for a in node.names] if isinstance(node, ast.Import) else [(node.module or '').split('.')[0]]
            if any(n in {"os", "subprocess", "socket", "requests", "sqlite3", "time"} for n in names):
                violations.append("Domínio importa dependência com efeitos")
        if isinstance(node, (ast.Assign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Attribute) for t in targets):
                violations.append("Domínio modifica atributos diretamente")
    return violations
