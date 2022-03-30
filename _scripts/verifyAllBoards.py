#!/usr/bin/env python
import sys
from typing import List
MIN_PYTHON = (3, 9)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

from subprocess import check_output
from pathlib import Path
from termcolor import cprint, colored
from datetime import datetime

import yaml
import jsonschema
import colorama
import struct

def inplace_change(file, attribute, value):
    with open(file,'r',encoding="utf8") as f:
        lines = f.readlines()
    with open(file, 'w',encoding="utf8") as f:
        for line in lines:
            if line.strip().startswith(attribute):
                f.write(f'{line.split(":", 1)[0]}: {value}\n')
            else:
                f.write(line)

def main(argv : list):
    colorama.init()
    autorepair = True

    with open("../schema/mapdescriptor.json", "r", encoding='utf8') as stream:
        yamlSchema = yaml.safe_load(stream)

    yamlMaps = list(Path().glob('../_maps/*/*.yaml'))
    for yamlMap in yamlMaps:
        name = yamlMap.parent.name
        with open(yamlMap, "r", encoding='utf8') as stream:
            try:
                print(f'{name:24} YAML Validation...', end = '')
                yamlContent = yaml.safe_load(stream)
                jsonschema.validate(yamlContent, yamlSchema)
                cprint(f'OK.', 'green')
            except yaml.YAMLError as exc:
                cprint(f'ERROR:', 'red')
                print(exc)
            except jsonschema.ValidationError as err:
                cprint(f'ERROR:', 'red')
                print(err.message)
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
            if targetAmount != yamlContent["targetAmount"]:
                strErrors.append(errorMsg.format(frbValue=targetAmount, yamlValue=yamlContent["targetAmount"], attribute="targetAmount"))
            if baseSalary != yamlContent["baseSalary"]:
                strErrors.append(errorMsg.format(frbValue=baseSalary, yamlValue=yamlContent["baseSalary"], attribute="baseSalary"))
                if autorepair:
                    inplace_change(yamlMap, "baseSalary", baseSalary)
                    strErrors.append(fixedMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
            if salaryIncrement != yamlContent["salaryIncrement"]:
                strErrors.append(errorMsg.format(frbValue=salaryIncrement, yamlValue=yamlContent["salaryIncrement"], attribute="salaryIncrement"))
                if autorepair:
                    inplace_change(yamlMap, "salaryIncrement", salaryIncrement)
                    strErrors.append(fixedMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
            if maxDiceRoll != yamlContent["maxDiceRoll"]:
                strErrors.append(errorMsg.format(frbValue=maxDiceRoll, yamlValue=yamlContent["maxDiceRoll"], attribute="maxDiceRoll"))
                if autorepair:
                    inplace_change(yamlMap, "maxDiceRoll", maxDiceRoll)
                    strErrors.append(fixedMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
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
            if len(strErrors) > 0:
                cprint(f'ERROR:', 'red')
                print("\n".join(strErrors))
            else:
                cprint(f'OK:', 'green')
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
        
            
if __name__ == "__main__":
    main(sys.argv[1:])