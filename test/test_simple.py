from mcfp.command import *
from mcfp import Compiler

def test_simple_commands():
    Say("Hello Minecraft world!")()
    SetBlock(0, 64, 0, "minecraft:stone")()
    SetBlock(1, 64, 0, "minecraft:dirt")()

    Execute([('at', Selector('s'))], Say("Executing from entity"))()

    cmd = Function("example", "my_function")
    for i in range(5):
        cmd()
    

    assert len(Compiler.commands) == 9
