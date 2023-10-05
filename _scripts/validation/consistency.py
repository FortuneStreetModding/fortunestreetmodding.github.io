from termcolor import colored

from validation.autorepair import inplace_change
from validation.errors import process_strErrors, process_strFixes
from validation.frb import LoopingMode

# Informational, Error, and Warning Messages
autorepair_success = (
    f'{colored("Auto-Repair", "green")}: The value of {colored("{attribute}", "blue")} '
    f'in the yaml file had been corrected to {colored("{frbValue}", "yellow")}.'
)

mismatch_error = (
    f'({colored("{filename}", "green")}): The value of {colored("{attribute}", "blue")} '
    f'is {colored("{yamlValue}", "yellow")} in the yaml file but {colored("{frbValue}", "yellow")} '
    'in the frb file.'
)


strErrors = []
strFixes = []


def compare_values(frbValue, yamlValue, attribute, autorepair, yamlMap, name):
    global strErrors
    global strFixes
    if not frbValue or not yamlValue: 
        return
    if frbValue != yamlValue:
        strErrors.append(mismatch_error.format(attribute=attribute, frbValue=frbValue, yamlValue=yamlValue, filename=name))
        if autorepair:
            inplace_change(yamlMap, attribute, frbValue)
            strFixes.append(autorepair_success.format(attribute=attribute, frbValue=frbValue))


def convert_galaxy_status(galaxyStatus):
    loopingMode = "unknown"
    match (galaxyStatus):
        case LoopingMode.NONE:
            loopingMode = "none"
        case LoopingMode.BOTH:
            loopingMode = "both"
        case LoopingMode.VERTICAL:
            loopingMode = "vertical"
    return loopingMode


def check_consistency(frb, yaml, autorepair, yamlMap, name):
    global strErrors
    global strFixes
    loopingMode = ""
    print(f'{" ":24} FRB/YAML Consistency Check.........', end="")

    compare_values(frb.board_info.base_salary, yaml["baseSalary"], "baseSalary", autorepair, yamlMap, name)
    compare_values(frb.board_info.initial_cash, yaml["initialCash"], "initialCash", autorepair, yamlMap, name)
    compare_values(frb.board_info.max_dice_roll, yaml["maxDiceRoll"], "maxDiceRoll", autorepair, yamlMap, name)
    compare_values(frb.board_info.salary_increment,yaml["salaryIncrement"],"salaryIncrement",autorepair,yamlMap, name)

    loopingMode = convert_galaxy_status(frb.board_info.galaxy_status)

    if "looping" in yaml:
        compare_values(loopingMode,yaml["looping"]["mode"].lower(),"looping mode",autorepair,yamlMap, name)
    else:
        compare_values(loopingMode, "none", "looping mode", autorepair, yamlMap, name)
    process_strErrors(strErrors)
    process_strFixes(strFixes)
    strErrors.clear()
    strFixes.clear()
