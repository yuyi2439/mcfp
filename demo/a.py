from mcfp import NameSpace
from mcfp.collecter import Collecter
from mcfp.command import *
from mcfp.command.util import Position, Selector

NameSpace.set('demo')

Say('Hello Minecraft world!')()

setblock(Position(0, 64, 0), 'minecraft:stone')()
setblock((-1, 64, 0), 'minecraft:grass_block')()
setblock(1, 64, 0, 'minecraft:dirt')()

# a little complex
Execute().at(Selector('s')).run(Say('Executing from entity'))()

with Collecter.collect():
    Say('Hello Minecraft world!')
    setblock(Position(0, 64, 0), 'minecraft:stone')
    Execute().at('@s').run(Say('Executing from entity'))


cmd = Function('b')
for i in range(2):
    cmd()
