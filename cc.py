import ast
import os
import argparse
from typing import Dict
parser = argparse.ArgumentParser()
parser.add_argument("-s", required=True, type=str)
args = parser.parse_args()

class GeneralVisitor(ast.NodeVisitor):

    def __init__(self, filename):
        self.filename = filename
        self.function: Dict[str, int] = {}
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
        func_vis = GeneralVisitor(None)
        for child in node.body:
            func_vis.visit(child)
            func_name = f"{node.parent.name}.{node.name}" if hasattr(node, "parent") else node.name
            self.function[func_name] = func_vis.metrics
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def __repr__(self):
        res = ""
        res += f"{self.filename} - {self.metrics}"
        sort_func = dict(sorted(self.function.items(), key=lambda x: x[1]))
        for func in sort_func:
            res += f"\n\t{func} - {sort_func[func]}"
        return res

def calc_cyclomatic(source: str, filename: str):
    root = ast.parse(source)
    for node in ast.walk(root):
        for child in ast.iter_child_nodes(node):
            if isinstance(node, ast.ClassDef):
                child.parent = node
    visitor = GeneralVisitor(filename)
    visitor.visit(root)
    return visitor


def get_python_files(path):
    py_files_path = []
    for root, dirs, files in os.walk(path):
        if not files:
            continue
        for file in files:
            if file[-2:] == "py":
                py_files_path.append(os.path.join(root, file))
    return py_files_path


def calc_dir(path):
    py_files_path = get_python_files(path)
    total_complexity = 0
    for py_file in py_files_path:
        with open(py_file, "r") as file:
            source = file.read()
            visitor = calc_cyclomatic(source, py_file)
            print(visitor)
            total_complexity += visitor.metrics
    print('----------------------------')
    print(total_complexity)


def main():
    src = args.s
    calc_dir(src)


if __name__ == "__main__":
    main()

