#!/usr/bin/env python
import sys
from termcolor import cprint
from dataclasses import dataclass
from datetime import datetime
import requests


@dataclass
class FileMetadata:
    file_size: int
    last_modified: datetime


def get_file_metadata(url: str) -> FileMetadata:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"  # NOQA
    }
    try:
        sess = requests.session()
        size = -1
        if "drive.google.com" in url:
            headers["Accept"] = "application/json"
            fileId = url.split("id=")[1].split("&")[0]
            res = sess.get(
                f"https://www.googleapis.com/drive/v3/files/{fileId}?alt=json&fields=size,modifiedTime&key=AIzaSyDQB22BQtznFe85nOyok2U9qO5HSr3Z5u4"
            )
            data = res.json()
            if "error" in data:
                cprint("google drive error", "red")
                if "message" in data["error"]:
                    print(data["error"]["message"])
            else:
                size = int(data["size"])
                lastModifiedStr = data["modifiedTime"]
                # 2022-01-06T14:11:48.000Z
                lastModifiedDate = datetime.strptime(
                    lastModifiedStr, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                return FileMetadata(size, lastModifiedDate)
        else:
            res = sess.head(
                url, headers=headers, stream=True, verify=True, allow_redirects=True
            )
            size = int(res.headers.get("Content-Length", 0))
            lastModifiedStr = res.headers.get("Last-Modified", 0)
            # Thu, 17 Mar 2022 12:28:08 GMT
            lastModifiedDate = datetime.strptime(
                lastModifiedStr, "%a, %d %b %Y %H:%M:%S %Z"
            )
            return FileMetadata(size, lastModifiedDate)
        return None
    except IOError as e:
        print(e, file=sys.stderr)
        return
    finally:
        sess.close()
