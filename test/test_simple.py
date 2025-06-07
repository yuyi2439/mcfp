from mcfp import Collecter
from mcfp.command import *
from mcfp.command.commands import Say
from mcfp.command.util import Position

# Please see demo for more examples
# This isn't available. I plan to enable it in the future.

# def test_simple_commands():
#     Say('Hello Minecraft world')()
#     SetBlock(Position(0, 64, 0), 'minecraft:stone')()
#     # SetBlock(1, 64, 0, 'minecraft:dirt')()

#     Execute().at(Selector('s')).run(Say('Executing from entity'))()

#     cmd = Function('example', 'my_function')
#     for i in range(5):
#         cmd()

#     assert len(Collecter.commands) == 8
