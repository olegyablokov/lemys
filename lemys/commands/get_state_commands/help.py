from ..base_commands import GetStateCommand
from ..base_commands import CommandExecutionCode
from lemys import commands


class Help(GetStateCommand):
    def __init__(self, _state):
        GetStateCommand.__init__(self, _state)
        self.Commands = commands.get_commands()

        # setting self.argv
        for command in self.Commands:
            if command.names and command.description:
                parameters = ''
                if command.argv:
                    for arg, descr in command.argv.items():
                        if arg == '':
                            arg = '<no args>'
                        parameters += '{arg}: {descr};\n\t'.format(arg=arg, descr=descr)
                else:
                    parameters = '(No parameters used for this command)'
                names = ''
                for name in command.names:
                    names += '\'{name}\' or '.format(name=name)
                names = names[:-4]

                item = ''
                if names:
                    item += 'Command:\n\t{names};\n'.format(names=names)
                if command.description:
                    item += 'Description:\n\t{descr};\n'.format(descr=command.description)
                if command.full_description:
                    item += 'Full description:\n\t{full_description};\n'.format(
                        full_description=command.full_description)
                if parameters:
                    item += 'Parameters:\n\t{parameters}'.format(parameters=parameters)

                for name in command.names:
                    self.argv['-' + name] = item

    names = ['help']
    description = ''
    argv = {}

    @GetStateCommand._execute_wrapper
    def execute(self, args, silent_mode=False):
        if len(args) == 0:
            print('For detailed description, type \'help <-command>\'.\n')
            for command in self.Commands:
                if command.names and command.description:
                    names = ''
                    for name in command.names:
                        names += '\'{name}\' or '.format(name=name)
                    names = names[:-4]
                    print('{names}: {descr};'.format(names=names, descr=command.description))
            if not self.State.shuffle_is_on:
                print(('\nSize of initial dictionary: {init_dict_size}\n' +
                       'Size of chosen dictionary (word box): {word_box_size}\n').format(
                    init_dict_size=self.State.cur_data.shape[0],
                    word_box_size=self.State.length))
                print('You are learning now the words from {start} to {finish}.'.format(start=str(self.State.start),
                                                                                        finish=str(self.State.finish)))
        else:
            for args_local in args:
                print('\n{detailed_description}'.format(detailed_description=self.argv[args_local[0]]))
        return CommandExecutionCode.NO_ANSWER
