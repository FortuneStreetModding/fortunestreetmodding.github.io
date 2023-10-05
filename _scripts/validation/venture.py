from termcolor import colored

from validation.errors import process_strErrors
from validation.frb import SquareType
from validation.utilities import are_square_types_present


venture_45_error = (
    f'({colored("{filename}", "green")}): Venture Card 45 is active, but the board does '
    'not contain both an Arcade square and a Take-A-Break square.'
)
venture_125_error = (
    f'({colored("{filename}", "green")}): Venture Card 125 is active, but the board does '
    'not contain both an Arcade square and a Boon square.'
)


def check_venture_cards(frb, yaml, name):
    strErrors = []
    print(f'{" ":24} Venture Card Check.................', end="")
    if "ventureCards" in yaml:
        activeVentureCards = 0
        for i, ventureCard in enumerate(yaml["ventureCards"]):
            # ventureCard is either a 0 or a 1, 
            # so adding it before the loop is fine
            activeVentureCards += ventureCard
            if ventureCard == 1:  # if it is active
                # Check Venture 45
                if (i + 1) == 45:  # i is 0-based, the Venture Cards in the yaml are not.
                    if not are_square_types_present(frb, [SquareType.ArcadeSquare, SquareType.TakeABreakSquare]):
                        strErrors.append(venture_45_error.format(filename=name))

                # Check Venture 125
                if (i + 1) == 125:
                    if not are_square_types_present(frb, [SquareType.ArcadeSquare, SquareType.BoonSquare]):
                        strErrors.append(venture_125_error.format(filename=name))

        # Check Venture Count
        if activeVentureCards != 64:
            strErrors.append(f'There are {colored(str(activeVentureCards), "yellow")} venture cards activated. It should be 64.')
    
    process_strErrors(strErrors)
