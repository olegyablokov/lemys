from ..base_commands import GetStateCommand
from ..base_commands import CommandExecutionCode


class Sets(GetStateCommand):
    def __init__(self, _state):
        GetStateCommand.__init__(self, _state)

    names = ['sets']
    description = 'Show current settings'
    argv = {}

    @GetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        print('Shuffle is {value};'.format(value='on' if self.State.shuffle_is_on else 'off'))
        if self.State.shuffle_is_on:
            print('Box length is {length};\n'.format(length='static' if self.State.len_is_static else 'dynamic'))
        print('Current data is {cur_data};\n'
              'Random coefficient is {random_coef};\n'
              'Remember coefficient is {rem_coef};\n'
              'Recent words box size is {size}.'.format(length='static' if self.State.len_is_static else 'dynamic',
                                                        cur_data='favorites' if self.State.cur_data_is_favorites
                                                        else 'main list',
                                                        random_coef=self.State.random_coef,
                                                        rem_coef=self.State.rem_coef,
                                                        size=self.State.recent_words_size))
        return CommandExecutionCode.NO_ANSWER
