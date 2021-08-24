import re
import os
from os.path import join

from typing import List

uuid_re = re.compile("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


class Replacer:
    cur_id = 1
    ids = {}

    def find_ids(self, lines):
        for line in lines:
            res = uuid_re.findall(line)
            for id in res:
                self.ids[id] = self.cur_id
                self.cur_id += 1


def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        return f.readlines()


def replace_file(in_text: List[str], data) -> str:
    res = ''.join(in_text)

    for old_id, new_id in data.items():
        res = res.replace(str(old_id), str(new_id))

    return res


if __name__ == '__main__':
    folder_path = "files"

    file_text = []
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        file_path = join(folder_path, file_name)
        file_text.append(read_file(file_path))

    rep = Replacer()

    for text in file_text:
        rep.find_ids(text)

    new_file_text_list = [replace_file(text, rep.ids) for text in file_text]

    for new_file_text, file_name in zip(new_file_text_list, file_names):
        file_path = join("new", file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_file_text)

        print(file_name, "- done")
