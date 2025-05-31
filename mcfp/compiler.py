# compiler.py
import ast
import sys
import importlib.util
from pathlib import Path


class CommandVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.commands = []  # 存储最终生成的命令字符串
        self.command_objects = {}  # 存储变量名到命令对象的映射
        self.current_scope = []  # 当前作用域栈（用于嵌套命令）

    def visit_Assign(self, node):
        """处理赋值语句，记录命令对象"""
        # 检查赋值右侧是否是命令调用
        if isinstance(node.value, ast.Call):
            call = node.value
            if self.is_command_call(call):
                # 创建命令对象
                command_obj = self.create_command_object(call)

                # 记录变量名和对应的命令对象
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.command_objects[target.id] = command_obj

        self.generic_visit(node)

    def visit_Expr(self, node):
        """提取未被赋值的命令调用"""
        if isinstance(node.value, ast.Call):
            call = node.value
            if self.is_command_call(call):
                # 创建命令对象
                command_obj = self.create_command_object(call)

                # 获取命令字符串表示
                command_str = str(command_obj)
                self.commands.append(command_str)

        self.generic_visit(node)

    def visit_Call(self, node):
        """处理命令变量使用（在嵌套命令中）"""
        # 检查是否是在其他命令中使用变量
        if (
            isinstance(node.func, ast.Name)
            and node.func.id in self.command_objects
            and self.in_command_context()
        ):

            # 返回命令对象
            return self.command_objects[node.func.id]

        # 处理嵌套命令调用
        if self.is_command_call(node):
            return self.create_command_object(node)

        return None

    def is_command_call(self, call_node):
        """检查是否是命令调用"""
        if not isinstance(call_node, ast.Call):
            return False

        # 检查函数名是否是已知的命令类
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id in [
                "Say",
                "SetBlock",
                "Execute",
                "Function",
                "Scoreboard",
                "Command",
            ]

        return False

    def in_command_context(self):
        """检查当前是否在命令上下文中（作为其他命令的参数）"""
        return bool(self.current_scope)

    def create_command_object(self, call_node):
        """创建命令对象实例"""
        # 解析参数
        args = []
        kwargs = {}

        # 处理位置参数
        for arg in call_node.args:
            # 如果是嵌套命令调用
            if isinstance(arg, ast.Call):
                nested_cmd = self.visit_Call(arg)
                if nested_cmd:
                    args.append(nested_cmd)
                    continue

            # 处理常量
            if isinstance(arg, ast.Constant):
                args.append(arg.value)
                continue

            # 处理变量引用
            if isinstance(arg, ast.Name):
                # 如果是命令变量
                if arg.id in self.command_objects:
                    args.append(self.command_objects[arg.id])
                else:
                    # 普通变量（暂时作为字符串处理）
                    args.append(f"${{{arg.id}}}")
                continue

            # 其他类型暂时作为字符串处理
            args.append(ast.unparse(arg))

        # 处理关键字参数
        for kw in call_node.keywords:
            value = kw.value
            if isinstance(value, ast.Call):
                nested_cmd = self.visit_Call(value)
                if nested_cmd:
                    kwargs[kw.arg] = nested_cmd
                    continue

            if isinstance(value, ast.Constant):
                kwargs[kw.arg] = value.value
                continue

            if isinstance(value, ast.Name):
                if value.id in self.command_objects:
                    kwargs[kw.arg] = self.command_objects[value.id]
                else:
                    kwargs[kw.arg] = f"${{{value.id}}}"
                continue

            kwargs[kw.arg] = ast.unparse(value)

        # 动态导入命令模块
        command_module = self.import_command_module()

        # 获取命令类
        command_class = getattr(command_module, call_node.func.id)

        # 创建命令对象
        try:
            return command_class(*args, **kwargs)
        except TypeError as e:
            # 处理参数错误
            lineno = call_node.lineno
            col_offset = call_node.col_offset
            print(
                f"Error creating command at {self.filename}:{lineno}:{col_offset}: {e}"
            )
            return None

    def import_command_module(self):
        """动态导入命令模块"""
        module_name = "mcfp.command"

        # 如果模块已经导入，直接返回
        if module_name in sys.modules:
            return sys.modules[module_name]

        # 获取模块路径
        base_path = Path('mcfp')
        module_path = base_path / "command" / "__init__.py"

        if not module_path.exists():
            raise ImportError(f"Command module not found at {module_path}")

        # 动态导入模块
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        assert spec is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        loader = spec.loader
        assert loader is not None
        loader.exec_module(module)

        return module


def compile_source(tree: ast.Module, filename: str) -> str:
    visitor = CommandVisitor(filename)
    visitor.visit(tree)
    return "\n".join(visitor.commands)


def compile_file(filename: str):
    """compile_file

    Args:
        filename (str): no suffix
    """
    with open(filename + '.py', 'r', encoding='utf8') as file:
        source = file.read()

    ast_tree = ast.parse(source, filename=filename)

    # 添加 .py 后缀到文件名以正确解析路径
    full_filename = filename + '.py'
    mcf = compile_source(ast_tree, full_filename)

    with open(filename + '.mcfunction', 'w', encoding='utf8') as file:
        file.write(mcf)
