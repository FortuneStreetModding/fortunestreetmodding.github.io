#!/usr/bin/env python
import sys

from subprocess import check_output
from pathlib import Path
from termcolor import cprint, colored
from datetime import datetime
from dataclasses import dataclass
from typing import TypedDict

import os
import yaml
import jsonschema
import colorama
import struct
import requests
import argparse
import hashlib

# https://stackoverflow.com/questions/50045617/yaml-load-force-dict-keys-to-strings
def my_construct_mapping(self, node, deep=False):
    data = self.construct_mapping_org(node, deep)
    return {(str(key) if isinstance(key, int) else key): data[key] for key in data}

yaml.SafeLoader.construct_mapping_org = yaml.SafeLoader.construct_mapping
yaml.SafeLoader.construct_mapping = my_construct_mapping

def inplace_change(file, attribute, value):
    with open(file,'r',encoding="utf8") as f:
        lines = f.readlines()
    with open(file, 'w',encoding="utf8") as f:
        for line in lines:
            if line.strip().startswith(attribute):
                f.write(f'{line.split(":", 1)[0]}: {value}\n')
            else:
                f.write(line)

def remove_lines(file):
    with open(file,'r',encoding="utf8") as f:
        lines = f.readlines()
    with open(file, 'w',encoding="utf8") as f:
        for line in lines:
            if not line.strip().startswith("---") and not line.strip().startswith("..."):
                f.write(line)

def has_lines(file):
    with open(file,'r',encoding="utf8") as f:
        lines = f.readlines()
    for line in lines:
        if line.strip().startswith("---"):
            return True
        if line.strip().startswith("..."):
            return True
    return False

@dataclass
class FileMetadata:
    file_size : int
    last_modified : datetime

@dataclass
class MusicFileMetadata:
    file_size : int
    file_hash : str
    file_path : Path
    music : str

def sha256sum(filename) -> str:
    h  = hashlib.sha256()
    b  = bytearray(8*1024*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

def get_file_metadata(url : str) -> FileMetadata:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"  # NOQA
    }
    try:
        sess = requests.session()
        size = -1
        if 'drive.google.com' in url:
            headers["Accept"] = "application/json"
            fileId = url.split("id=")[1].split("&")[0]
            res = sess.get(f'https://www.googleapis.com/drive/v3/files/{fileId}?alt=json&fields=size,modifiedTime&key=AIzaSyDQB22BQtznFe85nOyok2U9qO5HSr3Z5u4')
            data = res.json()
            if 'error' in data:
                cprint('google drive error', 'red')
                if 'message' in data['error']:
                    print(data['error']['message'])
            else:
                size = int(data["size"])
                lastModifiedStr = data["modifiedTime"]
                # 2022-01-06T14:11:48.000Z
                lastModifiedDate = datetime.strptime(lastModifiedStr, '%Y-%m-%dT%H:%M:%S.%fZ')
                return FileMetadata(size, lastModifiedDate)
        else:
            res = sess.head(url, headers=headers, stream=True, verify=True, allow_redirects=True)
            size = int(res.headers.get("Content-Length", 0))
            lastModifiedStr = res.headers.get("Last-Modified", 0)
            # Thu, 17 Mar 2022 12:28:08 GMT
            lastModifiedDate = datetime.strptime(lastModifiedStr, '%a, %d %b %Y %H:%M:%S %Z')
            return FileMetadata(size, lastModifiedDate)
        return None
    except IOError as e:
        print(e, file=sys.stderr)
        return
    finally:
        sess.close()

def file_exists_with_different_case(file_path: Path):
    for f in file_path.parent.glob("*"):
        if f.name.lower() == file_path.name.lower() and f.name != file_path.name:
            return True
    return False

