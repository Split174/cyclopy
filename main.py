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
            self.function[node.name] = func_vis.metrics
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)




with open("test.py", "r") as file:
    source = file.read()

root = ast.parse(source)
visitor = GeneralVisitor()
visitor.visit(root)
print(visitor.metrics)
print(visitor.function)
