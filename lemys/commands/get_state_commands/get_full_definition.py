from ..base_commands import GetStateCommand
from ..base_commands import CommandExecutionCode


class GetFullDefinition(GetStateCommand):
    def __init__(self, _state):
        GetStateCommand.__init__(self, _state)

    names = ['def']
    description = 'Get the full definition of a word'
    argv = {'': 'Get the full definition of the current word',
            '-w': 'Get the full definition of the word followed after \'-w\', e.g. \'-w meadow\'',
            '-p': 'Get the full definition of the previous word'}
    full_description = 'www.wordsapi.com/docs'

    @GetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        request_word = ''
        if not args:
            request_word = self.State.cur_data[self.State.cur_word_iter][2]
        else:
            for args_local in args:
                if args_local[0] == '-w':
                    if len(args[0]) > 1:
                        for word in args[0][1:]:
                            request_word += word + ' '
                        request_word = request_word[:-1]
                elif args_local[0] == '-p':
                    if self.State.prev_word_iter:
                        request_word = self.State.cur_data[self.State.prev_word_iter][2]
                    else:
                        raise ValueError('No previous word defined')
        if request_word:
            print('Full definition(s) for \'{word}\':\n'
                  '{definition}'.format(word=request_word, definition=Command.Dictionary.get_info(request_word)))

        return CommandExecutionCode.NO_ANSWER