bgmVolumeSensitiveHash:dict[str, MusicFileMetadata] = {}
bgmVolumeInsensitiveHash:dict[str, MusicFileMetadata] = {}
def run_music_uniqueness_validation(brstmPath: Path, rootPath: Path):
    strErrors = []

    if file_exists_with_different_case(brstmPath):
        strErrors.append(f'The music file {brstmPath.relative_to(rootPath).as_posix()} exists with a different case')
        return strErrors
    if not brstmPath.exists() or not brstmPath.is_file():
        strErrors.append(f'The music file {brstmPath.relative_to(rootPath).as_posix()} does not exist')
        return strErrors

    brstmPathWithoutVolume = Path(brstmPath.stem).with_suffix('').as_posix()
    brstmFileSize = os.path.getsize(brstmPath)
    sha256 = sha256sum(brstmPath)

    if brstmPathWithoutVolume in bgmVolumeInsensitiveHash:
        musicFileMetadata = bgmVolumeInsensitiveHash[brstmPathWithoutVolume]
        if musicFileMetadata.file_hash != sha256:
            strErrors.append(f'The music file {brstmPath.relative_to(rootPath).as_posix()} has different content from the music file {musicFileMetadata.file_path.relative_to(mapsFolder).as_posix()}')
        elif Path(brstmPath.stem).suffix != Path(musicFileMetadata.music).suffix:
            strErrors.append(f'The music file {brstmPath.relative_to(rootPath).as_posix()} has the same content as the music file {musicFileMetadata.file_path.relative_to(mapsFolder).as_posix()} but a different volume')
    else:
        bgmVolumeInsensitiveHash[brstmPathWithoutVolume] = MusicFileMetadata(brstmFileSize, sha256, brstmPath, brstmPath.stem)

    if brstmPath.stem in bgmVolumeSensitiveHash:
        musicFileMetadata = bgmVolumeSensitiveHash[brstmPath.stem]
        if musicFileMetadata.file_hash != sha256:
            strErrors.append(f'The music file {brstmPath.relative_to(rootPath).as_posix()} has different content from the music file {musicFileMetadata.file_path.relative_to(mapsFolder).as_posix()}')
    else:
        bgmVolumeSensitiveHash[brstmPath.stem] = MusicFileMetadata(brstmFileSize, sha256, brstmPath, brstmPath.stem)

    return strErrors

