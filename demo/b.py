from mcfp.collecter import Collecter
from mcfp.command import *

with Collecter.collect():
    Say("This is in file b.py")

Collecter.save_commands()
