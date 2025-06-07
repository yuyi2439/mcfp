import os

from mcfp import compile_and_run

current_dir = os.path.dirname(__file__)
current_file = os.path.basename(__file__)

for fname in os.listdir(current_dir):
    if fname.endswith('.py') and fname != current_file:
        full_path = os.path.join(current_dir, fname)
        compile_and_run(full_path)