def main(argv : list):
    colorama.init()

    parser = argparse.ArgumentParser(description='Validate all boards.')
    parser.add_argument('--skip-autorepair', action='store_true', help='Whether the script should try to automatically repair found issues where applicable.')
    parser.add_argument('--skip-update-dates', action='store_true', help='Update the Upload-date and Last-Update-Date of maps.')
    parser.add_argument('--skip-mirror-validation', action='store_true', help='Whether the script should validate the file sizes of mirrors.')
    parser.add_argument('--skip-download-validation', action='store_true', help='Whether the script should validate the file sizes of mirrors.')
    parser.add_argument('--skip-music-uniqueness-validation', action='store_true', help='Whether the script should validate the uniqueness of music files (assumes that the files have already been downloaded).')
    args = parser.parse_args(argv)

    autorepair = not args.skip_autorepair
    update_dates = not args.skip_update_dates
    mirror_validation = not args.skip_mirror_validation
    download_validation = not args.skip_download_validation
    music_uniqueness_validation = not args.skip_music_uniqueness_validation

    with open("../public/schema/mapdescriptor.json", "r", encoding='utf8') as stream:
        yamlSchema = yaml.safe_load(stream)

    yamlMaps = list(Path().glob('../_maps/*/*.yaml'))
    errorCount = 0
    fixedCount = 0

    allErrors = {}
    for yamlMap in yamlMaps:
        myErrors = []
        name = yamlMap.parent.name
        strErrors = []
        print(f'{name:24} Naming Convention Check...', end = '')

        if ' ' in yamlMap.name:
            strErrors.append(f"There is a whitespace character in {yamlMap}")
        if ' ' in name:
            strErrors.append(f"There is a whitespace character in {name}")

        if len(strErrors) > 0:
            cprint(f'ERROR:', 'red')
            print("\n".join(strErrors))
            errorCount += len(strErrors)
            myErrors += strErrors
        else:
            cprint(f'OK', 'green')

        
        with open(yamlMap, "r", encoding='utf8') as stream:
            try:
                print(f'{"":24} YAML Validation...', end = '')
                yamlContent = yaml.safe_load(stream)
                jsonschema.validate(yamlContent, yamlSchema)
                cprint(f'OK', 'green')
            except yaml.YAMLError as exc:
                errorCount += 1
                cprint(f'ERROR:', 'red')
                myErrors.append(exc)
                print(exc)
            except jsonschema.ValidationError as err:
                errorCount += 1
                cprint(f'ERROR:', 'red')
                myErrors.append(err.message)
                print(err.message)
        
        if has_lines(yamlMap):
            errorCount += 1
            cprint(f'{name:24} ERROR:', 'red')
            errMsg = "YAML files shall no longer contain the line '---' or '...'"
            myErrors.append(errMsg)
            print(errMsg)
            if autorepair:
                remove_lines(yamlMap)
                strErrors.append(f'Removed line from {yamlMap}')

        if yamlContent:
            print(f'{" ":24} Consistency Check...', end = '')
            strErrors = []
            # check casing
            if "mapIcon" in yamlContent:
                filePath = Path(yamlMap.parent, f'{yamlContent["mapIcon"]}.png')
                if file_exists_with_different_case(filePath):
                    strErrors.append(f'The map icon file {colored(yamlContent["mapIcon"], "yellow")} exists with a different case.')
            if "frbFile1" in yamlContent:
                filePath = Path(yamlMap.parent, f'{yamlContent["frbFile1"]}.frb')
                if file_exists_with_different_case(filePath):
                    strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} exists with a different case.')
                if not filePath.exists() or not filePath.is_file():
                    strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} does not exist')
            if "frbFile2" in yamlContent:
                filePath = Path(yamlMap.parent, f'{yamlContent["frbFile2"]}.frb')
                if file_exists_with_different_case(filePath):
                    strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} exists with a different case.')
                if not filePath.exists() or not filePath.is_file():
                    strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} does not exist')
            if "frbFile3" in yamlContent:
                filePath = Path(yamlMap.parent, f'{yamlContent["frbFile3"]}.frb')
                if file_exists_with_different_case(filePath):
                    strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} exists with a different case.')
                if not filePath.exists() or not filePath.is_file():
                    strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} does not exist')
            if "frbFile4" in yamlContent:
                filePath = Path(yamlMap.parent, f'{yamlContent["frbFile4"]}.frb')
                if file_exists_with_different_case(filePath):
                    strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} exists with a different case.')
                if not filePath.exists() or not filePath.is_file():
                    strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} does not exist')
            if "frbFiles" in yamlContent:
                for frbFile in yamlContent["frbFiles"]:
                    filePath = Path(yamlMap.parent, f'{frbFile}.frb')
                    if file_exists_with_different_case(filePath):
                        strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} exists with a different case.')
                    if not filePath.exists() or not filePath.is_file():
                        strErrors.append(f'The frb file {colored(filePath.stem, "yellow")} does not exist')

            frbFile1 = yamlMap.parent / Path(f'{yamlContent["frbFiles"][0] if "frbFiles" in yamlContent else yamlContent["frbFile1"]}.frb')
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
            if initialCash != yamlContent["initialCash"]:
                strErrors.append(errorMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
                if autorepair:
                    inplace_change(yamlMap, "initialCash", initialCash)
                    strErrors.append(fixedMsg.format(frbValue=initialCash, yamlValue=yamlContent["initialCash"], attribute="initialCash"))
                    fixedCount += 1
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
                myErrors += strErrors
            else:
                cprint(f'OK', 'green')
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
                    fileMetadata = get_file_metadata(mirror)
                    if fileMetadata:
                        fileSize = fileMetadata.file_size
                        mirrorFileSizeDict[mirror] = fileSize
                        if mirror != mirrors[0] and mirrorFileSizeDict[mirrors[0]] != fileSize:
                            fileSizeError = True
                    else:
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
                myErrors += strErrors
            else:
                cprint(f'OK', 'green')
        if music_uniqueness_validation and yamlContent and "music" in yamlContent:
            strErrors = []
            print(f'{" ":24} Music Uniqueness Check...', end = '')
            for musicType in yamlContent["music"]:
                if musicType == "download":
                    continue
                music = yamlContent["music"][musicType]
                if not music:
                    continue

                if type(music) == str:
                    mapsFolder = yamlMap.parent.parent
                    musicFilePath = yamlMap.parent / Path(f'{music}.brstm')
                    run_music_uniqueness_validation(musicFilePath, mapsFolder)
                else:
                    for i in range(len(music)):
                        mapsFolder = yamlMap.parent.parent
                        musicFilePath = yamlMap.parent / Path(f'{music[i]}.brstm')
                        run_music_uniqueness_validation(musicFilePath, mapsFolder)

            if len(strErrors) > 0:
                cprint(f'ERROR:', 'red')
                print("\n".join(strErrors))
                errorCount += len(strErrors)
                myErrors += strErrors
            else:
                cprint(f'OK', 'green')
        
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
        allErrors[yamlMap] = myErrors

    print("Board Validation complete")
    if errorCount == 0:
        cprint(f'No issues found', "green")
    else:
        print(f'Found {colored(str(errorCount), "red")} issue(s):')
        print()
        for yamlMap, errors in allErrors.items():
            if len(errors) > 0:
                print(f'{yamlMap.as_posix()} - {colored(str(len(errors)), "red")} issue(s):')
                print("\n".join(errors))
                print()
        if fixedCount > 0:
            if fixedCount < errorCount:
                print(f'{colored(str(fixedCount), "green")} issue(s) auto-repaired. Remaining issue(s): {colored(str(errorCount - fixedCount), "red")}')
            else:
                cprint(f'All {str(fixedCount)} issues were auto-repaired!', 'green')
        exit(1)
        
            
if __name__ == "__main__":
    main(sys.argv[1:])
