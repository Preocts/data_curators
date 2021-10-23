import pytest

from datacurators.nested_update import nested_update

STEP01 = {"name": "preocts", "type": {}}

STEP02 = {
    "name": "Preocts",
    "type": {
        "style": "egg",
        "size": "smol",
    },
    "likes": [
        {"id": 0},
        {"id": 1},
    ],
}

STEP03 = {
    "type": {
        "style": "Egg",
        "shell": "thicc",
    },
    "likes": [
        {"id": 0},
    ],
}

STEP04 = [STEP01, STEP02, STEP03]


def test_nothing_happens_with_mirrored_input() -> None:
    result = nested_update(STEP01, STEP01)
    assert result == STEP01


def test_add_missing_to_base() -> None:
    result = nested_update(STEP01, STEP02)
    assert result == STEP02


def test_buildin_update_unwanted_behavior() -> None:
    copy = STEP02.copy()
    copy.update(STEP01)
    assert not copy["type"]


def test_handle_nested_mappings_better() -> None:
    result = nested_update(STEP02, STEP01)
    assert result["name"] == "preocts"
    assert result["type"]["style"] == "egg"


def test_nested_mappings_are_updated() -> None:
    result = nested_update(STEP02, STEP03)
    assert len(result["likes"]) == 1
    assert result["type"]["style"] == "Egg"
    assert result["type"]["shell"] == "thicc"


def test_raise_on_type_errors() -> None:
    with pytest.raises(TypeError):
        _ = nested_update(STEP04, STEP01)  # type: ignore

    with pytest.raises(TypeError):
        _ = nested_update(STEP01, STEP04)  # type: ignore
