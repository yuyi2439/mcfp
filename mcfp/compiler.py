

class Compiler:
    commands: list[str] = []
    
    @classmethod
    def add_command(cls, command: str):
        cls.commands.append(command)
    
    @classmethod
    def save_commands(cls, filename: str):
        with open(filename, 'w', encoding='utf8') as file:
            for command in cls.commands:
                file.write(command + '\n')
