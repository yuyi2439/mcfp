import ast


class Visitor(ast.NodeVisitor):
    def visit_Call(self, node: ast.Call):
        pass


def complile_source(tree: ast.Module) -> str:
    print(ast.dump(tree, indent=4))
    
    visitor = Visitor()
    visitor.visit(tree)

    raise Exception


def compile_file(filename: str):
    """compile_file

    Args:
        filename (str): no suffix
    """
    with open(filename + '.py', 'r', encoding='utf8') as file:
        source = file.read()

    ast_tree = ast.parse(source, filename=filename)

    mcf = complile_source(ast_tree)

    with open(filename + '.mcfunction', 'w', encoding='utf8') as file:
        file.write(mcf)

if __name__ == '__main__':

    filename = 'example/a'
    compile_file(filename)
    print(f"Compiled {filename}.py to {filename}.mcfunction")
