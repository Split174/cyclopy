import ast


class GeneralVisitor(ast.NodeVisitor):

    def __init__(self):
        self.function = {}
        self.metrics = 0

    def visit_IfExp(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_comprehension(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_If(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_TryExcept(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        func_vis = GeneralVisitor()
        for child in node.body:
            func_vis.visit(child)
            func_name = f"{node.parent.name}.{node.name}" if hasattr(node, "parent") else node.name
            self.function[func_name] = func_vis.metrics
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)


def calc_cyclomatic(source):
    root = ast.parse(source)
    for node in ast.walk(root):
        for child in ast.iter_child_nodes(node):
            if isinstance(node, ast.ClassDef):
                child.parent = node
    visitor = GeneralVisitor()
    visitor.visit(root)
    return visitor




visitor = calc_cyclomatic(source)
print(visitor.metrics)
print(visitor.function)
