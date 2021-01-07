import ast
import os
import argparse
import git
from typing import Dict, Tuple, List
from dataclasses import dataclass
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="", help="calculate cyclomatic complexity in one file")
parser.add_argument("-s", "--srcdir", type=str, default="", help="calculate the cyclomatic complexity of the project in the local directory")
parser.add_argument("-g", "--git", type=str, default="", help="calculate the cyclomatic complexity of the project in the git project")
parser.add_argument("-l", "--limit", type=int, default=0)
args = parser.parse_args()

CLONE_PATH = "./CyclomaticComplexityTemporaryDir/"

@dataclass
class SourceFile:
    name: str
    function: Dict[str, int]
    total_complexity: int

    def __repr__(self):
        res = ""
        res += f"\n{self.name} - {self.total_complexity}"
        if not self.function:
            return res
        first_col = max([len(key) for key in self.function.keys()])
        second_col = max([len(str(value)) for value in self.function.values()])
        res += f"\n\t+" + "-" * (first_col + second_col + 3) + "+"
        for func in self.function:
            res += f"\n\t|{func:{first_col}} | {self.function[func]:{second_col}}|"
        res += f"\n\t+" + "-" * (first_col + second_col + 3) + "+"
        return res

    def __post_init__(self):
        self.name = self.name.replace(CLONE_PATH, "")


class GeneralVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.function: Dict[str, int] = {}
        self.metrics = 0
        self.min_limit = args.limit

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
            if func_vis.metrics <= self.min_limit:
                continue
            func_name = f"{node.parent.name}.{node.name}" if hasattr(node, "parent") else node.name
            self.function[func_name] = func_vis.metrics
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def to_dataclass(self):
        functions = dict(sorted(self.function.items(), key=lambda x: x[1],
                          reverse=True))
        return SourceFile(name=self.filename,
                          function=functions,
                          total_complexity=self.metrics)


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
            if visitor.metrics > args.limit:
                files_inform.append(visitor.to_dataclass())
            total_complexity += visitor.metrics

    return total_complexity, files_inform


def main():
    file_arg = args.file
    src_arg = args.srcdir
    git_arg = args.git
    path = ""
    if file_arg == "" and src_arg == "" and git_arg == "":
        print("plz add argument -s or -g or -f")
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
        path = CLONE_PATH
        os.mkdir(path)
        git.Git(path).clone(git_arg)

    total, files_inform = calc_dir(path)
    files_inform = sorted(files_inform, key=lambda x: x.total_complexity, reverse=True)
    print("total = ", total)
    print("-----------------------------")
    for file in files_inform:
        print(file)
    if path == CLONE_PATH:
        print(path)
        shutil.rmtree(path)