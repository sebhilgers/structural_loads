import pytest

from structural_loads.domain.actions import ActionCategory, ActionDefinition, ActionType
from structural_loads.domain.loadcase import LoadCase


def test_loadcase_builds_action_definition_from_category():
    loadcase = LoadCase(
        name="LC0",
        category=ActionCategory.WIND,
    )

    assert isinstance(loadcase.action, ActionDefinition)
    assert loadcase.action.category == ActionCategory.WIND
    assert loadcase.action.type == ActionType.VARIABLE
    assert loadcase.action.factors.psi_0 == 0.6
    assert loadcase.action.description == ""


def test_loadcase_repr():
    loadcase = LoadCase(
        name="LC1",
        category=ActionCategory.SNOW,
        description="Snow drift",
    )

    text = repr(loadcase)
    assert "LoadCase(" in text
    assert "name='LC1'" in text
    assert "category='Schneelast'" in text
    assert "description='Snow drift'" in text


def test_loadcase_to_df():
    try:
        import pandas as pd
    except ImportError:
        pytest.skip("pandas is not installed")

    loadcase = LoadCase(
        name="LC2",
        category=ActionCategory.WIND,
        description="Facade pressure",
    )

    df = loadcase.to_df()
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, "name"] == "LC2"
    assert df.loc[0, "category"] == ActionCategory.WIND.value
    assert df.loc[0, "description"] == "Facade pressure"


def test_loadcase_rejects_non_action_category():
    with pytest.raises(TypeError) as exc_info:
        LoadCase(
            name="LC3",
            category=[ActionCategory.SNOW],
            description="Invalid",
        )

    assert "must be an ActionCategory" in str(exc_info.value)


def test_loadcase_rejects_prebuilt_action_definition():
    with pytest.raises(TypeError) as exc_info:
        LoadCase(
            name="LC3b",
            category=ActionDefinition(category=ActionCategory.SNOW),
            description="Invalid",
        )

    assert "must be an ActionCategory" in str(exc_info.value)


def test_loadcase_to_dict_uses_action_category_value():
    loadcase = LoadCase(
        name="LC4",
        category=ActionCategory.RESIDENTIAL,
        description="Apartment floor",
    )

    assert loadcase.to_dict() == {
        "name": "LC4",
        "category": ActionCategory.RESIDENTIAL.value,
        "description": "Apartment floor",
    }
