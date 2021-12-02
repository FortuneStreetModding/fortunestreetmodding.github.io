#!/usr/bin/env python
import sys
MIN_PYTHON = (3, 9)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

from subprocess import check_output
from pathlib import Path

import os
import json
import urllib.request
import csv
import yaml
import gdown
import shutil
from PIL import Image
import imagehash
from multiprocessing import Process

def deleteFolderContents(folder : str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def process(lang : str):
    langDir = f'lang{lang}/'
    suffix = ""
    if lang:
        suffix = f'_{lang}'
    else:
        langDir = ''

    filePaths = list(Path().glob(f'chance_card/{langDir}*.cmpres'))
    gameBoardCmpresPath = list(Path().glob(f'game_board/game_board{suffix}.cmpres'))[0]

    gameBoardOutputDir = f'output/game/{langDir}'
    gameBoardOutput = gameBoardOutputDir + f'game_board{suffix}.cmpres'
    imageOutputDir = f'output/images/{langDir}'
    imageOutput = imageOutputDir + "ui_mark_eventsquare_{number}.png"
    chanceCardOutputDir = f'output/chance_card/{langDir}'

    if os.path.exists(imageOutputDir):
        deleteFolderContents(imageOutputDir)
    else:
        os.mkdir(imageOutputDir)

    if os.path.exists(chanceCardOutputDir):
        deleteFolderContents(chanceCardOutputDir)
    else:
        os.mkdir(chanceCardOutputDir)

    if os.path.exists(gameBoardOutputDir):
        deleteFolderContents(gameBoardOutputDir)
    else:
        os.mkdir(gameBoardOutputDir)

    gameBoardCmpres = gameBoardCmpresPath.as_posix()
    gameBoardCmpresDecomp = f'{gameBoardCmpresPath.parent.as_posix()}/{gameBoardCmpresPath.stem}_DECOMP.bin'
    print(check_output(f'ntcompress -x {gameBoardCmpres}', encoding="utf-8"))
    print(check_output(f'wszst EXTRACT {gameBoardCmpresDecomp} --overwrite', encoding="utf-8"))
    gameBoardExtractDir = f'{gameBoardCmpresDecomp}.d'
    gameBoardTexturesDir = f'{gameBoardExtractDir}/Textures(NW4R)'

    for filePath in filePaths:
        file = filePath.as_posix()
        fileDecomp = f'{filePath.parent.as_posix()}/{filePath.stem}_DECOMP.bin'
        print(check_output(f'ntcompress -x {file}', encoding="utf-8"))
        print(check_output(f'wszst EXTRACT {fileDecomp} --overwrite', encoding="utf-8"))
        fileExtractDir = f'{fileDecomp}.d'
        texturesDir = f'{fileExtractDir}/Textures(NW4R)'
        chanceCardTexturePath = list(Path().glob(f'{texturesDir}/ui_chancecard_*'))[0]
        chanceCardTextureFile = chanceCardTexturePath.as_posix()
        print(check_output(f'wimgt DECODE {chanceCardTextureFile} --overwrite', encoding="utf-8"))
        chanceCardPngFile = f'{chanceCardTextureFile}.png'
        number = Path(chanceCardPngFile).name.split('_')[2]
        chanceCardEditPngFile = f'chance_card_edits/ui_chancecard_{number}.png'
        if 'ES' in lang or 'FR' in lang or 'ES' in lang:
            if os.path.exists(f'chance_card_edits/ui_chancecard_{number}_es_fr_it.png'):
                chanceCardEditPngFile = f'chance_card_edits/ui_chancecard_{number}_es_fr_it.png'
        if os.path.exists(chanceCardEditPngFile):
            if os.path.exists(chanceCardPngFile):
                os.remove(chanceCardPngFile)
            shutil.copy(chanceCardEditPngFile, chanceCardPngFile)
            print(check_output(f'magick MOGRIFY -alpha off {chanceCardPngFile}', encoding="utf-8"))
            print(check_output(f'wimgt ENCODE {chanceCardPngFile} --transform .RGB565 --overwrite', encoding="utf-8"))
            print(check_output(f'wszst CREATE {fileExtractDir} --overwrite --dest {fileDecomp}', encoding="utf-8"))
            fileOutput = chanceCardOutputDir + f'{filePath.stem}.cmpres'
            print(check_output(f'ntcompress -lex {fileDecomp} -o {fileOutput}', encoding="utf-8"))

        print(check_output(f'magick MOGRIFY -crop 170x170+5+35 -resize 29x32 -alpha off {chanceCardPngFile}', encoding="utf-8")) # for ui_mark
        #print(check_output(f'magick MOGRIFY +level 0%,50% -crop 170x170+5+35 -resize 128x128 -alpha off {chanceCardPngFile}', encoding="utf-8"))
        #print(check_output(f'magick MOGRIFY -crop 170x170+5+35 -resize 64x64 -alpha off {chanceCardPngFile}', encoding="utf-8"))
        #print(check_output(f'magick MOGRIFY -crop 170x170+5+35 -resize 128x128 -alpha off {chanceCardPngFile}', encoding="utf-8"))

        #print(check_output(f'magick MOGRIFY -crop 170x170+5+35 -resize 10x10 -alpha off +dither -colors 8 -depth 3 {chanceCardPngFile}', encoding="utf-8"))

        #print(check_output(f'magick MOGRIFY {chanceCardPngFile} -alpha off', encoding="utf-8"))

        print(check_output(f'wimgt ENCODE {chanceCardPngFile} --transform .RGB565 --overwrite --dest {gameBoardTexturesDir}/eventsquare_{number}', encoding="utf-8"))
        #print(check_output(f'wimgt ENCODE {chanceCardPngFile} --transform .CMPR --overwrite --dest {gameBoardTexturesDir}/eventsquare_{number}', encoding="utf-8"))

        os.rename(chanceCardPngFile, imageOutput.format(number=number))
        shutil.rmtree(fileExtractDir)
        os.remove(fileDecomp)

    print(check_output(f'wszst CREATE {gameBoardExtractDir} --overwrite --dest {gameBoardCmpresDecomp}', encoding="utf-8"))
    print(check_output(f'ntcompress -lex {gameBoardCmpresDecomp} -o {gameBoardOutput}', encoding="utf-8"))
    os.remove(gameBoardCmpresDecomp)

    filePaths = list(Path().glob(imageOutputDir + "*.png"))

    hashToFiles = {}

    for filePath in filePaths:
        hash = imagehash.average_hash(Image.open(filePath), hash_size=20)
        if str(hash) in hashToFiles:
            hashToFiles[str(hash)].append(filePath.as_posix())
        else:
            hashToFiles[str(hash)] = [filePath.as_posix()]

    for hash in hashToFiles:
        if len(hashToFiles[hash]) > 1:
            print("SHA1: {0}".format(hash))
            for file in hashToFiles[hash]:
                print("      {0}".format(file))


def main(argv : list):
    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('output/images'):
        os.mkdir('output/images')
    if not os.path.exists('output/game'):
        os.mkdir('output/game')
    if not os.path.exists('output/chance_card'):
        os.mkdir('output/chance_card')

    processes = []

    lang = ""
    for lang in ["", "DE", "EN", "ES", "FR", "IT", "UK"]:
        p = Process(target=process, args=(lang,))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()


if __name__ == "__main__":
    main(sys.argv[1:])