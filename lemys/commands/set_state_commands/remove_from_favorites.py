from ..base_commands import SetStateCommand
from ..base_commands import CommandExecutionCode
import pandas as pd
import numpy as np


class RemoveFromFavorites(SetStateCommand):
    def __init__(self, _state):
        SetStateCommand.__init__(self, _state)

    names = ['uf']
    description = 'Remove a translation from favorites'
    argv = {'': 'Remove the current translation from favorites'}
    # '-p': 'Add the previous translation to favorites'}

    @SetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        if not self.State.cur_data[self.State.cur_word_iter][2:3] in self.State.favorites:
            if not silent_mode:
                print('\'{word}\': Word not in favorites'.format(word=self.State.cur_data[self.State.cur_word_iter]
                                                                                         [self.State.rev[0]]))
            return
        if not silent_mode:
            print('\'{word}\': Word removed from favorites.'.format(word=self.State.cur_data[self.State.cur_word_iter]
                                                                                            [self.State.rev[0]]))
        for k in range(self.State.favorites.shape[0]):
            if self.State.favorites[k][2] == self.State.cur_data[self.State.cur_word_iter, 2]:
                self.State.favorites = np.delete(self.State.favorites, k, axis=0)
                break
        with open(self.State.favorites_fn, 'w', encoding='UTF-8-sig') as f:
            pd.DataFrame(self.State.favorites[:, :4], dtype='str').to_csv(f, header=None, index=False)
        if self.State.cur_data_is_favorites:
            self.State.cur_data = self.State.favorites
            self.State.reset_recent_words()
            self.State.finish -= 1  # TODO: remake box changing verification
            self.State.length -= 1

        return CommandExecutionCode.NO_ANSWER
