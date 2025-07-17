import ast
import inspect
import shutil
import textwrap
from pathlib import Path

import mcfp


class CommandTransformer(ast.NodeTransformer):
    def visit_With(self, node):
        body = []
        body.append(
            ast.ImportFrom(
                module='mcfp.collecter', names=[ast.alias(name='Collecter')], level=0
            ),
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


def patch_save_commands(tree: ast.Module, relative_path: Path) -> ast.Module:
    def _patch():
        from mcfp.collecter import Collecter

        Collecter.save_commands(r'{relative_path}')

    stmt = inspect.getsource(_patch).format(
        relative_path=relative_path.with_suffix('.mcfunction')
    )
    stmt = textwrap.dedent(stmt).strip()
    body = ast.parse(stmt).body[0].body  # type: ignore
    tree.body.extend(body)
    return tree


def compile2str(dir: Path, relative_path: Path) -> str:
    code = (dir / relative_path).read_text(encoding='utf8')
    tree = ast.parse(code)
    tree = patch_save_commands(tree, relative_path)
    tree = CommandTransformer().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def compile(fpath: Path, dir: Path):
    dir = Path(dir)
    code_str = compile2str(dir, fpath.relative_to(dir))
    if mcfp.DEBUG:
        fpath.with_stem('_gen_' + fpath.stem).write_text(code_str, encoding='utf8')
    exec(code_str)


def compile_all(dir: Path):
    shutil.rmtree(mcfp.TargetPath.get())
    for fpath in dir.rglob('*.py'):
        if not fpath.name.startswith('_'):
            compile(fpath, dir)
    copy_built_ins()


def copy_built_ins(target: Path | None = None):
    if target is None:
        target = mcfp.TargetPath.get()
    built_in_dir = target / 'mcfp_gen' / 'function' / 'built_ins'
    shutil.rmtree(built_in_dir, ignore_errors=True)
    shutil.copytree(
        Path(__file__).parent / '_built_in',
        built_in_dir,
        dirs_exist_ok=True,
    )
    from mcfp import DEBUG

    if not DEBUG:
        shutil.rmtree(built_in_dir / '_debug')
