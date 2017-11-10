from ..base_commands import GetStateCommand
from ..base_commands import CommandExecutionCode
import pandas as pd


class ViewBox(GetStateCommand):
    def __init__(self, _state):
        GetStateCommand.__init__(self, _state)

    names = ['viewbox', 'vb']
    description = 'View a box'
    argv = {'': 'Show the words which are currently used',
            '-f': 'Show favorites box',
            '-rw': 'Show recent words box',
            '-rem': 'Show words to be remembered (hint: words not encountered yet are not in this list)'}

    @GetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        if not args:
            pd.set_option('display.max_rows', self.State.length)
            print(pd.DataFrame(data=self.State.cur_data[self.State.start:self.State.finish, 2:4]))
            if not self.State.shuffle_is_on:
                print('start = {start};\nfinish = {finish}.'.format(start=self.State.start, finish=self.State.finish))
        else:
            for args_local in args:
                if args_local[0] == '-f':
                    pd.set_option('display.max_rows', len(self.State.favorites))
                    if self.State.favorites.shape[0]:
                        print('Favorites list:\n{list}'.format(list=pd.DataFrame(data=self.State.favorites[:, 2:4])))
                    else:
                        print('Favorites list is empty.')
                elif args_local[0] == '-rw':
                    pd.set_option('display.max_rows', self.State.recent_words_cur_size)
                    if self.State.recent_words_cur_size:
                        print('Recent words box:\n{box}'.format(box=pd.DataFrame(
                            data=self.State.recent_words[:self.State.recent_words_cur_size])))
                    else:
                        print('Recent words box is empty.')
                elif args_local[0] == '-rem':
                    if self.State.words_to_remember:
                        pd.set_option('display.max_rows', len(self.State.words_to_remember))
                        print(pd.DataFrame(self.State.words_to_remember))
                    else:
                        print('No words to remember.')
            pd.reset_option('display.max_rows')

        return CommandExecutionCode.NO_ANSWER

