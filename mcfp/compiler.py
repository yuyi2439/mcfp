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


def compile_and_run(filename: str):
    with open(filename, 'r', encoding='utf8') as file:
        file = file.read()
    tree = ast.parse(file)
    tree = CommandTransformer().visit(tree)
    ast.fix_missing_locations(tree)
    exec(compile(tree, filename=filename, mode="exec"))
