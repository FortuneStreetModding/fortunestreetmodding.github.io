#!/usr/bin/env python
import sys

from pathlib import Path
from termcolor import cprint, colored

import yaml
import colorama
import argparse

from validation.consistency import check_consistency
from validation.doors import check_doors
from validation.errors import get_count, get_text, IssueType
from validation.filesystem import check_for_screenshots, check_for_stray_maps
from validation.frb import read
from validation.metadata import update_last_update_date
from validation.music import check_music_download, check_music_uniqueness
from validation.naming import check_naming_convention
from validation.paths import check_max_paths
from validation.venture import check_venture_cards
from validation.yaml import load_yaml, load_yaml_schema


# https://stackoverflow.com/questions/50045617/yaml-load-force-dict-keys-to-strings
def my_construct_mapping(self, node, deep=False):
    data = self.construct_mapping_org(node, deep)
    return {(str(key) if isinstance(key, int) else key): data[key] for key in data}


yaml.SafeLoader.construct_mapping_org = yaml.SafeLoader.construct_mapping
yaml.SafeLoader.construct_mapping = my_construct_mapping

# Argument Help Strings
skip_autorepair_help = (
    'Whether the script should try to automatically repair found '
    'issues where applicable.'
)

skip_update_dates_help = (
    'Whether the script should try to automatically repair found '
    'issues where applicable.'
)

skip_max_paths_help = (
    'Whether the script should calculate each board\'s Max Paths '
    'value.'
)

skip_mirror_validation_help = (
    'Whether the script should try to automatically repair found '
    'issues where applicable.'
)

skip_download_validation_help = (
    'Whether the script should try to automatically repair found '
    'issues where applicable.'
)

skip_music_uniqueness_help = (
    'Whether the script should try to automatically repair found '
    'issues where applicable.'
)


def main(argv: list):
    colorama.init()

    # Parsing Arguments
    parser = argparse.ArgumentParser(description="Validate all boards.")
    parser.add_argument("--skip-autorepair", action="store_true", help=skip_autorepair_help,)
    parser.add_argument("--skip-update-dates", action="store_true", help=skip_update_dates_help)
    parser.add_argument("--skip-max-paths-validation", action="store_true", help=skip_max_paths_help)
    parser.add_argument("--skip-mirror-validation", action="store_true", help=skip_mirror_validation_help)
    parser.add_argument("--skip-download-validation", action="store_true", help=skip_download_validation_help)
    parser.add_argument("--skip-music-uniqueness-validation", action="store_true", help=skip_music_uniqueness_help)
    args = parser.parse_args(argv)

    # Script Settings
    autorepair = not args.skip_autorepair
    update_dates = not args.skip_update_dates
    max_paths = not args.skip_max_paths_validation
    mirror_validation = not args.skip_mirror_validation
    download_validation = not args.skip_download_validation
    music_uniqueness_validation = not args.skip_music_uniqueness_validation

    # Load Schema and Map list
    yamlSchema = load_yaml_schema()
    yamlMaps = list(Path().glob("../_maps/*/*.yaml"))

    # Global/Startup/Pre-Run/Non-Board-Specific Checks
    # can go here, so we can error out before we
    # enumerate everything to save everyone time.

    print(f'--------------\n', end="")
    print(f'Startup Checks', end="")
    check_for_stray_maps()
    print(f'--------------', end="")
    check_for_screenshots()

    print("\n")

    # Board Checks
    for yamlMap in yamlMaps:
        name = yamlMap.parent.name

        check_naming_convention(name, yamlMap)
        yamlContent = load_yaml(name, yamlMap, yamlSchema)

        if not yamlContent: 
            return
        frbFile1 = yamlMap.parent / Path(f'{yamlContent["frbFiles"][0] if "frbFiles" in yamlContent else yamlContent["frbFile1"]}.frb')
        frbContent = read(frbFile1)

        check_consistency(frbContent, yamlContent, autorepair, yamlMap, name)
        check_doors(frbContent, name)
        if max_paths:
            check_max_paths(frbContent, name)
        check_venture_cards(frbContent, yamlContent, name)

        if (download_validation and "music" in yamlContent and "download" in yamlContent["music"]):
            check_music_download(mirror_validation, yamlContent)

        if music_uniqueness_validation and "music" in yamlContent:
            check_music_uniqueness(yamlMap, yamlContent)

        if update_dates:
            update_last_update_date(yamlMap)
            
        print("\n")

    print("Board Validation complete!")
    
    # Getting the final errors and counts
    allErrors = get_text(IssueType.ERRORS)
    allWarnings = get_text(IssueType.WARNINGS)
    errorCount = get_count(IssueType.ERRORS)
    fixedCount = get_count(IssueType.FIXED)
    warningCount = get_count(IssueType.WARNINGS)
    issueCount = errorCount + warningCount

    if issueCount == 0:
        cprint("No issues found", "green")
    else:
        print(f'Found {colored(str(errorCount), "red")} errors(s) and {colored(str(warningCount), "yellow")} warnings(s):')
        if errorCount > 0:
            print("---Errors---")
            print("\n".join(allErrors))
        if warningCount > 0:
            print("\n---Warnings---")
            print("\n".join(allWarnings))
        if fixedCount > 0:
            if fixedCount < issueCount:
                print(f'{colored(str(fixedCount), "green")} issue(s) auto-repaired. Remaining issue(s): {colored(str(issueCount - fixedCount), "red")}')
            else:
                cprint(f"All {str(fixedCount)} issues were auto-repaired!", "green")
        if(errorCount > 0):
            exit(1)
        else:
            exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
