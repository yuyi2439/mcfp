from mcfp.compiler import compile_file


if __name__ == '__main__':
    filename = 'example/a'
    compile_file(filename)
    print(f"Compiled {filename}.py to {filename}.mcfunction")