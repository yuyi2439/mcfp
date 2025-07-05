import ast
import inspect
import textwrap
from pathlib import Path


class CommandTransformer(ast.NodeTransformer):
    def visit_With(self, node):
        body = []
        body.append(
            ast.ImportFrom(module='mcfp', names=[ast.alias(name='Collecter')], level=0),
        )
        for n in node.body:
            if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call):
                body.append(
                    ast.Expr(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id='Collecter', ctx=ast.Load()),
                                attr='try_collect_command',
                                ctx=ast.Load(),
                            ),
                            args=[n.value],
                        )
                    )
                )
            else:
                body.append(n)

        node.body = body
        return node


def patch_save_commands(tree: ast.Module, fpath: Path) -> ast.Module:
    def _patch():
        from mcfp.collecter import Collecter

        Collecter.save_commands('{filename}')

    stmt = inspect.getsource(_patch).format(
        filename=fpath.with_suffix('.mcfunction').name
    )
    stmt = textwrap.dedent(stmt).strip()
    body = ast.parse(stmt).body[0].body  # type: ignore
    tree.body.extend(body)
    return tree


def compile_to_str(fpath: Path) -> str:
    code = fpath.read_text(encoding='utf8')
    tree = ast.parse(code)
    tree = patch_save_commands(tree, fpath)
    tree = CommandTransformer().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def compile_and_run(fpath: Path, debug: bool = False):
    code_str = compile_to_str(fpath)
    if debug:
        fpath.with_stem('_gen_' + fpath.stem).write_text(code_str, encoding='utf8')
    exec(code_str)
