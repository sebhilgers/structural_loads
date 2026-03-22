# actions.py

from __future__ import annotations

from abc import ABC
from enum import Enum
from re import S
from typing import Optional


class ActionType(str, Enum):
    # Clasification of action type 
    PERMANENT = "Ständig"  
    VARIABLE = "Veränderlich"  
    ACCIDENTAL = "Aussergewöhnlich"

class ActionCategory(str, Enum):
    # Subcategory of action type
    #SELFWEIGHT = "Eigengewicht"
    PERMANENT = "Ständige Last"
    OTHER = "Sonstige Einwirkung"
    RESIDENTIAL = "Kat. A: Wohnräume"
    OFFICE = "Kat. B: Büros"
    VERSAMMLUNG = "Kat. C: Versammlungsräume"
    COMMERCIAL = "Kat. D: Verkaufsräume"
    LAGER = "Kat. E: Lager und Werkstätten"
    FAHRZEUGVERKEHR = "Kat. F: Fahrzeuge bis 30kN"
    STAPLERVERKEHR = "Kat. G: Fahrzeuge über 30kN"
    ROOF = "Kat. H: Dächer"
    SNOW = "Schneelast"
    WIND = "Windlast"
    ANPRALL = "Anpralllast"

class DurationClass(str, Enum):  
    PERMANENT = "permanent"  
    LONG = "long"  
    MEDIUM = "medium"  
    SHORT = "short"  
    VERY_SHORT = "very_short"

_LOOKUP_ACTIONFACTORS: dict[str, dict[str, float]] = {
    ActionCategory.PERMANENT: {"psi0": 1.0, "psi1": 1.0, "psi2": 1.0, "duration": DurationClass.PERMANENT},
    ActionCategory.OTHER: {"psi0": 0.6, "psi1": 0.7, "psi2": 0.5, "duration": DurationClass.MEDIUM},
    ActionCategory.RESIDENTIAL: {"psi0": 0.7, "psi1": 0.5, "psi2": 0.3, "duration": DurationClass.MEDIUM},
    ActionCategory.OFFICE: {"psi0": 0.7, "psi1": 0.5, "psi2": 0.3, "duration": DurationClass.MEDIUM},
    ActionCategory.VERSAMMLUNG: {"psi0": 0.7, "psi1": 0.7, "psi2": 0.6, "duration": DurationClass.SHORT},
    ActionCategory.COMMERCIAL: {"psi0": 0.7, "psi1": 0.7, "psi2": 0.6, "duration": DurationClass.MEDIUM},
    ActionCategory.LAGER: {"psi0": 1.0, "psi1": 0.9, "psi2": 0.8, "duration": DurationClass.LONG},
    ActionCategory.FAHRZEUGVERKEHR: {"psi0": 0.7, "psi1": 0.7, "psi2": 0.6, "duration": DurationClass.MEDIUM},
    ActionCategory.STAPLERVERKEHR: {"psi0": 0.7, "psi1": 0.5, "psi2": 0.3, "duration": DurationClass.MEDIUM},
    ActionCategory.ROOF: {"psi0": 0.0, "psi1": 0.0, "psi2": 0.0, "duration": DurationClass.SHORT},
    ActionCategory.SNOW: {"psi0": 0.5, "psi1": 0.2, "psi2": 0.0, "duration": DurationClass.SHORT},
    ActionCategory.WIND: {"psi0": 0.6, "psi1": 0.2, "psi2": 0.0, "duration": DurationClass.SHORT},
    ActionCategory.ANPRALL: {"psi0": 1.0, "psi1": 1.0, "psi2": 1.0, "duration": DurationClass.VERY_SHORT}
}

class ActionFactors:
    def __init__(
        self,
        psi_0: Optional[float] = None,
        psi_1: Optional[float] = None,
        psi_2: Optional[float] = None,
        duration_class: Optional[DurationClass] = None,
    ) -> None:
        self.psi_0 = psi_0
        self.psi_1 = psi_1
        self.psi_2 = psi_2
        self.duration_class = duration_class

    @classmethod
    def from_category(cls, category: ActionCategory) -> "ActionFactors":
        info = _LOOKUP_ACTIONFACTORS.get(category)
        if not info:
            raise ValueError(f"No factors found for category {category}")
        return cls(
            psi_0=info.get("psi0"),
            psi_1=info.get("psi1"),
            psi_2=info.get("psi2"),
            duration_class=info.get("duration"),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "psi_0": self.psi_0,
            "psi_1": self.psi_1,
            "psi_2": self.psi_2,
            "duration_class": self.duration_class.value if self.duration_class else None,
        }

    def __repr__(self) -> str:
        return (
            f"ActionFactors(psi_0={self.psi_0}, psi_1={self.psi_1}, "
            f"psi_2={self.psi_2}, duration_class={self.duration_class!r})"
        )

class ActionDefinition:
    """
    Fachliche/normative Definition einer Einwirkungskategorie.
    Beispiele:
    - self_weight
    - dead_load_finishes
    - live_load_A_residential
    - snow_below_1000m
    - wind
    """
    def __init__(
        self,
        category: ActionCategory,
        description: str = "",
        factors: Optional[ActionFactors] = None,
        type_: Optional[ActionType] = None,
    ) -> None:
        self.category = category
        self.type = type_ or self._infer_type_from_category(category)
        self.factors = factors if factors is not None else ActionFactors.from_category(category)
        self.description = description

    @staticmethod
    def _infer_type_from_category(category: ActionCategory) -> ActionType:
        if category == ActionCategory.PERMANENT:
            return ActionType.PERMANENT
        if category in (ActionCategory.ANPRALL):
            return ActionType.ACCIDENTAL
        return ActionType.VARIABLE

    def __repr__(self) -> str:
        return (
            f"ActionDefinition(category={self.category!r}, type={self.type!r}, "
            f"factors={self.factors!r}, description={self.description!r})"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "category": self.category.value,
            "type": self.type.value,
            "description": self.description,
            "factors": self.factors.to_dict(),
        }

    def to_df(self):
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for to_df(); install with 'pip install pandas'"
            ) from exc

        row = {
            "category": self.category.value,
            "type": self.type.value,
            "description": self.description,
            **self.factors.to_dict(),
        }
        return pd.DataFrame([row])