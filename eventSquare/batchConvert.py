#!/usr/bin/env python
import sys
from typing import List
MIN_PYTHON = (3, 9)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

from subprocess import check_output
from pathlib import Path
from dataclasses import dataclass

import os
import shutil
from PIL import Image
import imagehash
import hashlib
import yaml
from multiprocessing import Process

@dataclass
class ImageMinimapIcon:
    tpl   : str
    mask  : str
    resize: str
    offset: str
    dir   : str
    tile  : str
    png   : str
    orig  : str
    tmp   : str

def deleteFolderContents(folder : str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def get_digest(file_path):
    h = hashlib.sha1()

    with open(file_path, 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()

def process(lang : str):
    langDir = f'lang{lang}/'
    suffix = ""
    if lang:
        suffix = f'_{lang}'
    else:
        langDir = ''

    filePaths = list(Path().glob(f'chance_card/{langDir}*.cmpres'))
    gameBoardCmpresPath = list(Path().glob(f'game/{langDir}game_board{suffix}.cmpres'))[0]
    gameBoardArcPath = list(Path().glob(f'game/{langDir}game_board{suffix}.arc'))[0]
    gameBoardOutputDir = f'output/game/{langDir}'
    gameBoardOutput = gameBoardOutputDir + f'game{suffix}.cmpres'
    chanceCardOutputDir = f'output/chance_card/{langDir}'
    chanceCardBsdiffDir = f'output/bsdiff/chance_card/{langDir}'
    gameBoardBsdiffDir = f'output/bsdiff/game/{langDir}'
    gameBoardBsdiff = gameBoardBsdiffDir + f'game{suffix}.cmpres.bsdiff'

    if os.path.exists(chanceCardOutputDir):
        deleteFolderContents(chanceCardOutputDir)
    else:
        os.makedirs(chanceCardOutputDir)

    if os.path.exists(gameBoardOutputDir):
        deleteFolderContents(gameBoardOutputDir)
    else:
        os.makedirs(gameBoardOutputDir)

    if os.path.exists(chanceCardBsdiffDir):
        deleteFolderContents(chanceCardBsdiffDir)
    else:
        os.makedirs(chanceCardBsdiffDir)

    if os.path.exists(gameBoardBsdiffDir):
        deleteFolderContents(gameBoardBsdiffDir)
    else:
        os.makedirs(gameBoardBsdiffDir)

    imageVenturecardDir = f'output/images_venturecard/{langDir}'
    imageVenturecard = imageVenturecardDir + "ui_mark_eventsquare_{number}.png"
    imageSquareDir = f'output/images_square/{langDir}'
    imageSquare = imageSquareDir + "ui_mark_eventsquare_{number}.png"
    imageBoardOutputDir = f'output/images_board/{langDir}'
    imageBoard = imageBoardOutputDir + "ui_mark_eventsquare_{number}.png"
    imageIconOutputDir = f'output/images_icon/{langDir}'
    imageIcon = imageIconOutputDir + "ui_mark_eventsquare_{number}.png"

    if os.path.exists(imageVenturecardDir):
        deleteFolderContents(imageVenturecardDir)
    else:
        os.makedirs(imageVenturecardDir)

    if os.path.exists(imageSquareDir):
        deleteFolderContents(imageSquareDir)
    else:
        os.makedirs(imageSquareDir)

    if os.path.exists(imageBoardOutputDir):
        deleteFolderContents(imageBoardOutputDir)
    else:
        os.makedirs(imageBoardOutputDir)

    if os.path.exists(imageIconOutputDir):
        deleteFolderContents(imageIconOutputDir)
    else:
        os.makedirs(imageIconOutputDir)

    gameBoardCmpres = gameBoardCmpresPath.as_posix()
    gameBoardCmpresDecomp = f'{gameBoardCmpresPath.parent.as_posix()}/{gameBoardCmpresPath.stem}_DECOMP.bin'
    print(check_output(f'ntcompress -x {gameBoardCmpres}', encoding="utf-8"))
    print(check_output(f'wszst EXTRACT {gameBoardCmpresDecomp} --overwrite', encoding="utf-8"))
    gameBoardExtractDir = f'{gameBoardCmpresDecomp}.d'
    gameBoardTexturesDir = f'{gameBoardExtractDir}/Textures(NW4R)'

    gameBoardArc = gameBoardArcPath.as_posix()
    gameBoardArcExtractDir = f'{gameBoardArc}.d'
    print(check_output(f'wszst EXTRACT {gameBoardArc} --overwrite --dest {gameBoardArcExtractDir}', encoding="utf-8"))
    gameBoardArcImgDir = f'{gameBoardArcExtractDir}/arc/timg'

    minimapIcons : List[ImageMinimapIcon] = []
    minimapIcons.append(ImageMinimapIcon(
        tpl=f'{gameBoardArcImgDir}/ui_minimap_icon_ja.tpl',
        mask='exclamationMarkMask.png',
        resize='12x12!',
        offset='+0+132',
        dir =f'output/images_minimap_icon/{langDir}',
        tile=f'output/images_minimap_icon/{langDir}ui_minimap_icon_ja.{{number}}.png',
        png =f'output/images_minimap_icon/{langDir}ui_minimap_icon_ja.png',
        orig=f'output/images_minimap_icon/{langDir}ui_minimap_icon_ja_orig.png',
        tmp =f'output/images_minimap_icon/{langDir}ui_minimap_icon_ja_tmp.png'
    ))
    minimapIcons.append(ImageMinimapIcon(
        tpl=f'{gameBoardArcImgDir}/ui_minimap_icon_w_ja.tpl',
        mask='exclamationMarkMask_w.png',
        resize='9x12!',
        offset='+0+132',
        dir =f'output/images_minimap_icon_w/{langDir}',
        tile=f'output/images_minimap_icon_w/{langDir}ui_minimap_icon_w_ja.{{number}}.png',
        png =f'output/game_minimap/{langDir}ui_minimap_icon_w_ja.png',
        orig=f'output/images_minimap_icon_w/{langDir}ui_minimap_icon_w_ja_orig.png',
        tmp =f'output/images_minimap_icon_w/{langDir}ui_minimap_icon_w_ja_tmp.png'
    ))
    minimapIcons.append(ImageMinimapIcon(
        tpl=f'{gameBoardArcImgDir}/ui_minimap_icon2_ja.tpl',
        mask='exclamationMarkMask2.png',
        resize='10x10!',
        offset='+0+110',
        dir =f'output/images_minimap_icon2/{langDir}',
        tile=f'output/images_minimap_icon2/{langDir}ui_minimap_icon2_ja.{{number}}.png',
        png =f'output/game_minimap/{langDir}ui_minimap_icon2_ja.png',
        orig=f'output/images_minimap_icon2/{langDir}ui_minimap_icon2_ja_orig.png',
        tmp =f'output/images_minimap_icon2/{langDir}ui_minimap_icon2_ja_tmp.png'
    ))
    minimapIcons.append(ImageMinimapIcon(
        tpl=f'{gameBoardArcImgDir}/ui_minimap_icon2_w_ja.tpl',
        mask='exclamationMarkMask2_w.png',
        resize='8x10!',
        offset='+0+110',
        dir =f'output/images_minimap_icon2_w/{langDir}',
        tile=f'output/images_minimap_icon2_w/{langDir}ui_minimap_icon2_w_ja.{{number}}.png',
        png =f'output/game_minimap/{langDir}ui_minimap_icon2_w_ja.png',
        orig=f'output/images_minimap_icon2_w/{langDir}ui_minimap_icon2_w_ja_orig.png',
        tmp =f'output/images_minimap_icon2_w/{langDir}ui_minimap_icon2_w_ja_tmp.png'
    ))

    minimapIconsWhite = [34,45,47,72,83,93,123,125]

    for minimapIcon in minimapIcons:
        if os.path.exists(minimapIcon.dir):
            deleteFolderContents(minimapIcon.dir)
        else:
            os.makedirs(minimapIcon.dir)
        print(check_output(f'wimgt DECODE {minimapIcon.tpl} --overwrite --dest {minimapIcon.orig}', encoding="utf-8"))

    shutil.rmtree(gameBoardArcExtractDir)

    #filePaths = []
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
            fileBsdiff = chanceCardBsdiffDir + f'{filePath.stem}.cmpres.bsdiff'
            print(check_output(f'bsdiff {file} {fileOutput} {fileBsdiff}', encoding="utf-8"))

        # full venture card image
        shutil.copy(chanceCardPngFile, imageVenturecard.format(number=number))
        # full bright square image
        shutil.copy(chanceCardPngFile, imageSquare.format(number=number))
        print(check_output(f'magick MOGRIFY -crop 170x170+5+35 -resize 128x128 -alpha off {imageSquare.format(number=number)}', encoding="utf-8"))
        # half darkened square image for game_board.cmpres
        shutil.copy(chanceCardPngFile, imageBoard.format(number=number))
        print(check_output(f'magick MOGRIFY +level 0%,50% -crop 170x170+5+35 -resize 128x128 -alpha off {imageBoard.format(number=number)}', encoding="utf-8"))
        print(check_output(f'wimgt ENCODE {imageBoard.format(number=number)} --transform .RGB565 --overwrite --dest {gameBoardTexturesDir}/eventsquare_{number}', encoding="utf-8"))
        #print(check_output(f'wimgt ENCODE {imageBoard.format(number=number)} --transform .CMPR --overwrite --dest {gameBoardTexturesDir}/eventsquare_{number}', encoding="utf-8"))
        # rescaled icon image for ui_mark
        shutil.copy(chanceCardPngFile, imageIcon.format(number=number))
        print(check_output(f'magick MOGRIFY -crop 170x170+5+35 -resize 29x32! -alpha off {imageIcon.format(number=number)}', encoding="utf-8"))
        # icon images:
        for minimapIcon in minimapIcons:
            imageMinimapIconFile = minimapIcon.tile.format(number=number)
            shutil.copy(chanceCardPngFile, imageMinimapIconFile)
            if int(number) in minimapIconsWhite:
                print(check_output(f'magick CONVERT -size {minimapIcon.resize} canvas:white {imageMinimapIconFile}', encoding="utf-8"))
            else:
                print(check_output(f'magick MOGRIFY -crop 12x12+85+20 -resize {minimapIcon.resize} -alpha off +dither -colors 8 -depth 3 -blur 0x8 -modulate 110,130 {imageMinimapIconFile}', encoding="utf-8"))
                #print(check_output(f'magick MOGRIFY -crop 170x170+5+35 -resize {minimapIcon.resize} -alpha off +dither -colors 8 -depth 3 -blur 0x8 -modulate 110,170 {imageMinimapIconFile}', encoding="utf-8"))
            print(check_output(f'magick {imageMinimapIconFile} {minimapIcon.mask} -compose Multiply -composite {imageMinimapIconFile}', encoding="utf-8"))
       
        os.remove(chanceCardPngFile)
        shutil.rmtree(fileExtractDir)
        os.remove(fileDecomp)

    print(check_output(f'wszst CREATE {gameBoardExtractDir} --overwrite --dest {gameBoardCmpresDecomp}', encoding="utf-8"))
    print(check_output(f'ntcompress -lex {gameBoardCmpresDecomp} -o {gameBoardOutput}', encoding="utf-8"))
    print(check_output(f'bsdiff {gameBoardCmpres} {gameBoardOutput} {gameBoardBsdiff}', encoding="utf-8"))
    shutil.rmtree(gameBoardExtractDir)
    os.remove(gameBoardCmpresDecomp)

    for minimapIcon in minimapIcons:
        if os.path.exists(minimapIcon.tmp):
            os.remove(minimapIcon.tmp)
        print(check_output(f'magick MONTAGE {minimapIcon.tile.format(number="*")} -tile 5x -geometry +0+0 -background transparent {minimapIcon.tmp}', encoding="utf-8"))
        print(check_output(f'magick CONVERT -page +0+0 {minimapIcon.orig} -page {minimapIcon.offset} {minimapIcon.tmp} -background transparent -layers merge +repage {minimapIcon.png}', encoding="utf-8"))
    
    # find similar venture cards
    filePaths = list(Path().glob(imageVenturecardDir + "*.png"))
    hashToFiles = {}
    for filePath in filePaths:
        hash = imagehash.average_hash(Image.open(filePath), hash_size=20)
        if str(hash) in hashToFiles:
            hashToFiles[str(hash)].append(filePath.as_posix())
        else:
            hashToFiles[str(hash)] = [filePath.as_posix()]

    for hash in hashToFiles:
        if len(hashToFiles[hash]) > 1:
            print("Hash: {0}".format(hash))
            for file in hashToFiles[hash]:
                print("      {0}".format(file))


def main(argv : list):
    if not os.path.exists('output'):
        os.mkdir('output')

    with open('output/sha1.yaml', 'w', encoding = "utf-8") as yaml_file:
        fileToSha1 = {}
        lang = ""
        for lang in ["", "DE", "EN", "ES", "FR", "IT", "UK"]:
            langDir = f'lang{lang}/'
            suffix = ""
            if lang:
                suffix = f'_{lang}'
            else:
                langDir = ''
            filePaths = list(Path().glob(f'chance_card/{langDir}*.cmpres'))
            gameBoardCmpresPath = list(Path().glob(f'game/{langDir}game_board{suffix}.cmpres'))[0]
            fileToSha1[gameBoardCmpresPath.as_posix()] = get_digest(gameBoardCmpresPath.as_posix())
            for filePath in filePaths:
                file = filePath.as_posix()
                fileToSha1[file] = get_digest(file)
        dump = yaml.dump(fileToSha1, default_flow_style = False, allow_unicode = True, encoding = None)
        yaml_file.write( dump )

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