from mcfp.collecter import Collecter
from mcfp.command import *
from mcfp.command.util import Storage

with Collecter.collect():
    # data modify storage memo:storage words set value
    Data(Storage('lists'), path='foo', args=['set', 'value', '["a", "b"]'])
