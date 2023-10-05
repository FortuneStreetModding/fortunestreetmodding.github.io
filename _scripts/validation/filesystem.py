import git
from termcolor import colored

from validation.errors import process_strErrors
from validation.utilities import get_files_in_directory, get_files_two_layers_recursively


files_incorrectly_placed_error = (
    f'({colored("File Placement Check", "red")}): Map file(s) '
    f'({colored("{filenames}", "yellow")}) were found in the root '
    f'of your branch. Please move your files to their own subdirectory '
    'inside _maps!'
)

maps_without_screenshots_error = (
    f'({colored("Screenshot Check", "red")}): Map file(s) '
    f'({colored("{filenames}", "yellow")}) do not have matching screenshots '
    f'for each board state.'
)


def get_repo_root_dir():
    # get our repo so we can grab the dir from it
    repo = git.Repo('.', search_parent_directories=True)
    return repo.working_tree_dir


def check_for_stray_maps():
    strErrors = []
    print(f'{" ":10} Stray File Check...................', end="")
    files = get_files_in_directory(get_repo_root_dir(), '.frb')
    if len(files) > 0:
        strErrors.append(files_incorrectly_placed_error.format(filenames=files))
    
    process_strErrors(strErrors)


def check_for_screenshots():
    strErrors = []
    print(f'{" ":10} FRB/Screenshot Check...............', end="")
    frbs = get_files_two_layers_recursively(f"{get_repo_root_dir()}/_maps", '.frb')
    webps = get_files_two_layers_recursively(f"{get_repo_root_dir()}/_maps", '.webp')

    frb_nosuffix = []
    webps_nosuffix = []

    for item in frbs:
        frb_nosuffix.append(item.lower()[:-4])
    
    for item in webps:
        webps_nosuffix.append(item.lower()[:-5])

    w = set(webps_nosuffix)
    frbs_with_no_screenshots = [x for x in frb_nosuffix if x not in w]
    
    if len(frbs_with_no_screenshots) > 0:
        strErrors.append(maps_without_screenshots_error.format(filenames=frbs_with_no_screenshots))
    
    process_strErrors(strErrors)