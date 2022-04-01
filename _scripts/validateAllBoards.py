#!/usr/bin/env python
import sys

from subprocess import check_output
from pathlib import Path
from termcolor import cprint, colored
from datetime import datetime

import yaml
import jsonschema
import colorama
import struct
import requests
import argparse


def inplace_change(file, attribute, value):
    with open(file,'r',encoding="utf8") as f:
        lines = f.readlines()
    with open(file, 'w',encoding="utf8") as f:
        for line in lines:
            if line.strip().startswith(attribute):
                f.write(f'{line.split(":", 1)[0]}: {value}\n')
            else:
                f.write(line)

def get_filesize(url : str):   
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"  # NOQA
    }
    try:
        sess = requests.session()
        size = -1
        if 'drive.google.com' in url:
            headers["Accept"] = "application/json"
            fileId = url.split("id=")[1].split("&")[0]
            res = sess.get(f'https://www.googleapis.com/drive/v3/files/{fileId}?alt=json&fields=size&key=AIzaSyDQB22BQtznFe85nOyok2U9qO5HSr3Z5u4')
            data = res.json()
            if 'error' in data:
                cprint('google drive error', 'red')
                if 'message' in data['error']:
                    print(data['error']['message'])
            else:
                size = int(data["size"])
        else:
            res = sess.head(url, headers=headers, stream=True, verify=True, allow_redirects=True)
            size = int(res.headers.get("Content-Length", 0))
        return size
    except IOError as e:
        print(e, file=sys.stderr)
        return
    finally:
        sess.close()

