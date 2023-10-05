from enum import Enum
from termcolor import cprint

allErrors = []
allFixes = []
allWarnings = []
errorCount = 0
fixedCount = 0
warningCount = 0


def process_strErrors(strErrors):
    global errorCount
    global allErrors

    if len(strErrors) > 0:
        cprint("ERROR", "red")
        #print("\n".join(strErrors)) # uncomment this to print all the errors inline.
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


def process_strWarnings(strWarnings):
    global warningCount
    global allWarnings

    if len(strWarnings) > 0:
        cprint("WARNING", "yellow")
        #print("\n".join(strWarnings)) # uncomment this to print all the warnings inline.
        warningCount += len(strWarnings)
        allWarnings += strWarnings
    else:
        cprint("OK", "green")


class IssueType(Enum):
    ERRORS = 1
    FIXED = 2
    WARNINGS = 3


def get_count(t: IssueType):
    match(t):
        case IssueType.ERRORS:
            return errorCount
        case IssueType.FIXED:
            return fixedCount
        case IssueType.WARNINGS:
            return warningCount

      
def get_text(t: IssueType):
    match(t):
        case IssueType.ERRORS:
            return allErrors
        case IssueType.FIXED:
            return allFixes
        case IssueType.WARNINGS:
            return allWarnings
