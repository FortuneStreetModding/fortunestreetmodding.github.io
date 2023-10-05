from termcolor import colored
from validation.frb import SquareType
from validation.errors import process_strErrors

doors_and_dice_error = (
    f'({colored("{filename}", "green")}): The board contains '
    f'{colored("One Way Alley Door squares", "yellow")} while its Max Dice Roll is set '
    f'to {colored("9", "red")}.'
)

doors=[
    SquareType.OneWayAlleyDoorA,
    SquareType.OneWayAlleyDoorB,
    SquareType.OneWayAlleyDoorC,
    SquareType.OneWayAlleyDoorD,
    #SquareType.OneWayAlleySquare
]


def check_doors(frb, name):
    strErrors = []
    print(f'{" ":24} Doors and Dice Check...............', end="")
    if frb.board_info.max_dice_roll != 9:
        process_strErrors(strErrors)
        return
    
    for s in frb._board_data.squares:
        if s.square_type in doors:
            strErrors.append(doors_and_dice_error.format(name))
    process_strErrors(strErrors)
    strErrors.clear()