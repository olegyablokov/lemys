import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from enum import Enum
import os.path
import random


# execute() return code:
class CommandExecutionCode(Enum):
    REQUEST_FINISH = 0
    WORD_KNOWN = 1
    WORD_UNKNOWN = 2
    NO_ANSWER = 3
    COMMAND_NOT_IMPLEMENTED = 4

# abstract commands:


class Command(ABC):
    def __init__(self, _state):
        self.State = _state

    names = []  # '[<command name>]'
    description = ''  # Command description (usage)
    full_description = ''  # A long and full description
    argv = {}  # {'<-argument>': '<description>'}

    Dictionary = None

    @abstractmethod
    def execute(self, args, silent_mode=False):
        pass

    @staticmethod
    def set_dict(_dict):
        Command.Dictionary = _dict

    @staticmethod
    def init(_state):
        _state.length = min(_state.all_data.shape[0], 20)
        _state.start = random.randint(0, _state.all_data.shape[0] - _state.length)
        _state.finish = _state.start + _state.length
        _state.reset_recent_words()

        if _state.all_data.shape[1] == 4:
            temp1 = np.full((_state.all_data.shape[0], 2), '0', dtype='str')
            temp2 = np.full((_state.all_data.shape[0], 1), '1', dtype='str')
            _state.all_data = np.concatenate((_state.all_data, temp1, temp2, temp1, temp2), axis=1)

        # setting favorites:
        if os.path.isfile(_state.favorites_fn):  # file exists and not empty
            if os.path.getsize(_state.favorites_fn) > 0:
                fav_df = pd.read_csv(_state.favorites_fn, encoding='UTF-8', header=None, dtype='str')
                temp1 = np.full((fav_df.values.shape[0], 2), '0', dtype='str')
                temp2 = np.full((fav_df.values.shape[0], 1), '1', dtype='str')
                _state.favorites = np.concatenate((fav_df.values, temp1, temp2, temp1, temp2), axis=1)
            else:
                _state.favorites = np.empty([0, 10])
        else:
            with open(_state.favorites_fn, "w"):
                _state.favorites = np.empty([0, 10])

        _state.recent_words_size = int((_state.finish - _state.start) / 4)
        _state.recent_words = np.full(_state.recent_words_size, '', dtype=_state.all_data.dtype)

        _state.cur_data = _state.all_data

        print(('\nSize of the initial dictionary: {init_dict_size};\n'
               'Size of the chosen dictionary (word box): {word_box_size};\n'
               'You are learning now the words from {start} to {finish}.\n\n'
               'Type \'help\' for help.\n').format(
            init_dict_size=_state.cur_data.shape[0],
            word_box_size=_state.length,
            start=str(_state.start),
            finish=str(_state.finish)))

        _state.reset_word_iter()
        Command._update_data(_state)

    @staticmethod
    def _update_data(_state, silent_mode=False):
        if not _state.cur_data.shape[0]:
            if _state.cur_data_is_favorites:
                if not silent_mode:
                    print('Favorites list is empty. Switched to main list.')
                _state.cur_data = _state.all_data
                _state.start = 0
                _state.finish = 20
                _state.length = 20
                _state.cur_data_is_favorites = False

        chosen_word = _state.cur_data[_state.cur_word_iter][_state.rev[0]]
        if _state.favorites.size:
            if _state.cur_data[_state.cur_word_iter][_state.rev[0]] in _state.favorites:
                chosen_word += ' ★'
        if not silent_mode:
            print(chosen_word)

    @staticmethod
    def _check_args(self, args):
        if len(args) <= 1:
            return []

        new_args = []
        if args[1][0] != '-':
            raise ValueError('Parameters should begin with \'-\'')
        for i, arg in enumerate(args[1:]):
            if arg[0] == '-':
                if arg not in self.argv.keys():
                    raise ValueError('Wrong parameter <{param}>'.format(param=arg))
                # appending new args:
                new_args.append([arg])
                if i == len(args) - 2:
                    continue
                for sub_arg in args[i + 2:]:
                    if sub_arg[0] != '-':
                        new_args[-1].append(sub_arg)
                    else:
                        break
        return new_args


