from termcolor import colored, cprint

errorCount = 0
fixedCount = 0
allErrors = []
allFixes = []

errorMsg = f'The value of {colored("{attribute}", "blue")} is {colored("{yamlValue}", "yellow")} in the yaml file but {colored("{frbValue}", "yellow")} in the frb file.'
fixedMsg = f'{colored("Auto-Repair", "green")}: The value of {colored("{attribute}", "blue")} in the yaml file had been corrected to {colored("{frbValue}", "yellow")}.'

def process_strErrors(strErrors):
    # Ensure we're working with the global values.
    global errorCount
    global allErrors

    if len(strErrors) > 0:
        # Print a ERROR in red, followed by the errors themselves.
        cprint("ERROR:", "red")
        print("\n".join(strErrors))

        # Add the strErrors to the allErrors list, as well as the error count.
        errorCount += len(strErrors)
        allErrors += strErrors
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

def get_all_errors():
    global allErrors
    return allErrors

def get_all_fixes():
    global allFixes
    return allFixes