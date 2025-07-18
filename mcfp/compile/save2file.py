import shutil
from pathlib import Path

import mcfp


def copy_built_ins(target: Path | None = None):
    if target is None:
        target = mcfp.TargetPath.get()
    built_in_dir = target / 'mcfp_gen' / 'function' / 'built_in'
    shutil.rmtree(built_in_dir, ignore_errors=True)
    shutil.copytree(
        Path(mcfp.__path__[0]) / '_built_in',
        built_in_dir,
        dirs_exist_ok=True,
    )
    from mcfp import DEBUG

    if not DEBUG:
        shutil.rmtree(built_in_dir / '_debug')
