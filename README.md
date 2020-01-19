# homie-spec

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/homie-spec.svg?style=flat-square)](https://pypi.python.org/pypi/homie-spec/)
[![GitHub license](https://img.shields.io/github/license/Qu4tro/homie-spec.svg?style=flat-square)](https://github.com/Qu4tro/homie-spec/blob/master/LICENSE)
[![PyPI version shields.io](https://img.shields.io/pypi/v/homie-spec.svg?style=flat-square)](https://pypi.python.org/pypi/homie-spec/)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square)](https://GitHub.com/Qu4tro/homie-spec/graphs/commit-activity)
[![Coverage](https://img.shields.io/codecov/c/github/Qu4tro/homie-spec?style=flat-square)](https://codecov.io/gh/Qu4tro/homie-spec)
[![Build Status](https://img.shields.io/travis/Qu4tro/homie-spec/master?style=flat-square)](https://travis-ci.com/Qu4tro/homie-spec)

**homie-spec** is a Python library that models the v4 [Homie Convention](https://homieiot.github.io/).

This package has no dependencies other than **Python >=3.6**. Since it doesn't implement MQTT this also means it's fairly useless on it's own, as it has no ability to interact with any MQTT broker on it's own.

The goal of this package is to provide a data-driven library to easily create `devices`, `nodes` and `properties`. These can also be published to be used by anyone.
Another package (WIP), will bridge the MQTT protocol and `homie-spec`.

Relevant external links:
  - [Documentation](https://qu4tro.github.io/homie-spec/)
  - [Specification](https://homieiot.github.io/specification/spec-core-v4_0_0/#)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `homie-spec`.

```bash
pip install homie-spec
```

## Usage

```python

from homie_spec import Device, Node, Property
from homie_spec.properties import Datatype


localtime = Node(
    name="Local time",
    typeOf="clock",
    properties={
        "color-repr": Property(
            name="Color representation", datatype=Datatype.COLOR, get=lambda: "233,102,23"
        ),
        "time": Property(
            name="HH:MM representation", datatype=Datatype.STRING, get=lambda: "20:20"
        ),
    },
)

desktop = Device(id="desktop", name="Desktop Computer", nodes={"local-time": localtime})

for msg in desktop.messages():
    print(msg.attrs)
print(desktop.getter_message('local-time/time').attrs)
print(desktop.getter_message('local-time/color-repr').attrs)

"""
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/$state',                          'payload': 'init'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/$name',                           'payload': 'Desktop Computer'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/$homie',                          'payload': '4.0.0'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/$implementation',                 'payload': 'homie-spec'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/$nodes',                          'payload': 'local-time'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/local-time/$name',                'payload': 'Local time'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/local-time/$type',                'payload': 'clock'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/local-time/$properties',          'payload': 'color-repr,time'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/local-time/color-repr/$name',     'payload': 'Color representation'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/local-time/color-repr/$datatype', 'payload': 'color'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/local-time/time/$name',           'payload': 'HH:MM representation'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/local-time/time/$datatype',       'payload': 'string'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/$state',                          'payload': 'ready'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/local-time/time',                 'payload': '20:20'}
{'retained': True, 'qos': 1, 'topic': 'homie/desktop/local-time/color-repr',           'payload': '233,102,23'}
"""
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