class GetStateCommand(Command):
    def __init__(self, _state):
        Command.__init__(self, _state)
        pass

    @abstractmethod
    def execute(self, args, silent_mode=False):
        pass

    @staticmethod
    def _execute_wrapper(fn):
        def wrapper(self, args, silent_mode=False):
            args = Command._check_args(self, args)
            ret = fn(self, args, silent_mode)
            if not silent_mode:
                input('Press enter to continue...')
            Command._update_data(self.State, silent_mode)
            return ret
        return wrapper


class SetStateCommand(Command):
    def __init__(self, _state):
        Command.__init__(self, _state)
        pass

    @abstractmethod
    def execute(self, args, silent_mode=False):
        pass

    @staticmethod
    def _execute_wrapper(fn):
        def wrapper(self, args, silent_mode=False):
            args = Command._check_args(self, args)
            ret = fn(self, args, silent_mode)
            Command._update_data(self.State, silent_mode)
            return ret
        return wrapper


class GiveAnswerCommand(Command):
    def __init__(self, _state):
        Command.__init__(self, _state)
        pass

    @abstractmethod
    def execute(self, args, silent_mode=False):
        pass

    @staticmethod
    def _execute_wrapper(fn):
        def wrapper(self, args, silent_mode=False):
            args = Command._check_args(self, args)
            ret = fn(self, args, silent_mode)

            self.State.cur_data[self.State.cur_word_iter][5 + self.State.shift] = \
                str(int(self.State.cur_data[self.State.cur_word_iter][5 + self.State.shift]) + 1)
            self.State.cur_data[self.State.cur_word_iter][6 + self.State.shift] = \
                str(1 - int(self.State.cur_data[self.State.cur_word_iter][4 + self.State.shift]) /
                    int(self.State.cur_data[self.State.cur_word_iter][5 + self.State.shift]))

            self.State.ans_counter[1 if self.State.reverse else 0] += 1

            # updating self.State.rate_history:
            rate = self.State.right_ans_counter[1 if self.State.reverse else 0] / self.State.ans_counter[
                1 if self.State.reverse else 0] * 100
            self.State.rate_history.append(rate)

            if not silent_mode:
                print('Translation: {translation};\nRate: {rate}% ({right_ans_counter} of {ans_counter} words known);'.
                      format(translation=self.State.cur_data[self.State.cur_word_iter][self.State.rev[1]],
                             rate=round(rate, 2),
                             right_ans_counter=self.State.right_ans_counter[1 if self.State.reverse else 0],
                             ans_counter=self.State.ans_counter[1 if self.State.reverse else 0]))

            # updating self.State.words_to_remember
            try:
                ind = self.State.words_to_remember.index(self.State.cur_data[self.State.cur_word_iter][self.State.rev[0]])
                if float(self.State.cur_data[self.State.cur_word_iter][6 + self.State.shift]) >= self.State.rem_coef:
                    pass
                else:
                    del self.State.words_to_remember[ind]
            except ValueError as e:
                if float(self.State.cur_data[self.State.cur_word_iter][6 + self.State.shift]) > self.State.rem_coef:
                    self.State.words_to_remember.append(self.State.cur_data[self.State.cur_word_iter]
                                                        [self.State.rev[0]])
                else:
                    pass

            # updating self.State.recent_words
            if self.State.recent_words_size:
                self.State.recent_words = np.roll(self.State.recent_words, 1)
                self.State.recent_words[0] = self.State.cur_data[self.State.cur_word_iter][self.State.rev[0]]
                self.State.recent_words_cur_size += 1
                if self.State.recent_words_cur_size == self.State.recent_words_size and \
                   self.State.recent_words_size == self.State.length:
                    self.State.reset_recent_words()
                    if not silent_mode:
                        print('All the words from the box have been encountered. Recent words box flushed.')

            self.State.reset_word_iter()
            Command._update_data(self.State, silent_mode)
            return ret
        return wrapper
