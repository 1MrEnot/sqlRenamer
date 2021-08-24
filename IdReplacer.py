from typing import Callable, List
import os

from Common import split_string


def use_changers(rows: List[str], column_id: int, changers: List[Callable[[str], str]]) -> List[str]:
    for changer in changers:
        rows = list(map(lambda x: change_id(x, column_id, changer), rows))
    return rows


def change_id(string: str, column_index: int, changer: Callable[[str], str]) -> str:
    args = split_string(string)

    old_id = args[column_index]
    new_id = changer(old_id)

    args[column_index] = new_id

    new_string = ', '.join(args)
    return new_string + '\n'


def param_changer(old_id: str) -> str:
    changed[old_id] = True
    return parameter_type_dict[old_id]


def back_changer(old_id: str) -> str:
    changed[old_id] = True
    return str(new_parameter_type_dict[old_id])


if __name__ == '__main__':
    directory, filename = r"C:\Users\MaX\Desktop", "а.txt"
    new_filename = f"new_{filename}"

    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
        file_rows = f.readlines()

    # gen = UUIDGen.get_lower_gen(start_shift=6)
    # gen_changer = lambda x: f"'{gen.get_id(int(x))}'"

    changed = {}
    parameter_type_dict = {
        '1': "LAYER",
        '2': "WELL",
        '3': "WELL_LAYER_INTERSECTION",
        '4': "TEST_LAYER",
        '5': "TEST_WELL",
        '6': "TEST_WELL_LAYER_INTERSECTION",
        '7': "SOLVER_SETTINGS",
        '8': "INTERPOLATION_SETTINGS",
        '9': "PVT",
    }

    new_parameter_type_dict = {
        "LAYER": 1, "TEST_LAYER": 1,
        "TEST_WELL": 2,
        "WELL_LAYER_INTERSECTION": 3, "TEST_WELL_LAYER_INTERSECTION": 3,
        "SOLVER_SETTINGS": 4,
        "INTERPOLATION_SETTINGS": 5,
        "PVT": 6,
    }

    new_rows = use_changers(file_rows, 5, [param_changer, back_changer])

    with open(os.path.join(directory, new_filename), 'w', encoding='utf-8') as f:
        f.writelines(new_rows)

    print(sorted(changed.keys()))

    print(f"Done!")
