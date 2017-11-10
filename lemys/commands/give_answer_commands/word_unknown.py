from ..base_commands import GiveAnswerCommand
from ..base_commands import CommandExecutionCode


class WordUnknown(GiveAnswerCommand):
    def __init__(self, _state):
        GiveAnswerCommand.__init__(self, _state)

    names = ['\'']
    description = 'Type this if you do not know the translation of the given word'
    argv = {}

    @GiveAnswerCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        return CommandExecutionCode.WORD_UNKNOWN
