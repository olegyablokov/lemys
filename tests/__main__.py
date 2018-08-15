import sys, os
sys.path.append(sys.argv[0] + '/..')  # to include parent packages

import unittest

import lemys
from commands_tests.set_state_commands_tests import *
from commands_tests.get_state_commands_tests import *
from commands_tests.give_answer_commands_tests import *
from core_tests.state_tests import *

if __name__ == '__main__':
    unittest.main()
