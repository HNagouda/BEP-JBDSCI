import json
from urllib.request import urlopen

from bep.paths import OSF_DIR

PROJECT_FILES_URL = "https://api.osf.io/v2/nodes/n8r9g/files/osfstorage/"

WANTED_PATHS = [
    "!README_OSF.pdf",
    "03_Data_Extraction_Cleaning",
    "04_Analysis/04_02_StudyFits",
]

# * ====================================================================
# * === utils
# * ====================================================================


def _list_folder(url):
    """Every entry in an OSF folder, following the API's pagination."""
    entries = []
    while url:
        with urlopen(url) as response:
            page = json.load(response)

        entries.extend(page["data"])
        url = page["links"]["next"]

    return entries


def _is_wanted(path):
    """True for a wanted path, anything inside one, and the folders leading to one."""
    return any(
        path == wanted or path.startswith(wanted + "/") or wanted.startswith(path + "/")
        for wanted in WANTED_PATHS
    )


def _download(url, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url) as response:
        target.write_bytes(response.read())


def mirror_folder(url):
    """Copy the wanted files under one OSF folder into OSF_DIR."""
    for entry in _list_folder(url):
        attributes = entry["attributes"]
        path = attributes["materialized_path"].strip("/")
        target = OSF_DIR / path

        if not _is_wanted(path):
            continue
        elif attributes["kind"] == "folder":
            mirror_folder(entry["relationships"]["files"]["links"]["related"]["href"])
        elif target.exists():
            continue
        else:
            _download(entry["links"]["download"], target)
            print(path)


if __name__ == "__main__":
    mirror_folder(PROJECT_FILES_URL)
