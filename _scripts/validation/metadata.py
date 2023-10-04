from datetime import datetime
from subprocess import check_output


def update_last_update_date(yamlMap):
    commitDatesOut = check_output(
        ["git", "log", "--follow", "--format=%aD", yamlMap.as_posix()], encoding="utf8"
    )
    commitDatesStrList = commitDatesOut.strip().splitlines()
    uploadDate = datetime.strptime(commitDatesStrList[-1], "%a, %d %b %Y %H:%M:%S %z")

    # get last update date
    commitDatesOut = check_output(
        ["git", "log", "--format=%aD", yamlMap.parent.as_posix()], encoding="utf8"
    )
    commitDatesStrList = commitDatesOut.strip().splitlines()
    lastUpdateDate = datetime.strptime(
        commitDatesStrList[0], "%a, %d %b %Y %H:%M:%S %z"
    )

    print(f'{" ":24} Upload Date:      {uploadDate.date().isoformat()}')
    print(f'{" ":24} Last Update Date: {lastUpdateDate.date().isoformat()}')
