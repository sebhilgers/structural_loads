from __future__ import annotations

from abc import ABC
from numbers import Real

from structural_loads.domain.loadcase import LoadCase


class Load(ABC):
    def __init__(
        self,
        name: str,
        loadcase: LoadCase,
        value: float,
        unit: str,
    ) -> None:
        if not isinstance(loadcase, LoadCase):
            raise TypeError(
                "Load.loadcase must be a LoadCase. "
                "Pass a single load case such as LoadCase('LC1', ActionCategory.SNOW)."
            )
        if not isinstance(value, Real) or isinstance(value, bool):
            raise TypeError("Load.value must be a real number.")
        self.name = name
        self.loadcase = loadcase
        self.value = float(value)
        self.unit = unit

    @property
    def load_type(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return (
            f"{self.load_type}(name={self.name!r}, loadcase={self.loadcase.name!r}, "
            f"value={self.value!r}, unit={self.unit!r})"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "type": self.load_type,
            "name": self.name,
            "loadcase": self.loadcase.to_dict(),
            "value": self.value,
            "unit": self.unit,
        }

    def to_df(self):
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for to_df(); install with 'pip install pandas'"
            ) from exc

        row = {
            "type": self.load_type,
            "name": self.name,
            "loadcase_name": self.loadcase.name,
            "loadcase_category": self.loadcase.category.value,
            "loadcase_description": self.loadcase.description,
            "value": self.value,
            "unit": self.unit,
        }
        return pd.DataFrame([row])


class AreaLoad(Load):
    def __init__(
        self,
        name: str,
        loadcase: LoadCase,
        value: float,
        unit: str = "kN/m²",
    ) -> None:
        super().__init__(name=name, loadcase=loadcase, value=value, unit=unit)


class LineLoad(Load):
    def __init__(
        self,
        name: str,
        loadcase: LoadCase,
        value: float,
        unit: str = "kN/m",
    ) -> None:
        super().__init__(name=name, loadcase=loadcase, value=value, unit=unit)


class PointLoad(Load):
    def __init__(
        self,
        name: str,
        loadcase: LoadCase,
        value: float,
        unit: str = "kN",
    ) -> None:
        super().__init__(name=name, loadcase=loadcase, value=value, unit=unit)
