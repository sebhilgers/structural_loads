from __future__ import annotations

from structural_loads.domain.actions import ActionType
from structural_loads.domain.loads import Load


class Slab:
    """Structural slab member with explicit permanent and variable loads."""

    def __init__(self, name: str, permanent: Load, variable: Load) -> None:
        self.name = name
        self.permanent = self._validate_load(
            field_name="Slab.permanent",
            load=permanent,
            expected_actiontype=ActionType.PERMANENT,
        )
        self.variable = self._validate_load(
            field_name="Slab.variable",
            load=variable,
            expected_actiontype=ActionType.VARIABLE,
        )

    @staticmethod
    def _validate_load(
        field_name: str,
        load: Load,
        expected_actiontype: ActionType,
    ) -> Load:
        if not isinstance(load, Load):
            raise TypeError(f"{field_name} must be a concrete Load instance.")
        if load.loadcase.actiontype != expected_actiontype:
            raise ValueError(
                f"{field_name} must reference a load with actiontype "
                f"{expected_actiontype.value!r}."
            )
        return load

    @property
    def loads(self) -> tuple[Load, Load]:
        return (self.permanent, self.variable)

    def __repr__(self) -> str:
        return (
            f"Slab(name={self.name!r}, permanent={self.permanent.name!r}, "
            f"variable={self.variable.name!r})"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "permanent": self.permanent.to_dict(),
            "variable": self.variable.to_dict(),
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
            "permanent_name": self.permanent.name,
            "permanent_type": self.permanent.load_type,
            "permanent_loadcase_name": self.permanent.loadcase.name,
            "permanent_value": self.permanent.value,
            "permanent_unit": self.permanent.unit,
            "variable_name": self.variable.name,
            "variable_type": self.variable.load_type,
            "variable_loadcase_name": self.variable.loadcase.name,
            "variable_value": self.variable.value,
            "variable_unit": self.variable.unit,
        }
        return pd.DataFrame([row])