def main(argv : list):
    colorama.init()

    parser = argparse.ArgumentParser(description='Validate all boards.')
    parser.add_argument('--skip-autorepair', action='store_true', help='Whether the script should try to automatically repair found issues where applicable.')
    parser.add_argument('--skip-update-dates', action='store_true', help='Update the Upload-date and Last-Update-Date of maps.')
    parser.add_argument('--skip-mirror-validation', action='store_true', help='Whether the script should validate the file sizes of mirrors.')
    parser.add_argument('--skip-download-validation', action='store_true', help='Whether the script should validate the file sizes of mirrors.')
    args = parser.parse_args(argv)

    autorepair = not args.skip_autorepair
    update_dates = not args.skip_update_dates
    mirror_validation = not args.skip_mirror_validation
    download_validation = not args.skip_download_validation

    with open("../schema/mapdescriptor.json", "r", encoding='utf8') as stream:
        yamlSchema = yaml.safe_load(stream)

    yamlMaps = list(Path().glob('../_maps/*/*.yaml'))
    errorCount = 0
    fixedCount = 0
    for yamlMap in yamlMaps:
        name = yamlMap.parent.name
        with open(yamlMap, "r", encoding='utf8') as stream:
            try:
                print(f'{name:24} YAML Validation...', end = '')
                yamlContent = yaml.safe_load(stream)
                jsonschema.validate(yamlContent, yamlSchema)
                cprint(f'OK.', 'green')
            except yaml.YAMLError as exc:
                errorCount += 1
                cprint(f'ERROR:', 'red')
                print(exc)
            except jsonschema.ValidationError as err:
                errorCount += 1
                cprint(f'ERROR:', 'red')
                print(err.message)
        with open(yamlMap, "r", encoding='utf8') as stream:
            if not stream.readline().strip() == "---":
                errorCount += 1
                cprint(f'{name:24} ERROR:', 'red')
                print("YAML file first line must be ---")
        if yamlContent:
            print(f'{" ":24} Consistency Check...', end = '')
            frbFile1 = yamlMap.parent / Path(f'{yamlContent["frbFile1"]}.frb')
            with open(frbFile1, "rb") as stream:
                stream.seek(0x20)
                initialCash = struct.unpack(">H", stream.read(2))[0]
                targetAmount = struct.unpack(">H", stream.read(2))[0]
                baseSalary = struct.unpack(">H", stream.read(2))[0]
                salaryIncrement = struct.unpack(">H", stream.read(2))[0]
                maxDiceRoll = struct.unpack(">H", stream.read(2))[0]
                galaxyStatus = struct.unpack(">H", stream.read(2))[0]
                stream.seek(0x3C)
                squareCount = struct.unpack(">H", stream.read(2))[0]
            errorMsg = f'The value of {colored("{attribute}", "blue")} is {colored("{yamlValue}", "yellow")} in the yaml file but {colored("{frbValue}", "yellow")} in the frb file.'
            fixedMsg = f'{colored("Auto-Repair", "green")}: The value of {colored("{attribute}", "blue")} in the yaml file had been corrected to {colored("{frbValue}", "yellow")}.'
            strErrors = []
            if initialCash != yamlContent["initialCash"]:
                strErrors.append(errorMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
                if autorepair:
                    inplace_change(yamlMap, "initialCash", initialCash)
                    strErrors.append(fixedMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
                    fixedCount += 1
            if targetAmount != yamlContent["targetAmount"]:
                strErrors.append(errorMsg.format(frbValue=targetAmount, yamlValue=yamlContent["targetAmount"], attribute="targetAmount"))
            if baseSalary != yamlContent["baseSalary"]:
                strErrors.append(errorMsg.format(frbValue=baseSalary, yamlValue=yamlContent["baseSalary"], attribute="baseSalary"))
                if autorepair:
                    inplace_change(yamlMap, "baseSalary", baseSalary)
                    strErrors.append(fixedMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
                    fixedCount += 1
            if salaryIncrement != yamlContent["salaryIncrement"]:
                strErrors.append(errorMsg.format(frbValue=salaryIncrement, yamlValue=yamlContent["salaryIncrement"], attribute="salaryIncrement"))
                if autorepair:
                    inplace_change(yamlMap, "salaryIncrement", salaryIncrement)
                    strErrors.append(fixedMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
                    fixedCount += 1
            if maxDiceRoll != yamlContent["maxDiceRoll"]:
                strErrors.append(errorMsg.format(frbValue=maxDiceRoll, yamlValue=yamlContent["maxDiceRoll"], attribute="maxDiceRoll"))
                if autorepair:
                    inplace_change(yamlMap, "maxDiceRoll", maxDiceRoll)
                    strErrors.append(fixedMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
                    fixedCount += 1
            loopingMode = "unknown"
            if galaxyStatus == 0:
                loopingMode = "none"
            elif galaxyStatus == 1:
                loopingMode = "both"
            elif galaxyStatus == 2:
                loopingMode = "vertical"
            if "looping" in yamlContent:
                if loopingMode != yamlContent["looping"]["mode"].lower():
                    strErrors.append(errorMsg.format(frbValue=loopingMode, yamlValue=yamlContent["looping"]["mode"], attribute="looping mode"))
            else:
                if loopingMode != "none":
                    strErrors.append(errorMsg.format(frbValue=loopingMode, yamlValue="none", attribute="looping mode"))
            if "ventureCards" in yamlContent:
                activeVentureCards = 0
                for ventureCard in yamlContent["ventureCards"]:
                    if ventureCard == 1:
                        activeVentureCards+=1
                if activeVentureCards != 64:
                    strErrors.append(f'There are {colored(str(activeVentureCards), "yellow")} venture cards activated. It should be 64.')
            if len(strErrors) > 0:
                cprint(f'ERROR:', 'red')
                print("\n".join(strErrors))
                errorCount += len(strErrors)
            else:
                cprint(f'OK.', 'green')
        if download_validation and yamlContent and "music" in yamlContent and "download" in yamlContent["music"]:
            strErrors = []
            print(f'{" ":24} Download URL Check...', end = '')
            mirrors = []
            if type(yamlContent["music"]["download"]) == str:
                mirrors.append(yamlContent["music"]["download"])
            else:
                mirrors = yamlContent["music"]["download"]
            if not mirrors[0].startswith("https://nikkums.io/cswt/"):
                strErrors.append("The first download link must start with https://nikkums.io/cswt/")
            if len(mirrors) < 2:
                strErrors.append("There should be at least 2 music download mirrors defined for each board")
            if mirror_validation and len(mirrors) > 1:
                mirrorFileSizeDict = {}
                fileSizeError = False
                for mirror in mirrors:
                    fileSize = get_filesize(mirror)
                    mirrorFileSizeDict[mirror] = fileSize
                    if mirror != mirrors[0] and mirrorFileSizeDict[mirrors[0]] != fileSize:
                        fileSizeError = True
                if fileSizeError:
                    mirrorFileSizeDictStr = ""
                    for key,value in mirrorFileSizeDict.items():
                        mirrorFileSizeDictStr += f'{key}: {str(value)}\n'
                    strErrors.append(f'The download size of the mirrors do not match:\n{mirrorFileSizeDictStr}')
            if len(strErrors) > 0:
                cprint(f'ERROR:', 'red')
                print("\n".join(strErrors))
                errorCount += len(strErrors)
            else:
                cprint(f'OK.', 'green')

                
        if update_dates:
            # get upload date
            commitDatesOut = check_output(['git', 'log', '--follow', '--format=%aD', yamlMap.as_posix()], encoding="utf8")
            commitDatesStrList = commitDatesOut.strip().splitlines()
            uploadDate = datetime.strptime(commitDatesStrList[-1], '%a, %d %b %Y %H:%M:%S %z')

            # get last update date
            commitDatesOut = check_output(['git', 'log', '--format=%aD', yamlMap.parent.as_posix()], encoding="utf8")
            commitDatesStrList = commitDatesOut.strip().splitlines()
            lastUpdateDate = datetime.strptime(commitDatesStrList[0], '%a, %d %b %Y %H:%M:%S %z')
            
            print(f'{" ":24} Upload Date:      {uploadDate.date().isoformat()}')
            print(f'{" ":24} Last Update Date: {lastUpdateDate.date().isoformat()}')
        print()



    print("Board Validation complete")
    if errorCount == 0:
        cprint(f'No issues found', "green")
    else:
        print(f'Found {colored(str(errorCount), "red")} issue(s)')
        if fixedCount > 0:
            if fixedCount < errorCount:
                print(f'{colored(str(fixedCount), "green")} issue(s) auto-repaired. Remaining issue(s): {colored(str(errorCount - fixedCount), "red")}')
            else:
                cprint(f'All {str(fixedCount)} issues were auto-repaired!', 'green')
        exit(1)
        
            
if __name__ == "__main__":
    main(sys.argv[1:])