from ..base_commands import SetStateCommand
from ..base_commands import CommandExecutionCode
import numpy as np
import random


class ChangeBox(SetStateCommand):
    def __init__(self, _state):
        SetStateCommand.__init__(self, _state)

    names = ['chgbox', 'cb']
    description = 'Change box'
    argv = {'': 'Change the word box randomly',
            '-l': 'Change start and length lines of word box (e.g. \'cb -l 10 20\' means set word box from 10th to '
                  '30th entries of the main word box).\n If shuffle is on, the arguments after \'-l\' are ignored and '
                  'the box is changed randomly',
            '-mls': 'Make the box length static',
            '-mld': 'Make the box length dynamic',
            '-rws': 'Change the size of recent words box (e.g. \'-rws 4\' means set the size of recent words box to 4)',
            '-remc': 'Change the remember coefficient (e.g. \'-rws 0.4\' means set the remember coefficient to 0.4)'}

    @SetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        if len(args) == 0:
            if self.State.shuffle_is_on:
                if not silent_mode:
                    print('Turn off shuffling to use this command.')
            else:
                self.State.start = random.randint(0, self.State.cur_data.shape[0] - self.State.length)
                self.State.finish = self.State.start + self.State.length
                self.State.reset_recent_words()
                self.State.words_to_remember = []
                self.State.reset_word_iter()
                if not silent_mode:
                    print('start = {start};\nfinish = {finish}.'.format(start=self.State.start,
                                                                        finish=self.State.finish))
        else:
            for args_local in args:
                if args_local[0] == '-l':
                    if self.State.shuffle_is_on:
                        if self.State.cur_data_is_favorites:
                            self.State.cur_data = self.State.favorites[
                                np.random.choice(range(self.State.cur_data.shape[0]), self.State.cur_data.shape[0],
                                                 replace=False)]
                        else:
                            self.State.cur_data = self.State.all_data[
                                np.random.choice(range(self.State.cur_data.shape[0]), self.State.cur_data.shape[0],
                                                 replace=False)]
                        if not silent_mode:
                            print('Box changed randomly.')
                    else:
                        self.State.start = int(args_local[1])
                        self.State.length = int(args_local[2])

                        if self.State.start < 0:
                            self.State.start = 0
                        if self.State.finish < 0:
                            self.State.finish = 0
                        if self.State.start >= self.State.finish:
                            self.State.finish = self.State.start + 1  # TODO: remake box changing verification
                        self.State.finish = self.State.start + self.State.length
                        if self.State.finish > self.State.cur_data.shape[0]:
                            self.State.finish = self.State.cur_data.shape[0]
                            self.State.length = self.State.finish - self.State.start
                        if not silent_mode:
                            print('Box changed.')
                    self.State.reset_rate_history(silent_mode=True)
                    self.State.reset_recent_words(silent_mode=True)
                    self.State.reset_word_iter()
                    self.State.words_to_remember = []
                elif args_local[0] == '-mls':
                    self.State.len_is_static = True
                    if not silent_mode:
                        print('Box length is now static.')
                elif args_local[0] == '-mld':
                    self.State.len_is_static = False
                    if not silent_mode:
                        print('Box length is now dynamic.')
                elif args_local[0] == '-rws':
                    self.State.reset_recent_words = args_local[1]
                elif args_local[0] == '-remc':
                    self.State.rem_coef = args_local[1]

        return CommandExecutionCode.NO_ANSWER
