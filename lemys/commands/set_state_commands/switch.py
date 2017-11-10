from ..base_commands import SetStateCommand
from ..base_commands import CommandExecutionCode
import numpy as np


class Switch(SetStateCommand):
    def __init__(self, _state):
        SetStateCommand.__init__(self, _state)

    names = ['switch', 'sw']
    description = 'Switch to favorites and vice versa'
    argv = {}

    @SetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        if self.State.shuffle_is_on:
            print('Switch is unavailable when shuffle mode is on.')
            return
        elif self.State.cur_data_is_favorites:
            self.State.cur_data_is_favorites = False
            self.State.cur_data = self.State.all_data
            print('Switched to main list.')
        else:
            if not self.State.favorites.size:
                print('Error: favorites list is empty.')
                return
            self.State.cur_data_is_favorites = True
            self.State.cur_data = self.State.favorites
            self.State.start = 0
            self.State.finish = self.State.cur_data.shape[0]
            print('Switched to favorites.')

        self.State.start, self.State.start = self.State.start, self.State.start
        self.State.finish, self.State.finish = self.State.finish, self.State.finish
        self.State.length = self.State.finish - self.State.start
        self.State.reset_recent_words()
        self.State.words_to_remember = []
        self.State.reset_word_iter()

        if self.State.shuffle_is_on:
            self.State.cur_data = self.State.cur_data[
                np.random.choice(range(self.State.cur_data.shape[0]), self.State.cur_data.shape[0],
                                 replace=False)]
        return CommandExecutionCode.NO_ANSWER
