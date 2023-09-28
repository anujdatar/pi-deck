from dataclasses import dataclass, field
from typing import List


@dataclass
class Key:
    label: str
    description: str
    command: str


@dataclass
class Keymap:
    keymap: List[Key] = field(default_factory=list)


@dataclass
class KeymapTab:
    title: str
    description: str
    keymap: List[Key] = field(default_factory=list)
    # keymap: Keymap
