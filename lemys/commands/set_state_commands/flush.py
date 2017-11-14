from ..base_commands import SetStateCommand
from ..base_commands import CommandExecutionCode
import numpy as np


class Flush(SetStateCommand):
    def __init__(self, _state):
        SetStateCommand.__init__(self, _state)

    names = ['flush', 'fl']
    description = 'Flush data'
    argv = {'': 'Flush rate history',
            '-fv': 'Flush favorites list',
            '-wr': 'Flush words to remember'}

    @SetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        if len(args) == 0:
            self.State.reset_rate_history()
        else:
            for args_local in args:
                if args_local[0] == '-fv':
                    if self.State.cur_data_is_favorites:
                        self.State.cur_data_is_favorites = False
                        self.State.cur_data = self.State.all_data
                        print('Switched to main list.')

                        self.State.rev_start, self.State.start = self.State.start, self.State.rev_start
                        self.State.rev_finish, self.State.finish = self.State.finish, self.State.rev_finish
                        self.State.length = self.State.finish - self.State.start
                        self.State.reset_recent_words()

                    # deleting all data from favorites file
                    with open(self.State.favorites_fn, 'w') as f:
                        f.seek(0)
                        f.truncate()
                    self.State.favorites = np.empty([0, 10])
                    print('Favorites flushed.')
                elif args_local[0] == '-wr':
                    self.State.words_to_remember = []
                    print('Words to remember flushed.')

        return CommandExecutionCode.NO_ANSWER
