from typing import List
import ujson as json

from src import Key, KeymapTab


def keymap_json_loader() -> List[KeymapTab]:
    with open("keymap.json", "r") as keymap_file:
        json_data = json.load(keymap_file)

    tabs: List[KeymapTab] = []
    for tab_data in json_data:
        keys = [Key(**key_data) for key_data in tab_data["keymap"]]
        tabs.append(
            KeymapTab(
                title=tab_data["title"],
                description=tab_data["description"],
                keymap=keys,
            )
        )

    # tabs = [KeymapTab(**keymap_tab) for keymap_tab in json_data]
    return tabs
