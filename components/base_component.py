from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import TEngine
    from entity import TEntity


class BaseComponent:
    entity: TEntity  # Owning entity instance.

    @property
    def engine(self) -> TEngine:
        return self.entity.gamemap.engine
