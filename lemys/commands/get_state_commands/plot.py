from ..base_commands import GetStateCommand
from ..base_commands import CommandExecutionCode
import matplotlib.pyplot as plt


class Plot(GetStateCommand):
    def __init__(self, _state):
        GetStateCommand.__init__(self, _state)

    names = ['plot', 'pl']
    description = 'Plot your stats'
    argv = {}

    @GetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        plt.plot(self.State.rate_history)
        plt.show()
        return CommandExecutionCode.NO_ANSWER
