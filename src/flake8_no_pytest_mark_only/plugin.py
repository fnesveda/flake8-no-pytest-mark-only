import ast
from typing import Iterable, List, NamedTuple, Optional, Tuple, Union

Flake8Error = Tuple[int, int, str, 'Flake8NoPytestMarkOnly']


class _CodePosition(NamedTuple):
    line: int
    column: int


def _get_qualname(node: ast.AST) -> Optional[str]:
    parts: List[str] = []
    while True:
        if isinstance(node, ast.Attribute):
            parts.insert(0, node.attr)
            node = node.value
        elif isinstance(node, ast.Name):
            parts.insert(0, node.id)
            break
        else:
            return None
    return '.'.join(parts)


class _MarksVisitor(ast.NodeVisitor):
    pytest_mark_only_positions: List[_CodePosition]

    def __init__(self) -> None:
        self.pytest_mark_only_positions = []

    def _check_node(self, node: Union[ast.ClassDef, ast.AsyncFunctionDef, ast.FunctionDef]) -> None:
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                decorator = decorator.func
            if not isinstance(decorator, ast.Attribute):
                continue

            if _get_qualname(decorator) == 'pytest.mark.only':
                self.pytest_mark_only_positions.append(_CodePosition(decorator.lineno, decorator.col_offset + len('pytest.mark.')))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        self._check_node(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
        self._check_node(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        # Check decorators on the class itself
        self._check_node(node)

        # Visit all children of the class
        self.generic_visit(node)


class Flake8NoPytestMarkOnly:
    """Flake8 plugin to check for `@pytest.mark.only` decorators."""

    def __init__(self, tree: ast.AST) -> None:
        """Initialize the plugin."""
        self._tree: ast.AST = tree

    def run(self) -> Iterable[Flake8Error]:
        """Run the plugin."""
        visitor = _MarksVisitor()
        visitor.visit(self._tree)

        for position in visitor.pytest_mark_only_positions:
            yield (
                position.line,
                position.column,
                'PNO001 do not commit @pytest.mark.only',
                self,
            )
