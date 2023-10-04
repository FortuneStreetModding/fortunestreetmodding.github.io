#!/usr/bin/env python
import sys

from pathlib import Path
from termcolor import cprint, colored

import yaml
import colorama
import argparse

from validation.consistency import check_consistency
from validation.doors import check_doors
from validation.errors import get_all_errors, get_all_warnings, get_error_count, get_fixed_count, get_warning_count
from validation.frb import read
from validation.metadata import update_last_update_date
from validation.music import check_music_download, check_music_uniqueness
from validation.naming import check_naming_convention
from validation.paths import check_max_paths
from validation.venture import check_venture
from validation.yaml import load_yaml, load_yaml_schema


# https://stackoverflow.com/questions/50045617/yaml-load-force-dict-keys-to-strings
def my_construct_mapping(self, node, deep=False):
    data = self.construct_mapping_org(node, deep)
    return {(str(key) if isinstance(key, int) else key): data[key] for key in data}


yaml.SafeLoader.construct_mapping_org = yaml.SafeLoader.construct_mapping
yaml.SafeLoader.construct_mapping = my_construct_mapping


def main(argv: list):
    colorama.init()

    # Parsing Arguments
    parser = argparse.ArgumentParser(description="Validate all boards.")
    parser.add_argument("--skip-autorepair", action="store_true", help="Whether the script should try to automatically repair found issues where applicable.",)
    parser.add_argument("--skip-update-dates", action="store_true", help="Update the Upload-date and Last-Update-Date of maps.",)
    parser.add_argument("--skip-mirror-validation", action="store_true", help="Whether the script should validate the file sizes of mirrors.")
    parser.add_argument("--skip-download-validation", action="store_true", help="Whether the script should validate the file sizes of mirrors.")
    parser.add_argument("--skip-music-uniqueness-validation", action="store_true", help="Whether the script should validate the uniqueness of music files (assumes that the files have already been downloaded).")
    args = parser.parse_args(argv)

    # Script Settings
    autorepair = not args.skip_autorepair
    update_dates = not args.skip_update_dates
    mirror_validation = not args.skip_mirror_validation
    download_validation = not args.skip_download_validation
    music_uniqueness_validation = not args.skip_music_uniqueness_validation

    # Load Schema and Map list
    yamlSchema = load_yaml_schema()
    yamlMaps = list(Path().glob("../_maps/*/*.yaml"))

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
        check_max_paths(frbContent, name)
        check_venture(yamlContent)

        if (download_validation and "music" in yamlContent and "download" in yamlContent["music"]):
            check_music_download(mirror_validation, yamlContent)

        if music_uniqueness_validation and "music" in yamlContent:
            check_music_uniqueness(yamlMap, yamlContent)

        if update_dates:
            update_last_update_date(yamlMap)
            
        print("\n")

    allErrors = get_all_errors()
    allWarnings = get_all_warnings()
    errorCount = get_error_count()
    fixedCount = get_fixed_count()
    warningCount = get_warning_count()
    issueCount = errorCount + warningCount

    print("Board Validation complete!")

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
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
