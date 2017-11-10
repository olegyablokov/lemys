from ..base_commands import GiveAnswerCommand
from ..base_commands import CommandExecutionCode


class WordKnown(GiveAnswerCommand):
    def __init__(self, _state):
        GiveAnswerCommand.__init__(self, _state)

    names = ['']
    description = 'Type this if you know the translation of the given word'
    argv = {}

    @GiveAnswerCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        self.State.right_ans_counter[1 if self.State.reverse else 0] += 1

        self.State.cur_data[self.State.cur_word_iter][4 + self.State.shift] = \
            str(int(self.State.cur_data[self.State.cur_word_iter][4 + self.State.shift]) + 1)
        return CommandExecutionCode.WORD_KNOWN
