from __future__ import annotations

from numbers import Real


class TributaryArea:
    """Explicit tributary area definition used for simplified load derivation.

    A one-way tributary area is represented as a 1.0 m reference strip with a
    tributary width in x-direction and one factor. A two-way tributary area
    stores tributary widths in x- and y-direction with separate factors.
    """

    def __init__(
        self,
        name: str,
        tributary_width_x: float,
        tributary_width_y: float | None = None,
        factor_x: float = 1.0,
        factor_y: float | None = None,
    ) -> None:
        self.name = name
        self.tributary_width_x = self._validate_positive_real(
            "TributaryArea.tributary_width_x",
            tributary_width_x,
        )
        self.factor_x = self._validate_positive_real("TributaryArea.factor_x", factor_x)

        if tributary_width_y is None:
            if factor_y is not None:
                raise ValueError(
                    "TributaryArea.factor_y can only be set when tributary_width_y "
                    "is provided."
                )
            self.tributary_width_y = None
            self.factor_y = None
        else:
            self.tributary_width_y = self._validate_positive_real(
                "TributaryArea.tributary_width_y",
                tributary_width_y,
            )
            resolved_factor_y = 1.0 if factor_y is None else factor_y
            self.factor_y = self._validate_positive_real(
                "TributaryArea.factor_y",
                resolved_factor_y,
            )

    @classmethod
    def one_way_strip(
        cls,
        name: str,
        tributary_width: float,
        factor: float = 1.0,
    ) -> "TributaryArea":
        return cls(name=name, tributary_width_x=tributary_width, factor_x=factor)

    @classmethod
    def two_way_area(
        cls,
        name: str,
        tributary_width_x: float,
        tributary_width_y: float,
        factor_x: float = 1.0,
        factor_y: float = 1.0,
    ) -> "TributaryArea":
        return cls(
            name=name,
            tributary_width_x=tributary_width_x,
            tributary_width_y=tributary_width_y,
            factor_x=factor_x,
            factor_y=factor_y,
        )

    @staticmethod
    def _validate_positive_real(field_name: str, value: float) -> float:
        if not isinstance(value, Real) or isinstance(value, bool):
            raise TypeError(f"{field_name} must be a real number.")
        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0.")
        return float(value)

    @property
    def is_one_way(self) -> bool:
        return self.tributary_width_y is None

    @property
    def is_two_way(self) -> bool:
        return not self.is_one_way

    @property
    def distribution_type(self) -> str:
        return "one_way_strip" if self.is_one_way else "two_way_area"

    @property
    def reference_strip_length(self) -> float | None:
        return 1.0 if self.is_one_way else None

    @property
    def effective_tributary_width_x(self) -> float:
        return self.tributary_width_x * self.factor_x

    @property
    def effective_tributary_width_y(self) -> float | None:
        if self.tributary_width_y is None:
            return None
        return self.tributary_width_y * self.factor_y

    @property
    def effective_area(self) -> float:
        if self.effective_tributary_width_y is None:
            return self.effective_tributary_width_x * 1.0
        return self.effective_tributary_width_x * self.effective_tributary_width_y

    def __repr__(self) -> str:
        return (
            f"TributaryArea(name={self.name!r}, "
            f"distribution_type={self.distribution_type!r}, "
            f"tributary_width_x={self.tributary_width_x!r}, "
            f"tributary_width_y={self.tributary_width_y!r}, "
            f"factor_x={self.factor_x!r}, factor_y={self.factor_y!r})"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "distribution_type": self.distribution_type,
            "tributary_width_x": self.tributary_width_x,
            "tributary_width_y": self.tributary_width_y,
            "factor_x": self.factor_x,
            "factor_y": self.factor_y,
            "reference_strip_length": self.reference_strip_length,
            "effective_tributary_width_x": self.effective_tributary_width_x,
            "effective_tributary_width_y": self.effective_tributary_width_y,
            "effective_area": self.effective_area,
        }

    def to_df(self):
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for to_df(); install with 'pip install pandas'"
            ) from exc

        return pd.DataFrame([self.to_dict()])
