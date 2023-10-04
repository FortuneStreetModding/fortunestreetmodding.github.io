from validation.autorepair import inplace_change
from validation.errors import errorMsg, fixedMsg, process_strErrors, process_strFixes

strErrors = []
strFixes = []


def compare_values(frbValue, yamlValue, attribute, autorepair, yamlMap):
    global strErrors
    global strFixes
    if frbValue != yamlValue:
        strErrors.append(errorMsg.format(frbValue, yamlValue, attribute))
        if autorepair:
            inplace_change(yamlMap, attribute, frbValue)
            strFixes.append(fixedMsg.format(frbValue, yamlValue, attribute))



def convert_galaxy_status(galaxyStatus):
    loopingMode = "unknown"
    match (galaxyStatus):
        case 0:
            loopingMode = "none"
        case 1:
            loopingMode = "both"
        case 2:
            loopingMode = "vertical"
    return loopingMode


def check_consistency(frb, yaml, autorepair, yamlMap):
    global strErrors
    global strFixes
    print(f'{" ":24} FRB/YAML Consistency Check...', end="")
    
    compare_values(frb.baseSalary, yaml["baseSalary"], "baseSalary", autorepair, yamlMap)
    compare_values(frb.initialCash, yaml["initialCash"], "initialCash", autorepair, yamlMap)
    compare_values(frb.maxDiceRoll, yaml["maxDiceRoll"], "maxDiceRoll", autorepair, yamlMap)
    compare_values(frb.salaryIncrement,yaml["salaryIncrement"],"salaryIncrement",autorepair,yamlMap)

    loopingMode = convert_galaxy_status(frb.galaxyStatus)

    if "looping" in yaml:
        compare_values(
            loopingMode,
            yaml["looping"]["mode"].lower(),
            "looping mode",
            autorepair,
            yamlMap,
        )
    else:
        compare_values(loopingMode, "none", "looping mode", autorepair, yamlMap)
    process_strErrors(strErrors)
    process_strFixes(strFixes)
