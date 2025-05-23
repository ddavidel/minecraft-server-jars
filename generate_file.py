"""
Generate a JSON file with all the versions download links.
"""

import os
import json
import requests
from time import sleep


TYPE_MAP = {
    "vanilla": {
        "filename": "vanilla_version_list.json",
        "url": "https://mcutils.com/api/server-jars/vanilla",
    },
    # "spigot": {  # No longer supported by mcutils API
    #     "filename": "spigot_version_list.json",
    #     "url": "https://mcutils.com/api/server-jars/spigot",
    # },
    "fabric": {
        "filename": "fabric_version_list.json",
        "url": "https://mcutils.com/api/server-jars/fabric",
    },
    "paper": {
        "filename": "paper_version_list.json",
        "url": "https://mcutils.com/api/server-jars/paper",
    },
    "purpur": {
        "filename": "purpur_version_list.json",
        "url": "https://mcutils.com/api/server-jars/purpur",
    },
    "forge": {
        "filename": "forge_version_list.json",
        "url": "https://mcutils.com/api/server-jars/forge",
    },
    "pufferfish": {
        "filename": "pufferfish_version_list.json",
        "url": "https://mcutils.com/api/server-jars/pufferfish",
    },
    "craftbukkit": {
        "filename": "craftbukkit_version_list.json",
        "url": "https://mcutils.com/api/server-jars/craftbukkit",
    },
    "folia": {
        "filename": "folia_version_list.json",
        "url": "https://mcutils.com/api/server-jars/folia",
    },
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

    return data_dict


for jar_type, data in TYPE_MAP.items():
    print(f"Getting {jar_type} versions... This could take a while")
    version_dict = get_versions(data["url"])
    print(f"Got {len(version_dict.keys())} {jar_type}versions")

    with open(
        os.path.join(os.getcwd(), "versions", data["filename"]), "w", encoding="utf-8"
    ) as file:
        json.dump(version_dict, file, indent=4)

    print(f"File {data['filename']} saved")
    # Sleep for 1 minute to avoid rate limiting
    sleep(60)

print("All files saved")
