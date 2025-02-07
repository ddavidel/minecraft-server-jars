"""
Generate a JSON file with all the versions download links.
"""

import json
import requests


TYPE_MAP = {
    "vanilla": {
        "filename": "vanilla_version_list.json",
        "url": "https://mcutils.com/api/server-jars/vanilla",
    },
    "spigot": {
        "filename": "spigot_version_list.json",
        "url": "https://mcutils.com/api/server-jars/spigot",
    },
    # "fabric": {
    #     "filename": "fabric_version_list.json",
    #     "url": "https://mcutils.com/api/server-jars/fabric",
    # },
    # "paper": {
    #     "filename": "paper_version_list.json",
    #     "url": "https://mcutils.com/api/server-jars/paper",
    # },
}


def get_versions(url: str) -> dict:
    """Request to the API and gets the versions and download links."""
    # Get the URL and request the page
    r = requests.get(url, timeout=30)
    r.raise_for_status()

    # Get the content of the page
    content = r.json()

    data_dict = {}
    for versiondict in content:
        version_json = requests.get(versiondict["url"], timeout=30).json()

        if version_json.get("downloadUrl"):
            data_dict[versiondict["version"]] = version_json["downloadUrl"]
            print(f"Got version {versiondict['version']}")

    return data_dict


for jar_type, data in TYPE_MAP.items():
    print(f"Getting {jar_type} versions... This could take a while")
    version_dict = get_versions(data["url"])
    print(f"Got {len(version_dict.keys())} {jar_type}versions")

    with open(data["filename"], "w", encoding="utf-8") as file:
        json.dump(version_dict, file, indent=4)

    print(f"File {data['filename']} saved")

print("All files saved")
