from .base_commands import Command
from .base_commands import CommandExecutionCode
from .base_commands import GetStateCommand
from .base_commands import SetStateCommand
from .base_commands import GiveAnswerCommand

from .set_state_commands.flush import Flush
from .set_state_commands.change_box import ChangeBox
from .get_state_commands.help import Help
from .get_state_commands.view_box import ViewBox
from .set_state_commands.switch import Switch
from .set_state_commands.add_to_favorites import AddToFavorites
from .get_state_commands.plot import Plot
from .set_state_commands.quit import Quit
from .set_state_commands.remove_from_favorites import RemoveFromFavorites
from .set_state_commands.remove_word import RemoveWord
from .set_state_commands.reverse_translation import ReverseTranslation
from .get_state_commands.sets import Sets
from .set_state_commands.shuffle import Shuffle
from .give_answer_commands.word_known import WordKnown
from .give_answer_commands.word_unknown import WordUnknown
from .get_state_commands.get_full_definition import GetFullDefinition


def get_commands():
    return [Help, Sets, Switch, Flush, Quit, ReverseTranslation,
            AddToFavorites, RemoveFromFavorites,
            Plot, Shuffle, RemoveWord, ViewBox, ChangeBox,
            WordKnown, WordUnknown, GetFullDefinition]
