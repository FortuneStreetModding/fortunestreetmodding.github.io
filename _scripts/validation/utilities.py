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
