import argparse
import re
import os
import time

from os import walk

from models import Directory, Todos, Language
from github import Github
from typing import List, Dict


class Delator:
    def __init__(self,
                 token: str,
                 path: str,
                 ignore_files: List,
                 ignore_directories: List,
                 ):

        self.ignore_directories = ignore_directories
        self.ignore_files = ignore_files

        self.github: Github = Github(token)
        self.directory: Directory = Directory(path)
        self.todos: List[Todos] = []
        self.watched: Dict[str, List] = {}
        self.languages: Dict[str, Language] = {}
        self.files: List[Dict] = []

    def get_path(self) -> str:
        return self.directory.PATH

    def get_token(self) -> str:
        return self.github.get_token()

    def init_languages(self) -> None:
        self.languages['python'] = Language(["^(.*)TODO: .*(\n#(.*).*)*"], '.py')
        self.languages['javascript'] = Language(["^(.*)TODO: .*(\n//(.*).*)*"], '.js')
        self.languages['golang'] = Language(["^(.*)TODO: .*(\n//(.*).*)*"], '.go')

    def get_file_names(self):
        return tuple(i[1].file_name for i in self.languages.items())

    def parse_files(self, path) -> None:
        for (dirpath, dirnames, filenames) in walk(path):
            if dirnames not in self.ignore_directories:
                for file in filenames:
                    if file not in self.ignore_files:
                        if file.endswith(self.get_file_names()):
                            if file.endswith('.py'):
                                self.files.append({"path": f'{dirpath}\{file}', "language": self.languages['python']})
                            if file.endswith('.js'):
                                self.files.append(
                                    {"path": f'{dirpath}\{file}', "language": self.languages['javascript']})
                            if file.endswith('.go'):
                                self.files.append(
                                    {"path": f'{dirpath}\{file}', "language": self.languages['golang']})

    def parse_py_todos(self, string: str, regular: str) -> None:
        res = []
        raw_todos = []

        matches = re.finditer(regular[0], string, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            res.extend(match.group().split())

        for i in range(len(res)):
            if res[i].startswith('TODO'):
                todo = ''
                for j in range(i + 1, len(res)):
                    if res[j].startswith("TODO"):
                        break
                    todo = todo + " " + res[j]
                raw_todos.append(todo.split('#'))
        for i in raw_todos:
            self.todos.append(Todos(i[0], '\n'.join(i[1::])))

    def parse_js_todos(self, string: str, regular: str):
        res = []
        raw_todos = []

        matches = re.finditer(regular[0], string, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            res.extend(match.group().split())

        for i in range(len(res)):
            if res[i].startswith('TODO'):
                todo = ''
                for j in range(i + 1, len(res)):
                    if res[j].startswith("TODO"):
                        break
                    todo = todo + " " + res[j]
                raw_todos.append(todo.split('//'))
        for i in raw_todos:
            self.todos.append(Todos(i[0], '\n'.join(i[1::])))

    def parse_golang_todos(self, string: str, regular: str):
        res = []
        raw_todos = []

        matches = re.finditer(regular[0], string, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            res.extend(match.group().split())

        for i in range(len(res)):
            if res[i].startswith('TODO'):
                todo = ''
                for j in range(i + 1, len(res)):
                    if res[j].startswith("TODO"):
                        break
                    todo = todo + " " + res[j]
                raw_todos.append(todo.split('//'))
        for i in raw_todos:
            self.todos.append(Todos(i[0], '\n'.join(i[1::])))

    def collect_todos(self):
        for file in self.files:
            with open(file['path'], 'r') as f:
                if file['path']:
                    string = f.read()
                    if file['language'].file_name == '.py':
                        self.parse_py_todos(string=string, regular=file['language'].regular)
                    elif file['language'].file_name == '.js':
                        self.parse_py_todos(string=string, regular=file['language'].regular)
                    elif file['language'].file_name == '.golang':
                        self.parse_py_todos(string=string, regular=file['language'].regular)

    def push_todos(self):
        for i in self.todos:
            time.sleep(0.5)
            self.github.create_issue(data={'title': i.NAME, 'body': i.DESCRIPTION})

    def run(self):
        self.init_languages()
        self.parse_files(path=self.get_path())
        self.collect_todos()
        self.push_todos()


if __name__ == '__main__':
    directory = os.getcwd()
    parser = argparse.ArgumentParser(description='TODO finder')
    parser.add_argument("--token", required=True, type=str)
    parser.add_argument("--ignore_files", type=str)
    parser.add_argument("--ignore_directories", type=str)

    args = parser.parse_args()
    ignore_files = args.ignore_files.split(',') if args.ignore_files else []
    ignore_directories = args.ignore_directories.split(',') if args.ignore_directories else []

    delator = Delator(token=args.token,
                      path=directory,
                      ignore_directories=ignore_directories,
                      ignore_files=ignore_files
                      )
    delator.run()
