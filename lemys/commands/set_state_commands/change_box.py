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
                  '30th entries of the main word box).\n If shuffle is on, this argument is invalid.',
            '-mls': 'Make the box length static',
            '-mld': 'Make the box length dynamic',
            '-rws': 'Change the size of recent words box (e.g. \'-rws 4\' means set the size of recent words box to 4)',
            '-remc': 'Change the remember coefficient (e.g. \'-rws 0.4\' means set the remember coefficient to 0.4)'}

    @SetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        if len(args) == 0:
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
                        if not silent_mode:
                            print('Turn off shuffling to use this command.')
                    else:
                        if len(args_local) != 3:
                            raise ValueError('Wrong number of arguments')
                        start = int(args_local[1])
                        length = int(args_local[2])
                        finish = start + length

                        if length <= 0:
                            raise ValueError('Length must be a non-zero positive integer')

                        if start < 0:
                            start = 0
                            if not silent_mode:
                                print('Start value is too small. Setting it to {val}'.format(val=start))

                        if finish >= self.State.cur_data.shape[0]:
                            finish = self.State.cur_data.shape[0]
                            length = finish - start
                            if not silent_mode:
                                print('Finish value is too large. Setting it to {val}'.format(val=finish))

                        if start >= self.State.cur_data.shape[0]:
                            start = self.State.cur_data.shape[0] - 1
                            finish = start + 1
                            length = 1
                            if not silent_mode:
                                print('Start value is too large. Setting it to {val}'.format(val=start))

                        self.State.start = start
                        self.State.length = length
                        self.State.finish = finish
                        if not silent_mode:
                            print('Box changed.')

                    self.State.reset_rate_history(silent_mode=True)
                    self.State.flush_recent_words(silent_mode=True)
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
                    self.State.reset_recent_words(int(args_local[1]))
                elif args_local[0] == '-remc':
                    self.State.rem_coef = args_local[1]

        return CommandExecutionCode.NO_ANSWER
