from typing import Dict

from SqlFile import SqlFile
from UUIDGen import UUIDGen
from SqlReplacer import SqlReplacer
from os import listdir, remove
from os.path import isfile, join, isdir
import shutil

root_folder = r"C:\Users\MaX\Desktop\replaced_ids"
backup_folder = "all"


def copytree(src, dst, symlinks=False, ignore=None):
    for item in listdir(src):
        s = join(src, item)
        d = join(dst, item)
        if isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def reset():
    files_and_dirs = listdir(root_folder)
    files = [f for f in files_and_dirs if isfile(join(root_folder, f))]

    for file in files:
        remove(join(root_folder, file))

    from_dir = join(root_folder, backup_folder)
    copytree(from_dir, root_folder)

    print("folder reset!")


def get_query():
    return [
        [
            SqlFile("asset.sql", root_folder),
            SqlFile("company.sql", root_folder),
            SqlFile("language.sql", root_folder),
            SqlFile("project_folder.sql", root_folder),
            SqlFile("pvt_method.sql", root_folder),
            SqlFile("solver_group.sql", root_folder),
            SqlFile("unisum_category.sql", root_folder),
            SqlFile("unisum_unit.sql", root_folder, {
                1: 'unisum_category.sql'
            }),
            SqlFile("unisum_unit_system.sql", root_folder),
        ],
        [
            SqlFile("parameter.sql", root_folder, {
                3: "unisum_unit.sql"
            }),
            SqlFile("parameter2.sql", root_folder, {
                3: "unisum_unit.sql",
                7: "parameter.sql",
                15: "parameter.sql",
                16: "parameter.sql"
            }),
            SqlFile("solver_model.sql", root_folder, {
                1: "solver_group.sql"
            }),
            SqlFile("unisum_group.sql", root_folder, {
                1: "unisum_category.sql"
            }),
            SqlFile("unisum_unit_locale.sql", root_folder, {
                1: "unisum_unit.sql",
                2: "language.sql"
            }),
            SqlFile("unisum_unit_possible_names.sql", root_folder, {
                2: "unisum_unit.sql"
            }),
            SqlFile("unit_in_unisum_system.sql", root_folder, {
                1: "unisum_unit_system.sql",
                2: "unisum_unit.sql"
            }),
        ],
        [
            SqlFile("dict_gauge_property.sql", root_folder, {
                5: "unisum_group.sql"
            }),
            SqlFile("unisum_group_default_unit.sql", root_folder, {
                1: "unisum_group.sql",
                2: "unisum_unit_system.sql",
                3: "unisum_unit.sql"
            }),
            SqlFile("unisum_group_unit.sql", root_folder, {
                1: "unisum_group.sql",
                2: "unisum_unit.sql"
            }),
        ]
    ]


if __name__ == '__main__':
    reset()
    gen = UUIDGen.get_lower_gen()
    rep = SqlReplacer(gen)

    file_query = get_query()
    all_files = []
    for level in file_query:
        all_files.extend(level)

    first = file_query[0]
    second = file_query[1]
    third = file_query[2]

    """
    Key: filename
    Value:
        Key: old_id
        Value: new_id
    """
    mapping: Dict[str, Dict[str, str]] = dict()

    for file in all_files:
        file_mapping = rep.replace(file, mapping)
        mapping[file.file_name] = file_mapping

        gen.increment_shift()

    param_map = mapping["parameter.sql"]
