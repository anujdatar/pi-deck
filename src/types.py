from dataclasses import dataclass, field
from typing import List, Union


@dataclass
class Key:
    label: str
    description: str
    command: str
    type: str = "text"
    row: Union[int, None] = None
    column: Union[int, None] = None
    width: Union[int, None] = None
    height: Union[int, None] = None
    imgPath: Union[str, None] = None
    imgZoom: float = 1.0


@dataclass
class Keymap:
    keymap: List[Key] = field(default_factory=list)


@dataclass
class KeymapTab:
    title: str
    description: str
    packing: str
    keymap: List[Key] = field(default_factory=list)
