import pytest

from structural_loads.domain.actions import ActionCategory, ActionDefinition, ActionFactors, ActionType


def test_action_factors_from_category_values():
    factors = ActionFactors.from_category(ActionCategory.RESIDENTIAL)
    assert factors.psi_0 == 0.7
    assert factors.psi_1 == 0.5
    assert factors.psi_2 == 0.3
    assert factors.duration_class.value == "medium"


def test_action_factors_to_dict_and_repr():
    factors = ActionFactors.from_category(ActionCategory.SNOW)
    d = factors.to_dict()
    assert d == {
        "psi_0": 0.5,
        "psi_1": 0.2,
        "psi_2": 0.0,
        "duration_class": "short",
    }
    assert "ActionFactors(" in repr(factors)
    assert "psi_0=0.5" in repr(factors)


def test_action_definition_category_auto_population():
    action_def = ActionDefinition(category=ActionCategory.WIND, description="Wind load")
    assert action_def.type == ActionType.VARIABLE
    assert action_def.category == ActionCategory.WIND
    assert action_def.description == "Wind load"
    assert isinstance(action_def.factors, ActionFactors)
    assert action_def.factors.psi_0 == 0.6


def test_action_definition_to_dict_and_repr():
    action_def = ActionDefinition(category=ActionCategory.LAGER, description="Storage load")
    d = action_def.to_dict()
    assert d["category"] == ActionCategory.LAGER.value
    assert d["type"] == ActionType.VARIABLE.value
    assert d["description"] == "Storage load"
    assert d["factors"]["psi_0"] == 1.0
    assert "ActionDefinition(" in repr(action_def)


def test_action_definition_to_df():
    try:
        import pandas as pd
    except ImportError:
        pytest.skip("pandas is not installed")

    action_def = ActionDefinition(category=ActionCategory.VERSAMMLUNG, description="Assembly load")
    df = action_def.to_df()
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, "category"] == ActionCategory.VERSAMMLUNG.value
    assert df.loc[0, "type"] == ActionType.VARIABLE.value
    assert df.loc[0, "description"] == "Assembly load"
    assert df.loc[0, "psi_0"] == 0.7
    assert df.loc[0, "duration_class"] == "short"
