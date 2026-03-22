from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from structural_loads.domain.actions import ActionCategory, ActionDefinition, ActionType


@dataclass(init=False)
class LoadCase:
    """Represents a structural load case with an automatically derived action definition."""

    name: str
    action: ActionDefinition
    description: Optional[str] = None

    def __init__(
        self,
        name: str,
        category: ActionCategory,
        description: Optional[str] = None,
    ) -> None:
        if not isinstance(category, ActionCategory):
            raise TypeError(
                "LoadCase.category must be an ActionCategory. "
                "Pass a single category such as ActionCategory.SNOW."
            )
        self.name = name
        self.action = ActionDefinition(category=category)
        self.description = description

    @property
    def category(self) -> ActionCategory:
        return self.action.category

    @property
    def actiontype(self) -> ActionType:
        return self.action.type

    def __repr__(self) -> str:
        return (
            f"LoadCase(name={self.name!r}, category={self.category.value!r}, "
            f"description={self.description!r})"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
        }

    def to_df(self):
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for to_df(); install with 'pip install pandas'"
            ) from exc

        row = {
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
        }
        return pd.DataFrame([row])
    
# Predefined load cases for common use
G = LoadCase(name="Ständige Last", category=ActionCategory.PERMANENT, description="Ständige Lasten")
S = LoadCase(name="Schnee", category=ActionCategory.SNOW, description="Schneelasten")
Q_A = LoadCase(name="Nutzlast Kategorie A", category=ActionCategory.RESIDENTIAL, description="Wohnen")
Q_B = LoadCase(name="Nutzlast Kategorie B", category=ActionCategory.OFFICE, description="Büro") 
Q_C = LoadCase(name="Nutzlast Kategorie C", category=ActionCategory.VERSAMMLUNG, description="Versammlungsräume") 
Q_D = LoadCase(name="Nutzlast Kategorie D", category=ActionCategory.COMMERCIAL, description="Verkaufsflächen")
Q_E = LoadCase(name="Nutzlast Kategorie E", category=ActionCategory.LAGER, description="Lager- und Werkstattflächen")
W = LoadCase(name="Wind", category=ActionCategory.WIND, description="Windlasten")
