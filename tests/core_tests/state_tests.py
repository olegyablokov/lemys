import unittest
import numpy as np
import os

import lemys.state as st


class TestState(unittest.TestCase):
    def setUp(self):
        # State:
        self.m_State = st.State()
        self.m_State.all_data = np.array(
            [['English', 'Russian', 'meadow', 'луг', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'induce', 'вызывать', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'stamp', 'топать ногой', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'rib', 'ребро', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'utter', 'выговорить', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'sly', 'лукавый', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'loft', 'чердак', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'barley', 'ячмень', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'trod', 'тропинка', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'mane', 'грива', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'жеребёнок', 'foal', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'tumor', 'опухоль', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'pithy', 'содержательный', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'speculative', 'умозрительный', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'furrow', 'борозда', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'forlorn', 'покинутый', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'chiefly', 'главным образом', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'pang', 'острая боль', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'protrude', 'выступать', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'avert', 'предотвращать', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'awry', 'кривой', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'shrill', 'пронзительный', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'indecipherable', 'неразборчивый', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'impregnable', 'неприступный', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'indistinctly', 'невнятно', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'contemplate', 'созерцать', '0', '0', '1', '0', '0', '1'],
             ['English', 'Russian', 'chalk', 'мел', '0', '0', '1', '0', '0', '1']])

        self.m_State.cur_data = self.m_State.all_data

        self.m_State.recent_words_size = 5
        self.m_State.recent_words_cur_size = 3
        self.m_State.recent_words = np.asarray(['предотвращать', 'stamp', 'indecipherable', '', ''],
                                               dtype=self.m_State.all_data.dtype)

        self.m_State.start = 5
        self.m_State.finish = 15
        self.m_State.length = 10
        self.m_State.cur_word_iter = 8

    def tearDown(self):
        pass

    def test_reset_word_iter(self):
        for i in range(10):
            cur_iter = self.m_State.cur_word_iter

            self.m_State.reset_word_iter()
            self.assertEqual(self.m_State.prev_word_iter, cur_iter)

            self.assertGreaterEqual(self.m_State.cur_word_iter, self.m_State.start)
            self.assertLess(self.m_State.cur_word_iter, self.m_State.finish)

    def test_reset_recent_words_correctly(self):
        self.m_State.reset_recent_words(2, silent_mode=True)
        self.assertEqual(self.m_State.recent_words_size, 2)
        self.assertEqual(self.m_State.recent_words_cur_size, 2)
        self.assertTrue((self.m_State.recent_words == np.asarray(['предотвращать', 'stamp'],
                                                                 dtype=self.m_State.all_data.dtype)).all())

    def test_reset_recent_words_with_arg_more_than_length_of_chosen_word(self):
        self.m_State.reset_recent_words(100, silent_mode=True)
        self.assertEqual(self.m_State.recent_words_size, self.m_State.length)
        self.assertEqual(self.m_State.recent_words_cur_size, 3)
        self.assertTrue((self.m_State.recent_words == np.asarray(['предотвращать', 'stamp', 'indecipherable', '', '',
                                                                  '', '', '', '', ''],
                                                                 dtype=self.m_State.all_data.dtype)).all())


if __name__ == '__main__':
    unittest.main()
