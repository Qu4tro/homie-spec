from homie_spec import Device, Node, Property
from homie_spec.properties import Datatype

# pylint: skip-file


localtime = Node(
    name="Local time",
    typeOf="clock",
    properties={
        "color-repr": Property(
            name="Color representation", datatype=Datatype.COLOR, get=lambda: "20:20"
        ),
        "time": Property(
            name="HH:MM representation",
            datatype=Datatype.STRING,
            get=lambda: "233,102,23",
        ),
    },
)

desktop = Device(id="desktop", name="Desktop Computer", nodes={"local-time": localtime})

for msg in desktop.messages():
    print(msg.attrs)
print(desktop.getter_message("local-time/time").attrs)
print(desktop.getter_message("local-time/color-repr").attrs)

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
