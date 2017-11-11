import unittest
import numpy as np

import lemys.state as st
import lemys.commands.set_state_commands.change_box as cb


class TestChangeBox(unittest.TestCase):
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

        self.m_State.start = 5
        self.m_State.finish = 15
        self.m_State.length = 10
        self.m_State.cur_word_iter = 8

        # ChangeBox:
        self.m_ChangeBox = cb.ChangeBox(self.m_State)

    def tearDown(self):
        pass

    def test_change_start_and_finish_correctly(self):
        self.m_ChangeBox.execute(['cb', '-l', '2', '7'], silent_mode=True)
        self.assertEqual(self.m_State.start, 2)
        self.assertEqual(self.m_State.finish, 9)
        self.assertEqual(self.m_State.length, 7)
        self.assertEqual(self.m_State.words_to_remember, [])
        self.assertEqual(self.m_State.recent_words_cur_size, 0)
        self.assertEqual(len(self.m_State.recent_words), self.m_State.recent_words_size)

        for word in self.m_State.recent_words:
            self.assertEqual(word, '')

        self.assertLess(self.m_State.recent_words_size, self.m_State.length)

        self.assertGreaterEqual(self.m_State.cur_word_iter, 2)
        self.assertLess(self.m_State.cur_word_iter, 9)

    def test_change_start_and_finish_with_no_integers(self):
        exception_thrown = False
        try:
            self.m_ChangeBox.execute(['cb', '-l', '2', '2ed'], silent_mode=True)
        except ValueError:
            exception_thrown = True
            self.assertEqual(self.m_State.start, 5)
            self.assertEqual(self.m_State.finish, 15)
            self.assertEqual(self.m_State.length, 10)

        self.assertTrue(exception_thrown)

    def test_change_start_and_finish_where_finish_too_big(self):
        self.m_ChangeBox.execute(['cb', '-l', '3', '1000'], silent_mode=True)

        self.assertEqual(self.m_State.start, 3)
        self.assertEqual(self.m_State.finish, self.m_State.cur_data.shape[0])
        self.assertEqual(self.m_State.length, self.m_State.finish - self.m_State.start)


class TestChangeBoxSmallMainWordBox(unittest.TestCase):
    def setUp(self):
        # State:
        self.m_State = st.State()
        self.m_State.all_data = np.array(
            [['English', 'Russian', 'meadow', 'луг', '0', '0', '1', '0', '0', '1']])

        self.m_State.cur_data = self.m_State.all_data

        self.m_State.start = 0
        self.m_State.finish = 1
        self.m_State.length = 1
        self.m_State.cur_word_iter = 0

        # ChangeBox:
        self.m_ChangeBox = cb.ChangeBox(self.m_State)

    def tearDown(self):
        pass

    def test_change_start_and_finish_where_finish_too_big(self):
        self.m_ChangeBox.execute(['cb', '-l', '0', '2'], silent_mode=True)

        self.assertEqual(self.m_State.start, 0)
        self.assertEqual(self.m_State.finish, self.m_State.cur_data.shape[0])
        self.assertEqual(self.m_State.length, self.m_State.finish - self.m_State.start)


if __name__ == '__main__':
    unittest.main()
