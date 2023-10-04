from termcolor import colored, cprint

allErrors = []
allFixes = []
allWarnings = []
errorCount = 0
fixedCount = 0
warningCount = 0

informational_consistency_autorepaired_message = f'{colored("Auto-Repair", "green")}: The value of {colored("{attribute}", "blue")} in the yaml file had been corrected to {colored("{frbValue}", "yellow")}.'

error_consistency_message = f'In board {colored("{filename}", "green")}: The value of {colored("{attribute}", "blue")} is {colored("{yamlValue}", "yellow")} in the yaml file but {colored("{frbValue}", "yellow")} in the frb file.'
error_doors_and_dice_message = f'In board {colored("{filename}", "green")}: The board contains {colored("One Way Alley Door squares", "yellow")} while its Max Dice Roll is set to {colored("9", "red")}.'

warning_max_paths_message=f'In board {colored("{filename}", "green")}: The Max Paths value of {colored("{max_paths}", "red")} is higher than {colored("{limit}", "yellow")}.'

def process_strErrors(strErrors):
    # Ensure we're working with the global values.
    global errorCount
    global allErrors

    if len(strErrors) > 0:
        # Print a ERROR in red, followed by the errors themselves.
        cprint("ERROR", "red")
        #print("\n".join(strErrors))

        # Add the strErrors to the allErrors list, as well as the error count.
        errorCount += len(strErrors)
        allErrors += strErrors
    else:
        cprint("OK", "green")


def process_strWarnings(strWarnings):
    # Ensure we're working with the global values.
    global warningCount
    global allWarnings

    if len(strWarnings) > 0:
        # Print a WARNING in yellow, followed by the warnings themselves.
        cprint("WARNING", "yellow")
        #print("\n".join(strWarnings))

        # Add the strErrors to the allErrors list, as well as the error count.
        warningCount += len(strWarnings)
        allWarnings += strWarnings
    else:
        cprint("OK", "green")
    


def process_strFixes(strFixes):
    global allFixes
    global fixedCount
    if len(strFixes) > 0:
        fixedCount += len(strFixes)
        allFixes += strFixes


def get_error_count():
    global errorCount
    return errorCount


def get_fixed_count():
    global fixedCount
    return fixedCount

def get_warning_count():
    global warningCount
    return warningCount


def get_all_errors():
    global allErrors
    return allErrors


def get_all_fixes():
    global allFixes
    return allFixes


def get_all_warnings():
    global allWarnings
    return allWarnings


def get_consistency_error_message(attribute, frbValue, yamlValue, filename):
    return error_consistency_message.format(attribute=attribute, filename=filename, frbValue=frbValue, yamlValue=yamlValue)

def get_doors_and_dice_error_message(filename):
    return error_doors_and_dice_message.format(filename=filename)

def get_fixed_message(attribute, frbValue):
    return informational_consistency_autorepaired_message.format(attribute=attribute, frbValue=frbValue)

def get_path_warning(filename, max_paths, limit):
    return warning_max_paths_message.format(filename=filename, max_paths=max_paths, limit=limit)