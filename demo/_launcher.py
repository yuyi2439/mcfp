from pathlib import Path

import mcfp
from mcfp.compile import compile_all

# mcfp.DEBUG = True

dir_path = Path(__file__).parent

mcfp.NameSpace.set('demo')
mcfp.TargetPath.set(dir_path)

compile_all(dir_path)
