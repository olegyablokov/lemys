from ..base_commands import SetStateCommand
from ..base_commands import CommandExecutionCode
import numpy as np


class Shuffle(SetStateCommand):
    def __init__(self, _state):
        SetStateCommand.__init__(self, _state)

    names = ['shuffle', 'shuf', 'sh']
    description = 'Shuffle all the words from the table'
    argv = {}

    @SetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        if self.State.shuffle_is_on:
            if self.State.cur_data_is_favorites:
                print('Shuffle is unavailable when current data is favorites.')
            else:
                print('Shuffle is off.')
                assert self.State.shuffle_is_on
                self.State.shuffle_is_on = False
                if self.State.cur_data_is_favorites:
                    self.State.cur_data = self.State.favorites[self.State.start:self.State.finish]
                else:
                    self.State.cur_data = self.State.all_data
                self.State.reset_recent_words()
                self.State.words_to_remember = []
        else:
            if self.State.cur_data_is_favorites:
                print('Shuffle is unavailable when current data is favorites.')
            else:
                print('Shuffle is on.')
                assert not self.State.shuffle_is_on
                self.State.shuffle_is_on = True
                self.State.cur_data = self.State.cur_data[
                    np.random.choice(range(self.State.cur_data.shape[0]), self.State.cur_data.shape[0],
                                     replace=False)]
                self.State.reset_recent_words()
                self.State.words_to_remember = []
        return CommandExecutionCode.NO_ANSWER
