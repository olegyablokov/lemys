import unittest
import numpy as np
import os

import lemys.state as st
import lemys.commands.set_state_commands.remove_from_favorites as remove_from_favorites


class TestRemoveFromFavorites(unittest.TestCase):
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

        # creating favorites file:
        with open(self.m_State.favorites_fn, 'w') as f:
            f.write('English, Russian, meadow, луг, 0, 0, 1, 0, 0, 1')
            f.write('English, Russian, stir, размешивать, 0, 0, 1, 0, 0, 1')
            f.write('English, Russian, brittle, ломкий, 0, 0, 1, 0, 0, 1')

        # ChangeBox:
        self.m_RemoveFromFavorites = remove_from_favorites.RemoveFromFavorites(self.m_State)

    def tearDown(self):
        # deleting favorites file:
        os.remove(self.m_State.favorites_fn)

    def test_remove_favorite_translation_from_favorites(self):
        self.m_State.cur_word_iter = 0
        cur_translation = self.m_State.cur_data[0]
        self.m_RemoveFromFavorites.execute(['uf'], silent_mode=True)

        self.assertTrue(cur_translation not in self.m_State.favorites)

    def test_remove_non_favorite_translation_from_favorites(self):
        self.m_State.cur_word_iter = 1
        cur_translation = self.m_State.cur_data[1]
        self.m_RemoveFromFavorites.execute(['uf'], silent_mode=True)

        self.assertTrue(cur_translation not in self.m_State.favorites)


if __name__ == '__main__':
    unittest.main()
