import ast


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


def patch_save_commands(tree: ast.Module, filename: str) -> ast.Module:
    tree.body.append(
        ast.ImportFrom(
            module='mcfp.collecter', names=[ast.alias(name='Collecter')], level=0
        )
    )
    tree.body.append(
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='Collecter', ctx=ast.Load()),
                    attr='save_commands',
                    ctx=ast.Load(),
                ),
                keywords=[ast.keyword(arg='filename', value=ast.Constant(filename))],
            )
        )
    )
    return tree


def compile_and_run(fpath: str):
    with open(fpath, 'r', encoding='utf8') as file:
        code = file.read()
    tree = ast.parse(code)
    tree = patch_save_commands(tree, filename=fpath)
    tree = CommandTransformer().visit(tree)
    ast.fix_missing_locations(tree)
    exec(compile(tree, filename=fpath, mode="exec"))
