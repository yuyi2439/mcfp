from mcfp.collecter import Collecter
from mcfp.command import *
from mcfp.data_struct import List

foo_list = List('foo', [1, 2, 3, 4, 5])
with Collecter.collect():
    length = foo_list.len()
