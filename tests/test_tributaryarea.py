import pytest

from structural_loads.domain.tributaryarea import TributaryArea


def test_one_way_tributary_area_repr_and_to_dict():
    tributary_area = TributaryArea.one_way_strip(
        name="Beam strip",
        tributary_width=3.0,
        factor=0.75,
    )

    assert tributary_area.is_one_way is True
    assert tributary_area.is_two_way is False
    assert tributary_area.distribution_type == "one_way_strip"
    assert tributary_area.reference_strip_length == 1.0
    assert tributary_area.effective_tributary_width_x == 2.25
    assert tributary_area.effective_tributary_width_y is None
    assert tributary_area.effective_area == 2.25

    text = repr(tributary_area)
    assert "TributaryArea(" in text
    assert "distribution_type='one_way_strip'" in text
    assert "name='Beam strip'" in text

    assert tributary_area.to_dict() == {
        "name": "Beam strip",
        "distribution_type": "one_way_strip",
        "tributary_width_x": 3.0,
        "tributary_width_y": None,
        "factor_x": 0.75,
        "factor_y": None,
        "reference_strip_length": 1.0,
        "effective_tributary_width_x": 2.25,
        "effective_tributary_width_y": None,
        "effective_area": 2.25,
    }


def test_two_way_tributary_area_to_df():
    try:
        import pandas as pd
    except ImportError:
        pytest.skip("pandas is not installed")

    tributary_area = TributaryArea(
        name="Column patch",
        tributary_width_x=4.0,
        tributary_width_y=5.0,
        factor_x=0.5,
    )

    assert tributary_area.is_one_way is False
    assert tributary_area.is_two_way is True
    assert tributary_area.distribution_type == "two_way_area"
    assert tributary_area.factor_y == 1.0
    assert tributary_area.reference_strip_length is None
    assert tributary_area.effective_tributary_width_x == 2.0
    assert tributary_area.effective_tributary_width_y == 5.0
    assert tributary_area.effective_area == 10.0

    df = tributary_area.to_df()
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, "name"] == "Column patch"
    assert df.loc[0, "distribution_type"] == "two_way_area"
    assert df.loc[0, "factor_y"] == 1.0
    assert df.loc[0, "effective_area"] == 10.0


def test_tributary_area_rejects_non_numeric_width():
    with pytest.raises(TypeError) as exc_info:
        TributaryArea.one_way_strip(name="Invalid strip", tributary_width="wide")

    assert "must be a real number" in str(exc_info.value)


def test_tributary_area_rejects_non_positive_factor():
    with pytest.raises(ValueError) as exc_info:
        TributaryArea.two_way_area(
            name="Invalid patch",
            tributary_width_x=3.0,
            tributary_width_y=4.0,
            factor_x=0.0,
        )

    assert "must be greater than 0" in str(exc_info.value)


def test_tributary_area_rejects_factor_y_without_width_y():
    with pytest.raises(ValueError) as exc_info:
        TributaryArea(
            name="Invalid strip",
            tributary_width_x=3.0,
            factor_y=0.9,
        )

    assert "can only be set when tributary_width_y is provided" in str(exc_info.value)
