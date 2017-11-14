import datetime
import glob
import json
import os.path
import random

from command_runner import CommandRunner
import pandas as pd

from state import State
from dictionary import Dictionary
from dictionary import ResponseDataMap


random.seed(datetime.datetime.now().time())


class Lemys:
    def __init__(self):
        self.State = State()

        self.Dictionary = Dictionary()
        print('Remote dictionary: {link};'.format(link=self.Dictionary.website))

        self.__init_base_settings_file(self.State.base_settings_filename)
        self.__init_dict_settings_file(self.State.dict_settings_filename)

        # Commands:
        self.CommandRunner = CommandRunner(self.State, self.Dictionary)

    def __init_base_settings_file(self, settings_filename):
        if os.path.isfile(settings_filename):
            obj = json.load(open(settings_filename, 'r'))
            for ka, va in obj.items():
                exec('self.State.' + str(ka) + ' = \'' + str(va) + '\'')
            self.State.random_coef = float(self.State.random_coef)
            self.State.rem_coef = float(self.State.rem_coef)
        else:
            with open(settings_filename, 'w') as settings_file:
                settings_file.write(json.dumps({
                    "filename": self.State.filename,
                    "random_coef": self.State.random_coef,
                    "favorites_fn": self.State.favorites_fn,
                    "rem_coef": self.State.rem_coef}, indent=2))

    def __init_dict_settings_file(self, settings_filename):
        new_x_mashape_key = 'yhxwJ4lWl5mshKCB3Tlpn2RvTNC6p1dFiMojsnAwD0vcxDAKUg'
        if not os.path.isfile(settings_filename):
            obj = {}
            for key, val in ResponseDataMap.items():
                obj[key] = False
            obj['X-Mashape-Key'] = new_x_mashape_key
            obj['synonyms'] = True
            obj['definition'] = True
            obj['examples'] = True
            obj['partOfSpeech'] = True
            obj['typeOf'] = True

            with open(settings_filename, 'w') as settings_file:
                settings_file.write(json.dumps(obj, indent=2))
        else:
            # loading response entries from file
            obj = json.load(open(settings_filename, 'r'))

        new_response_entries = 0
        for ka, va in obj.items():
            if ka == 'X-Mashape-Key':
                new_x_mashape_key = va
            else:
                if va:
                    new_response_entries |= ResponseDataMap[ka]
        self.Dictionary.override_response_entries(new_response_entries)
        self.Dictionary.XMashapeKey = new_x_mashape_key

    def read_csv(self):
        if os.path.isfile(self.State.filename) and os.path.getsize(self.State.filename) > 0:
            self.State.input_df = pd.read_csv(self.State.filename, encoding='UTF-8-sig', header=None, dtype='str')
            self.State.all_data = self.State.input_df.values
            print('Reading from \'{filename}\'...'.format(filename=os.path.realpath(self.State.filename)))
        else:
            os.listdir(os.path.dirname(os.path.realpath(__file__)))  # setting current dir
            for file_csv in glob.glob('*.csv'):
                if file_csv != self.State.favorites_fn:
                    self.State.filename = file_csv
                    self.State.input_df = pd.read_csv(file_csv, encoding='UTF-8-sig', header=None, dtype='str')
                    self.State.all_data = self.State.input_df.values
                    print('Reading from \'{filename}\'...'.format(filename=self.State.filename))
                    return
            raise ValueError('File not exist or empty')

    def run(self):
        self.CommandRunner.init()
        self.CommandRunner.run()
