from validation.frb import SquareType
from validation.errors import process_strErrors, get_doors_and_dice_error_message

doors=[
    SquareType.OneWayAlleyDoorA,
    SquareType.OneWayAlleyDoorB,
    SquareType.OneWayAlleyDoorC,
    SquareType.OneWayAlleyDoorD,
    #SquareType.OneWayAlleySquare
]


def check_doors(frb, name):
    strErrors = []
    print(f'{" ":24} Door and Dice Check..........', end="")
    if frb.board_info.max_dice_roll != 9:
        process_strErrors(strErrors)
        return
    
    for s in frb._board_data.squares:
        if s.square_type in doors:
            strErrors.append(get_doors_and_dice_error_message(name))
    process_strErrors(strErrors)
    strErrors.clear()