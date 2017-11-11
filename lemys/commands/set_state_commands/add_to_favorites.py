from ..base_commands import SetStateCommand
from ..base_commands import CommandExecutionCode
import pandas as pd
import numpy as np


class AddToFavorites(SetStateCommand):
    def __init__(self, _state):
        SetStateCommand.__init__(self, _state)

    names = ['f']
    description = 'Add a translation to favorites'
    argv = {'': 'Add the current translation to favorites',
            '-p': 'Add the previous translation to favorites'}

    @SetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        word_to_add = ''  # or, more accurately, line containing the word to add
        if not args:
            word_to_add = self.State.cur_data[self.State.cur_word_iter]
        else:
            for args_local in args:
                if args_local[0] == '-p':
                    if self.State.prev_word_iter:
                        word_to_add = self.State.cur_data[self.State.prev_word_iter]
                    else:
                        raise ValueError('No previous word defined')

        if self.State.favorites.shape[0]:
            if self.State.cur_data_is_favorites or \
                            word_to_add[2] in self.State.favorites[:, 2]:
                if not silent_mode:
                    print('\'{word}\': Word already in favorites'.format(word=word_to_add[2]))
                return
        if not silent_mode:
            print('\'{word}\': Word added to favorites.'.format(word=word_to_add[2]))
        with open(self.State.favorites_fn, 'a', encoding='UTF-8-sig') as f:
            pd.DataFrame(word_to_add[:4], dtype='str').T.to_csv(f,
                                                                header=None,
                                                                index=False)
        self.State.favorites = np.vstack((self.State.favorites, word_to_add))

        if self.State.cur_data_is_favorites:
            self.State.cur_data = self.State.favorites

        return CommandExecutionCode.NO_ANSWER
