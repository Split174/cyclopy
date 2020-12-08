import ast
import os
import argparse
import git
from typing import Dict, Tuple, List
from dataclasses import dataclass
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="")
parser.add_argument("-s", "--srcdir", type=str, default="")
parser.add_argument("-g", "--git", type=str, default="")
args = parser.parse_args()


@dataclass
class SourceFile:
    name: str
    function: Dict[str, int]
    total_complexity: int

    def __repr__(self):
        res = ""
        res += f"{self.name} - {self.total_complexity}"
        sort_func = dict(sorted(self.function.items(), key=lambda x: x[1], reverse=True))
        for func in sort_func:
            res += f"\n\t{func} - {sort_func[func]}"
        return res


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

    def visit_With(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_And(self, node):
        self.metrics += 1
        self.generic_visit(node)

    def visit_Or(self, node):
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

    def to_dataclass(self):
        return SourceFile(name=self.filename, function=self.function, total_complexity=self.metrics)


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


def calc_dir(path) -> Tuple[int, List[SourceFile]]:
    py_files_path = get_python_files(path)
    total_complexity = 0
    files_inform: List[SourceFile] = []
    for py_file in py_files_path:
        with open(py_file, "r") as file:
            source = file.read()
            visitor = calc_cyclomatic(source, py_file)
            files_inform.append(visitor.to_dataclass())
            total_complexity += visitor.metrics

    return total_complexity, files_inform


def main():
    file_arg = args.file
    src_arg = args.srcdir
    git_arg = args.git
    path = ""
    if file_arg == "" and src_arg == "" and git_arg == "":
        print("plz add argument -s or -g")
        return
    if file_arg != "":
        with open(file_arg, "r") as file:
            source = file.read()
            visitor = calc_cyclomatic(source, file_arg)
            print(visitor.to_dataclass())
        return
    elif src_arg != "" and os.path.isdir(src_arg):
        path = src_arg
    elif git_arg != "":
        path = "./CyclomaticComplexityTemporaryDir/"
        os.mkdir(path)
        git.Git(path).clone(git_arg)

    total, files_inform = calc_dir(path)
    files_inform = sorted(files_inform, key=lambda x: x.total_complexity,
                          reverse=True)
    for file in files_inform:
        print(file)
    print("-----------------------------")
    print("total = ", total)
    if path == "./CyclomaticComplexityTemporaryDir/":
        print(path)
        shutil.rmtree(path)


if __name__ == "__main__":
    main()