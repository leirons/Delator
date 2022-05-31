from dataclasses import dataclass
from typing import List


@dataclass
class Todos:
    NAME: str
    DESCRIPTION: str = ''


@dataclass
class GithubToken:
    TOKEN: str


@dataclass
class Directory:
    PATH: str


@dataclass
class Language:
    regular: List[str]
    file_name: str
