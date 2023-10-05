import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from termcolor import colored

from validation.errors import process_strErrors
from validation.network import get_file_metadata


music_content_diff_error = (
    f'The music file {colored("{file_1}", "green")} has different content from the  '
    f'music file {colored("{file_2}", "green")}.'
)

music_content_volume_error = (
    f'The music file {colored("{file_1}", "green")} has the same content as the music '
    f'file {colored("{file_2}", "green")} but a different volume'
)


@dataclass
class MusicFileMetadata:
    file_size: int
    file_hash: str
    file_path: Path
    music: str


bgmVolumeSensitiveHash: dict[str, MusicFileMetadata] = {}
bgmVolumeInsensitiveHash: dict[str, MusicFileMetadata] = {}


def sha256sum(filename) -> str:
    h = hashlib.sha256()
    b = bytearray(8 * 1024 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()


def check_music_download(mirror_validation, yaml):
    strErrors = []
    print(f'{" ":24} Download URL Check.................', end="")
    mirrors = []
    if type(yaml["music"]["download"]) is str:
        mirrors.append(yaml["music"]["download"])
    else:
        mirrors = yaml["music"]["download"]
    if not mirrors[0].startswith("https://nikkums.io/cswt/"):
        strErrors.append(
            "The first download link must start with https://nikkums.io/cswt/"
        )
    if len(mirrors) < 2:
        strErrors.append(
            "There should be at least 2 music download mirrors defined for each board"
        )
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
            for key, value in mirrorFileSizeDict.items():
                mirrorFileSizeDictStr += f"{key}: {str(value)}\n"
            strErrors.append(
                f"The download size of the mirrors do not match:\n{mirrorFileSizeDictStr}"
            )
    process_strErrors(strErrors)


def check_music_uniqueness(yamlMap, yamlContent):
    strErrors = []
    print(f'{" ":24} Music Uniqueness Check.............', end="")
    for musicType in yamlContent["music"]:
        if musicType == "download":
            continue
        music = yamlContent["music"][musicType]
        if not music:
            continue
        if isinstance(music, list):
            music = music[0]

        mapsFolder = yamlMap.parent.parent

        musicFilePath = yamlMap.parent / Path(f"{music}.brstm")
        if not musicFilePath.exists() or not musicFilePath.is_file():
            strErrors.append(
                f"The music file {musicFilePath.relative_to(mapsFolder).as_posix()} does not exist"
            )
            continue

        musicWithoutVolume = Path(music).with_suffix("").as_posix()
        musicFileSize = os.path.getsize(musicFilePath)
        sha256 = sha256sum(musicFilePath)

        if musicWithoutVolume in bgmVolumeInsensitiveHash:
            musicFileMetadata = bgmVolumeInsensitiveHash[musicWithoutVolume]
            if musicFileMetadata.file_hash != sha256:
                file1=musicFilePath.relative_to(mapsFolder).as_posix()
                file2=musicFileMetadata.file_path.relative_to(mapsFolder).as_posix()
                
                strErrors.append(music_content_diff_error.format(file1=file1, file2=file2))

            elif Path(music).suffix != Path(musicFileMetadata.music).suffix:
                file1=musicFilePath.relative_to(mapsFolder).as_posix()
                file2=musicFileMetadata.file_path.relative_to(mapsFolder).as_posix()
                
                strErrors.append(music_content_volume_error.format(file1=file1, file2=file2))

        else:
            bgmVolumeInsensitiveHash[musicWithoutVolume] = MusicFileMetadata(
                musicFileSize, sha256, musicFilePath, music
            )

        if music in bgmVolumeSensitiveHash:
            musicFileMetadata = bgmVolumeSensitiveHash[music]
            if musicFileMetadata.file_hash != sha256:
                file1=musicFilePath.relative_to(mapsFolder).as_posix()
                file2=musicFileMetadata.file_path.relative_to(mapsFolder).as_posix()

                strErrors.append(music_content_diff_error.format(file1=file1, file2=file2))
        else:
            bgmVolumeSensitiveHash[music] = MusicFileMetadata(
                musicFileSize, sha256, musicFilePath, music
            )
    process_strErrors(strErrors)
