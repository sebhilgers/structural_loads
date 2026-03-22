import pytest

from structural_loads.domain.actions import ActionCategory, ActionType
from structural_loads.domain.loadcase import LoadCase
from structural_loads.domain.loadcollection import LoadCollection
from structural_loads.domain.loads import AreaLoad, LineLoad, PointLoad


def test_loadcollection_add_methods_create_and_store_loads():
    collection = LoadCollection(name="roof loads")
    snow = LoadCase(name="LC1", category=ActionCategory.SNOW)
    wind = LoadCase(name="LC2", category=ActionCategory.WIND)
    permanent = LoadCase(name="LC3", category=ActionCategory.PERMANENT)

    area = collection.add_areaload(name="q_snow", loadcase=snow, value=2.75)
    line = collection.add_lineload(name="w_edge", loadcase=wind, value=4.0)
    point = collection.add_pointload(name="P_column", loadcase=permanent, value=35.0)

    assert isinstance(area, AreaLoad)
    assert isinstance(line, LineLoad)
    assert isinstance(point, PointLoad)
    assert collection.name == "roof loads"
    assert len(collection) == 3
    assert [load.name for load in collection.loads] == ["q_snow", "w_edge", "P_column"]


def test_loadcollection_exposes_only_compact_add_method_names():
    assert not hasattr(LoadCollection, "add_area_load")
    assert not hasattr(LoadCollection, "add_line_load")
    assert not hasattr(LoadCollection, "add_point_load")


def test_loadcollection_sort_by_loadcase_reorders_collection():
    collection = LoadCollection(name="sorted by loadcase")
    lc_accidental = LoadCase(name="LC1", category=ActionCategory.ANPRALL)
    lc_variable = LoadCase(name="LC2", category=ActionCategory.SNOW)
    lc_permanent = LoadCase(name="LC3", category=ActionCategory.PERMANENT)

    collection.add_pointload(name="A_impact", loadcase=lc_accidental, value=8.0)
    collection.add_lineload(name="Q_snow", loadcase=lc_variable, value=2.0)
    collection.add_areaload(name="G_slab", loadcase=lc_permanent, value=1.5)

    collection.sort_by_loadcase()

    assert [(load.loadcase.actiontype, load.name) for load in collection] == [
        (ActionType.PERMANENT, "G_slab"),
        (ActionType.VARIABLE, "Q_snow"),
        (ActionType.ACCIDENTAL, "A_impact"),
    ]


def test_loadcollection_sort_by_action_definition_reorders_collection():
    collection = LoadCollection(name="sorted by action")
    lc_wind = LoadCase(name="LC3", category=ActionCategory.WIND)
    lc_perm = LoadCase(name="LC1", category=ActionCategory.PERMANENT)
    lc_snow = LoadCase(name="LC2", category=ActionCategory.SNOW)
    lc_acc = LoadCase(name="LC0", category=ActionCategory.ANPRALL)

    collection.add_lineload(name="w_edge", loadcase=lc_wind, value=3.0)
    collection.add_pointload(name="P_wall", loadcase=lc_perm, value=12.0)
    collection.add_areaload(name="q_snow", loadcase=lc_snow, value=1.8)
    collection.add_pointload(name="P_barrier", loadcase=lc_acc, value=20.0)

    collection.sort_by_action_definition()

    assert [(load.loadcase.actiontype, load.name) for load in collection] == [
        (ActionType.PERMANENT, "P_wall"),
        (ActionType.VARIABLE, "q_snow"),
        (ActionType.VARIABLE, "w_edge"),
        (ActionType.ACCIDENTAL, "P_barrier"),
    ]


def test_loadcollection_to_df_lists_loads_sorted_by_loadcase():
    try:
        import pandas as pd
    except ImportError:
        pytest.skip("pandas is not installed")

    collection = LoadCollection(name="dataframe export")
    lc_wind = LoadCase(name="LC2", category=ActionCategory.WIND)
    lc_snow = LoadCase(
        name="LC1",
        category=ActionCategory.SNOW,
        description="Roof drift",
    )

    collection.add_pointload(name="P_edge", loadcase=lc_wind, value=5.0)
    collection.add_areaload(name="q_roof", loadcase=lc_snow, value=2.1)

    df = collection.to_df()

    assert isinstance(df, pd.DataFrame)
    assert list(df["loadcase_name"]) == ["LC1", "LC2"]
    assert list(df.columns) == [
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
    assert df.loc[0, "type"] == "AreaLoad"
    assert df.loc[0, "loadcase_category"] == ActionCategory.SNOW.value
    assert df.loc[0, "loadcase_description"] == "Roof drift"
    assert df.loc[0, "action_type"] == ActionType.VARIABLE.value
    assert df.loc[0, "value"] == 2.1
    assert df.loc[0, "unit"] == "kN/m²"


def test_loadcollection_add_load_rejects_non_load_instance():
    collection = LoadCollection(name="invalid load")

    with pytest.raises(TypeError) as exc_info:
        collection.add_load(load="not_a_load")

    assert "concrete Load instance" in str(exc_info.value)
