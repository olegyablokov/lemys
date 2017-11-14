from commands import Command, get_commands, CommandExecutionCode


class CommandRunner:
    def __init__(self, _state, _dict):
        self.State = _state
        self.CommandsDict = None
        self.Dictionary = _dict

    def init(self):
        Command.set_dict(self.Dictionary)
        self.CommandsDict = self.__load_commands()

    def __load_commands(self):
        _Commands = get_commands()
        _CommandsDict = {}
        for _Command in _Commands:
            _Object = _Command(self.State)
            for name in _Object.names:
                _CommandsDict[name] = _Object
        return _CommandsDict

    def run(self):
        Command.init(self.State)
        while True:
            try:
                x = input()
                if x == '':
                    x = ['']
                else:
                    x = x.split()

                if x[0] in self.CommandsDict.keys():
                    execution_code = self.CommandsDict[x[0]].execute(x)

                    if execution_code == CommandExecutionCode.REQUEST_FINISH:
                        break
                    elif execution_code == CommandExecutionCode.WORD_KNOWN:
                        pass
                    elif execution_code == CommandExecutionCode.WORD_UNKNOWN:
                        pass
                    elif execution_code == CommandExecutionCode.NO_ANSWER:
                        pass
                    elif execution_code == CommandExecutionCode.COMMAND_NOT_IMPLEMENTED:
                        print('{name}: Command not implemented.'.format(name=self.CommandsDict[x].names[0]))
                else:
                    print('Error: no such command.')
            except ValueError as e:
                print('Error: {error}.'.format(error=e))
