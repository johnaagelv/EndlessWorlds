""" Collection of common tags """
from __future__ import annotations
from typing import Final

IsPlayer: Final = "IsPlayer"
""" Entity is a player """

IsActor: Final = "IsActor"
""" Entity is an actor """

IsItem: Final = "IsItem"
""" Entity is an item """

IsWorld: Final = "IsWorld"
""" Entity is a world """

IsState: Final = "IsState"
"""
Entity is a state with:
- name
- value
- max
- usage
"""