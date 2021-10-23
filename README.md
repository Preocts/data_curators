[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/data_curators/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/data_curators/main)
[![Python Tests](https://github.com/Preocts/data_curators/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/data_curators/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/Preocts/data_curators/branch/main/graph/badge.svg?token=9LL6DY1POA)](https://codecov.io/gh/Preocts/data_curators)

# data_curators

Tools for the curating of data.

### Requirements
- Python >= 3.8

---


## Dictionary to Dataclass curator
```py
from datacurators.dataclass_curator import dataclass_curator
```

Accepts any dataclass and dictionary. Returns a dictionary that will unpack into dataclass without error.

This is done by matching the dataclass attributes with the dictionary's keys. Missing key/ values, by default, are added as `None`. Unexpected values are removed from the result.

1. Does not enforce type-hints
1. Does not override attribute defaults
1. Default value for missing keywords can be set per call
1. Behavior of adding/removing values can be toggled
1. Optional logging of changes made as INFO level logs

```py
import dataclasses

from datacurators.dataclass_curator import dataclass_curator

@dataclasses.dataclass
class Example:
    first_value: str
    second_value: int
    third_value: bool = False

sample_input = {
    some_value: "This doesn't match",
    second_value: 42,
}

# This will cause a TypeError as we are:
#   - Missing `first_value`
#   - some_value is an unexpected keyword
mydataclass = Example(**sample_input)

# This will not error as we:
#   - Add a None default to `first_value`
#   - Remove `some_value`
mydataclass = Example(**dataclass_curator(Example, sample_input))
```

---

## A better `.update()` for nested mappings
```py
from datacurators.nested_update import nested_update
```

Merge two mappings, inluding nested mappings, returning a new result.

This is done by starting with a copy of map1. Key/values that are unique to map2 are added to map1. Key/values that exist in both are updated with map1[key] = map2[key]. Nested mapping structures have the same logic applied, recursively.

**Note:** Collections of mappings, such as a list of dicts, must be handled with your own implemented logic. This is because there is no way to ensure the order in which objects of the list are updated.

```py
import json
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

step_one = nested_update(STEP01, STEP02)
step_two = nested_update(STEP02, STEP03)

print(json.dumps(step_one, indent=2))
print(json.dumps(step_two, indent=2))
```

### Expected results

```
{
  "name": "Preocts",
  "type": {
    "style": "egg",
    "size": "smol"
  },
  "likes": [
    {
      "id": 0
    },
    {
      "id": 1
    }
  ]
}
{
  "name": "Preocts",
  "type": {
    "style": "Egg",
    "size": "smol",
    "shell": "thicc"
  },
  "likes": [
    {
      "id": 0
    }
  ]
}
```

---
## Local developer installation

It is **highly** recommended to use a `venv` for installation. Leveraging a `venv` will ensure the installed dependency files will not impact other python projects.

Clone this repo and enter root directory of repo:
```bash
$ git clone https://github.com/preocts/data_curators
$ cd data_curators
```

Create and activate `venv`:
```bash
# Linux/MacOS
python3 -m venv venv
. venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate.bat
# or
py -m venv venv
venv\Scripts\activate.bat
```

Your command prompt should now have a `(venv)` prefix on it.

Install editable library and development requirements:
```bash
# Linux/MacOS
pip install -r requirements-dev.txt
pip install --editable .

# Windows
python -m pip install -r requirements-dev.txt
python -m pip install --editable .
# or
py -m pip install -r requirements-dev.txt
py -m pip install --editable .
```

Install pre-commit hooks to local repo:
```bash
pre-commit install
pre-commit autoupdate
```

Run tests
```bash
tox
```

To exit the `venv`:
```bash
deactivate
```

---

### Makefile

This repo has a Makefile with some quality of life scripts if your system supports `make`.

- `install` : Clean all artifacts, update pip, install requirements with no updates
- `update` : Clean all artifacts, update pip, update requirements, install everything
- `build-dist` : Build source distribution and wheel distribution
- `clean-pyc` : Deletes python/mypy artifacts
- `clean-tests` : Deletes tox, coverage, and pytest artifacts
- `clean-build` : Deletes build artifacts
- `clean-all` : Runs all clean scripts
