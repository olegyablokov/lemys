import numpy as np
import pandas as pd
import random


class State:
    def __init__(self):
        self.base_settings_filename = \
            'settings_base.json'

        self.dict_settings_filename = \
            'settings_dict.json'

        self.filename = \
            'Phrasebook - Phrasebook.csv'
        self.favorites_fn = \
            'favorites.csv'

        self.favorites = np.empty([0, 10])
        self.input_df = pd.DataFrame()
        self.all_data = np.empty([0, 10])

        self.recent_words_size = 0
        self.recent_words_cur_size = 0
        self.recent_words = np.full(0, '')

        self.right_ans_counter = [0, 0]  # first corresponds to English, second to Russian
        self.ans_counter = [0, 0]  # first corresponds to English, second to Russian

        self.words_to_remember = []
        self.rem_coef = 0.5  # if word rate is higher than this, it is placed in self.words_to_remember

        self.rate_history = []

        # current box == all_data[self.start:self.finish]
        self.length = 0  # self.length == self.finish - self.start
        self.start = 0
        self.finish = 0

        self.prev_word_iter = None
        self.cur_word_iter = 0

        self.random_coef = 0.4

        self.cur_data = []  # representation: [['Language1', 'Language2', 'Word in language1', 'Word in language2',
        # 'number of correct answers', 'number of answers', 'rate (if zero, word is known)',
        # 'number of correct answers in reverse mode', 'number of answers in reverse mode',
        # 'rate in reverse mode (if zero, word is known)']]

        self.reverse = False  # if true, translate Russian words into English
        self.rev = [3, 2] if self.reverse else [2, 3]
        self.shift = 3 if self.reverse else 0
        self.shuffle_is_on = False
        self.cur_data_is_favorites = False
        self.len_is_static = True

    def flush_recent_words(self, silent_mode=False):
        self.recent_words = np.full(self.recent_words.shape[0], '', dtype=self.all_data.dtype)
        self.recent_words_cur_size = 0
        if not silent_mode:
            print('Recent words box is flushed.')

    def reset_recent_words(self, new_recent_words_size=-1, silent_mode=False):
        if new_recent_words_size != -1:
            if new_recent_words_size > self.length:
                new_recent_words_size = self.length
                if not silent_mode:
                    print('Error: new size is too large. Setting it to {new_size}.'.format(
                        new_size=new_recent_words_size))
            elif self.recent_words_size < 0:
                new_recent_words_size = 0
                if not silent_mode:
                    print('Error: new size is too small. Setting it to {new_size}.'.format(
                        new_size=new_recent_words_size))
        else:
            new_recent_words_size = int(self.length / 4)

        if new_recent_words_size < self.recent_words_size:
            self.recent_words = self.recent_words[:new_recent_words_size]
        else:
            self.recent_words = np.append(self.recent_words, np.full(new_recent_words_size - self.recent_words_size, '',
                                                                     dtype=self.all_data.dtype))
        self.recent_words_cur_size = min(self.recent_words_cur_size, new_recent_words_size)
        self.recent_words_size = self.recent_words.shape[0]

    def reset_rate_history(self, silent_mode=False):
        self.right_ans_counter[1 if self.reverse else 0] = 0
        self.ans_counter[1 if self.reverse else 0] = 0
        if not silent_mode:
            print('History flushed.')

    def reset_word_iter(self):
        self.prev_word_iter = self.cur_word_iter
        while True:
            if random.random() > self.random_coef:
                i = random.randint(self.start, self.finish - 1)
            else:
                sum_rates = np.sum(self.cur_data[self.start:self.finish,
                                   6 + self.shift].astype('float'))
                if sum_rates == 0:
                    rate_norm = np.full(self.length, 1 / self.length)
                else:
                    rate_norm = self.cur_data[self.start:self.finish,
                                              6 + self.shift].astype('float') / sum_rates
                i = self.start + np.random.choice(self.length, p=rate_norm)
            self.cur_word_iter = i

            if not self.cur_data[self.cur_word_iter][self.rev[0]] in self.recent_words:
                break
