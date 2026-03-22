from __future__ import annotations

from collections.abc import Iterable, Iterator

from structural_loads.domain.actions import ActionType
from structural_loads.domain.loadcase import LoadCase
from structural_loads.domain.loads import AreaLoad, LineLoad, Load, PointLoad

_ACTION_TYPE_ORDER = {
    ActionType.PERMANENT: 0,
    ActionType.VARIABLE: 1,
    ActionType.ACCIDENTAL: 2,
}

_DF_COLUMNS = [
    "type",
    "name",
    "loadcase_name",
    "loadcase_category",
    "loadcase_description",
    "action_type",
    "action_description",
    "value",
    "unit",
]


class LoadCollection:
    """Container for concrete loads with explicit sorting helpers."""

    def __init__(self, name: str, loads: Iterable[Load] | None = None) -> None:
        self.name = name
        self._loads: list[Load] = []
        if loads is None:
            return
        for load in loads:
            self.add_load(load)

    def __iter__(self) -> Iterator[Load]:
        return iter(self._loads)

    def __len__(self) -> int:
        return len(self._loads)

    def __repr__(self) -> str:
        return f"LoadCollection(name={self.name!r}, load_count={len(self._loads)})"

    @property
    def loads(self) -> list[Load]:
        return list(self._loads)

    def add_load(self, load: Load) -> Load:
        if not isinstance(load, Load):
            raise TypeError(
                "LoadCollection.add_load expects a concrete Load instance."
            )
        self._loads.append(load)
        return load

    def add_areaload(
        self,
        name: str,
        loadcase: LoadCase,
        value: float,
        unit: str = "kN/m²",
    ) -> AreaLoad:
        load = AreaLoad(name=name, loadcase=loadcase, value=value, unit=unit)
        self._loads.append(load)
        return load

    def add_lineload(
        self,
        name: str,
        loadcase: LoadCase,
        value: float,
        unit: str = "kN/m",
    ) -> LineLoad:
        load = LineLoad(name=name, loadcase=loadcase, value=value, unit=unit)
        self._loads.append(load)
        return load

    def add_pointload(
        self,
        name: str,
        loadcase: LoadCase,
        value: float,
        unit: str = "kN",
    ) -> PointLoad:
        load = PointLoad(name=name, loadcase=loadcase, value=value, unit=unit)
        self._loads.append(load)
        return load

    def sort_by_loadcase(self) -> None:
        self._loads.sort(key=self._loadcase_sort_key)

    def sort_by_action_definition(self) -> None:
        self._loads.sort(key=self._action_definition_sort_key)

    def to_df(self):
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for to_df(); install with 'pip install pandas'"
            ) from exc

        rows = [
            self._load_to_row(load)
            for load in sorted(self._loads, key=self._loadcase_sort_key)
        ]
        return pd.DataFrame(rows, columns=_DF_COLUMNS)

    @staticmethod
    def _loadcase_sort_key(load: Load) -> tuple[int, str, str, str, str, str]:
        return (
            _ACTION_TYPE_ORDER[load.loadcase.actiontype],
            load.loadcase.name,
            load.loadcase.category.value,
            load.loadcase.description or "",
            load.load_type,
            load.name,
        )

    @staticmethod
    def _action_definition_sort_key(load: Load) -> tuple[int, str, str, str, str, str]:
        action = load.loadcase.action
        return (
            _ACTION_TYPE_ORDER[load.loadcase.actiontype],
            action.category.value,
            action.description,
            load.loadcase.name,
            load.load_type,
            load.name,
        )

    @staticmethod
    def _load_to_row(load: Load) -> dict[str, object]:
        action = load.loadcase.action
        return {
            "type": load.load_type,
            "name": load.name,
            "loadcase_name": load.loadcase.name,
            "loadcase_category": load.loadcase.category.value,
            "loadcase_description": load.loadcase.description,
            "action_type": load.loadcase.actiontype.value,
            "action_description": action.description,
            "value": load.value,
            "unit": load.unit,
        }
