import pytest

from structural_loads.domain.actions import ActionCategory
from structural_loads.domain.loadcase import LoadCase
from structural_loads.domain.loads import AreaLoad, LineLoad, PointLoad


def test_area_load_repr_and_to_dict():
    loadcase = LoadCase(name="LC1", category=ActionCategory.SNOW, description="Roof drift")
    load = AreaLoad(name="q_snow", loadcase=loadcase, value=2.75)

    text = repr(load)
    assert "AreaLoad(" in text
    assert "name='q_snow'" in text
    assert "loadcase='LC1'" in text
    assert "value=2.75" in text
    assert "unit='kN/m²'" in text

    assert load.to_dict() == {
        "type": "AreaLoad",
        "name": "q_snow",
        "loadcase": {
            "name": "LC1",
            "category": ActionCategory.SNOW.value,
            "description": "Roof drift",
        },
        "value": 2.75,
        "unit": "kN/m²",
    }


def test_line_load_default_unit():
    loadcase = LoadCase(name="LC2", category=ActionCategory.WIND)
    load = LineLoad(name="w_edge", loadcase=loadcase, value=4.0)

    assert load.unit == "kN/m"
    assert load.load_type == "LineLoad"


def test_point_load_to_df():
    try:
        import pandas as pd
    except ImportError:
        pytest.skip("pandas is not installed")

    loadcase = LoadCase(
        name="LC3",
        category=ActionCategory.RESIDENTIAL,
        description="Office floor",
    )
    load = PointLoad(name="P_column", loadcase=loadcase, value=35)

    df = load.to_df()
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, "type"] == "PointLoad"
    assert df.loc[0, "name"] == "P_column"
    assert df.loc[0, "loadcase_name"] == "LC3"
    assert df.loc[0, "loadcase_category"] == ActionCategory.RESIDENTIAL.value
    assert df.loc[0, "loadcase_description"] == "Office floor"
    assert df.loc[0, "value"] == 35.0
    assert df.loc[0, "unit"] == "kN"


def test_load_rejects_non_loadcase():
    with pytest.raises(TypeError) as exc_info:
        AreaLoad(name="q_invalid", loadcase="LC4", value=1.0)

    assert "must be a LoadCase" in str(exc_info.value)


def test_load_rejects_non_numeric_value():
    loadcase = LoadCase(name="LC5", category=ActionCategory.PERMANENT)

    with pytest.raises(TypeError) as exc_info:
        PointLoad(name="P_invalid", loadcase=loadcase, value="high")

    assert "must be a real number" in str(exc_info.value)
