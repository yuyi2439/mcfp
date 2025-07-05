from pathlib import Path

from mcfp import compile_and_run

DEBUG = True

fpath = Path(__file__).resolve()

for fp in fpath.parent.rglob('*.py'):
    fname = fp.name
    if not fname.startswith('_'):
        compile_and_run(fpath.with_name(fname), debug=DEBUG)
