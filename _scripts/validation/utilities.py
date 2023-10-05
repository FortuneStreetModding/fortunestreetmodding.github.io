import os
from pathlib import Path
from validation.frb import SquareType


def are_square_types_present(frb, t: list[SquareType]) -> bool:
    types = []
    for i, square in enumerate(frb.squares):
        types.append(square.square_type)
    result = all(item in types for item in t)
    return result
    

def is_square_type_present(frb, t: SquareType) -> bool:
    result = False
    for i, square in enumerate(frb.squares):
        if square.square_type == t:
            result = True
    return result


def get_files_in_directory(path, extension):
    files = []
    for file in os.listdir(path):
        if file.endswith(extension):
            files.append(file)
    return files


def get_files_two_layers_recursively(path, extension):
    files = []

    p = Path(path)
    for file in p.glob("**/*.*"):
        if file.suffix == extension:
            files.append(file.name)

    return files


def compare_lists(list1, list2):
    list1.sort()
    list2.sort()

    if(list1==list2):
        return True
    else:
        return False