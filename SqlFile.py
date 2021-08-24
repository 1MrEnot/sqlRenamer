from typing import List, Dict
from os import path


class SqlFile:

    def __init__(self, file_name: str, folder_path: str, relations: Dict[int, str] = None):
        if relations is None:
            relations = dict()

        self.file_name: str = file_name
        self.folder_path: str = folder_path
        self.relations: Dict[int, str] = relations
        self.content: List[str]

        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.readlines()

    @property
    def file_path(self):
        return path.join(self.folder_path, self.file_name)

    def rewrite(self, new_content: List[str]):
        self.content = new_content

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.writelines(self.content)
