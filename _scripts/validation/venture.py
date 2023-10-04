from termcolor import colored

from validation.errors import process_strErrors


def check_venture(yaml):
    strErrors = []
    print(f'{" ":24} Venture Card Check...........', end="")
    if "ventureCards" in yaml:
        activeVentureCards = 0
        for ventureCard in yaml["ventureCards"]:
            if ventureCard == 1:
                activeVentureCards += 1
        if activeVentureCards != 64:
            strErrors.append(
                f'There are {colored(str(activeVentureCards), "yellow")} venture cards activated. It should be 64.'
            )
    process_strErrors(strErrors)
