from ..base_commands import SetStateCommand
from ..base_commands import CommandExecutionCode
import numpy as np


class RemoveWord(SetStateCommand):
    def __init__(self, _state):
        SetStateCommand.__init__(self, _state)

    names = ['-']
    description = 'Remove the current word from the word box'
    argv = {}

    @SetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        if self.State.shuffle_is_on:
            print('\'{word}\': Word removed from the box.'.format(word=self.State.cur_data[self.State.cur_word_iter]
                                                                                          [self.State.rev[0]]))
            if self.State.len_is_static:
                while True:
                    new_word = np.reshape(self.State.cur_data[np.random.randint(0, self.State.cur_data.shape[0])],
                                          (1, 10))
                    if new_word[0][self.State.rev[0]] not in self.State.cur_data[self.State.start:self.State.finish,
                                                                                 self.State.rev[0]]:
                        break
                if self.State.cur_word_iter < self.State.cur_data.shape[0]:
                    self.State.cur_data = np.concatenate(
                        (self.State.cur_data[:self.State.cur_word_iter], new_word,
                         self.State.cur_data[self.State.cur_word_iter + 1:]))
                else:
                    self.State.cur_data = np.concatenate((self.State.cur_data[:self.State.cur_word_iter], new_word))
                print('\'{word}\': Word added to the box.'.format(word=new_word[0][self.State.rev[0]]))
            else:
                if self.State.cur_word_iter < self.State.cur_data.shape[0]:
                    self.State.cur_data = np.concatenate((self.State.cur_data[:self.State.cur_word_iter],
                                                          self.State.cur_data[self.State.cur_word_iter + 1:]))
                else:
                    self.State.cur_data = np.concatenate((self.State.cur_data[:self.State.cur_word_iter]))
                self.State.length -= 1
                self.State.finish -= 1
        else:
            print('Removing words is available only when shuffle mode is on.')

        return CommandExecutionCode.NO_ANSWER
