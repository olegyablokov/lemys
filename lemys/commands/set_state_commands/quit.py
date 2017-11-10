from ..base_commands import SetStateCommand
from ..base_commands import CommandExecutionCode


class Quit(SetStateCommand):
    def __init__(self, _state):
        SetStateCommand.__init__(self, _state)

    names = ['quit', 'q']
    description = 'Finish the program'
    argv = {}

    def execute(self, args, silent_mode=False):
        print('Session finished.')
        return CommandExecutionCode.REQUEST_FINISH
