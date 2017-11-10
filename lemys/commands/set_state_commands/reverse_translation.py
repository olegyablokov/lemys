from ..base_commands import SetStateCommand
from ..base_commands import CommandExecutionCode


class ReverseTranslation(SetStateCommand):
    def __init__(self, _state):
        SetStateCommand.__init__(self, _state)

    names = ['reverse', 'rev']
    description = 'Reverse the languages translation (e.g. English: Russian and vice versa)'
    argv = {}

    @SetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        self.State.reverse = not self.State.reverse
        self.State.rev = [3, 2] if self.State.reverse else [2, 3]
        self.State.shift = 3 if self.State.reverse else 0
        print('reverse = {0}'.format(self.State.reverse))
        self.State.words_to_remember = []
        self.State.reset_word_iter()
        return CommandExecutionCode.NO_ANSWER
