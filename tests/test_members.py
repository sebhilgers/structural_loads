import pytest

from structural_loads.domain.actions import ActionCategory
from structural_loads.domain.loadcase import LoadCase
from structural_loads.domain.loads import AreaLoad
from structural_loads.domain.members import Slab


def test_slab_stores_permanent_and_variable_loads():
    permanent = AreaLoad(
        name="g_floor",
        loadcase=LoadCase(name="G", category=ActionCategory.PERMANENT),
        value=4.5,
    )
    variable = AreaLoad(
        name="q_floor",
        loadcase=LoadCase(name="Q", category=ActionCategory.RESIDENTIAL),
        value=2.0,
    )

    slab = Slab(name="S1", permanent=permanent, variable=variable)

    assert slab.name == "S1"
    assert slab.permanent is permanent
    assert slab.variable is variable
    assert slab.loads == (permanent, variable)
    assert slab.to_dict() == {
        "name": "S1",
        "permanent": permanent.to_dict(),
        "variable": variable.to_dict(),
    }


def test_slab_repr():
    permanent = AreaLoad(
        name="g_floor",
        loadcase=LoadCase(name="G", category=ActionCategory.PERMANENT),
        value=4.5,
    )
    variable = AreaLoad(
        name="q_floor",
        loadcase=LoadCase(name="Q", category=ActionCategory.SNOW),
        value=1.2,
    )

    text = repr(Slab(name="S2", permanent=permanent, variable=variable))

    assert "Slab(" in text
    assert "name='S2'" in text
    assert "permanent='g_floor'" in text
    assert "variable='q_floor'" in text


def test_slab_rejects_non_load_object():
    variable = AreaLoad(
        name="q_floor",
        loadcase=LoadCase(name="Q", category=ActionCategory.SNOW),
        value=1.2,
    )

    with pytest.raises(TypeError) as exc_info:
        Slab(name="S3", permanent="not_a_load", variable=variable)

    assert "Slab.permanent must be a concrete Load instance" in str(exc_info.value)


def test_slab_rejects_non_permanent_load_for_permanent_attribute():
    not_permanent = AreaLoad(
        name="q_floor",
        loadcase=LoadCase(name="Q", category=ActionCategory.SNOW),
        value=1.2,
    )
    variable = AreaLoad(
        name="q_live",
        loadcase=LoadCase(name="Q2", category=ActionCategory.RESIDENTIAL),
        value=2.0,
    )

    with pytest.raises(ValueError) as exc_info:
        Slab(name="S4", permanent=not_permanent, variable=variable)

    assert "Slab.permanent must reference a load with actiontype" in str(exc_info.value)


def test_slab_rejects_non_variable_load_for_variable_attribute():
    permanent = AreaLoad(
        name="g_floor",
        loadcase=LoadCase(name="G", category=ActionCategory.PERMANENT),
        value=4.5,
    )
    not_variable = AreaLoad(
        name="a_impact",
        loadcase=LoadCase(name="A", category=ActionCategory.ANPRALL),
        value=8.0,
    )

    with pytest.raises(ValueError) as exc_info:
        Slab(name="S5", permanent=permanent, variable=not_variable)

    assert "Slab.variable must reference a load with actiontype" in str(exc_info.value)
