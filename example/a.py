from mcfp import Compiler
from mcfp.command import *
from mcfp.command.commands import Say, SetBlock
from mcfp.command.util import Position

# 简单的命令序列
Say('Hello Minecraft world!')()
SetBlock(Position(0, 64, 0), 'minecraft:stone')()
setblock(1, 64, 0, 'minecraft:dirt')()

# 稍复杂的命令
Execute().at(Selector('s')).run(Say('Executing from entity'))()

cmd = Function('example', 'my_function')
for i in range(5):
    cmd()

Compiler.save_commands('a.mcfunction')
