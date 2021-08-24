from typing import Dict, List
import re
from Common import split_string

from UUIDGen import UUIDGen as IdGen
from SqlFile import SqlFile


class SqlReplacer:
    pattern = re.compile(r"INSERT INTO \"public\"\.\".*\" VALUES \((\s*.+\s*)\,*\);")

    def __init__(self, gen: IdGen, replace_index: int = 0):
        self.gen: IdGen = gen
        self.replace_index: int = replace_index

    def replace(self, sql_file: SqlFile, old_mapping: Dict[str, Dict[str, str]] = None) -> Dict[str, str]:
        if old_mapping is None:
            old_mapping = dict()

        mapping = dict()
        new_content = []

        for file_row in sql_file.content:
            fond_strings = self.pattern.findall(file_row)

            if not fond_strings:
                new_content.append(file_row)
                continue

            fond_string = fond_strings[0]
            fond_elements = split_string(fond_string)

            old_id = fond_elements[self.replace_index]
            new_id = f"'{self.gen.get_next()}'"
            mapping[old_id] = new_id

            fond_elements[self.replace_index] = new_id
            fond_elements = self._replace_foreign(fond_elements, old_mapping, sql_file.relations)

            res_str = ', '.join(fond_elements)
            new_string = file_row.replace(fond_string, res_str)
            new_content.append(new_string)

        sql_file.rewrite(new_content)

        print(f"Replaced {sql_file.file_path}")

        return mapping

    @staticmethod
    def _replace_foreign(elements: List[str], mappings: Dict[str, Dict[str, str]], file_relations: Dict[int, str]):

        for index, filename in file_relations.items():

            try:
                mapping = mappings[filename]
            except Exception:
                print(f"No map from {filename}")
                raise

            cur_val = elements[index]

            if cur_val == 'NULL':
                new_val = 'NULL'
            else:
                try:
                    new_val = mapping[cur_val]
                except Exception:
                    print(f"No id = {cur_val} in mapping from {filename}")
                    raise

            elements[index] = new_val

        return elements
