import requests
import os
import json
from abc import ABC


ResponseDataMap = {'definition': 1 << 0,
                   'synonyms': 1 << 1,
                   'antonyms': 1 << 2,
                   'examples': 1 << 3,
                   'rhymes': 1 << 4,
                   'typeOf': 1 << 5,
                   'hasTypes': 1 << 6,
                   'partOf': 1 << 7,
                   'hasParts': 1 << 8,
                   'instanceOf': 1 << 9,
                   'hasInstances': 1 << 10,
                   'inRegion': 1 << 11,
                   'regionOf': 1 << 12,
                   'usageOf': 1 << 13,
                   'hasUsages': 1 << 14,
                   'memberOf': 1 << 15,
                   'hasMembers': 1 << 16,
                   'substanceOf': 1 << 17,
                   'hasSubstances': 1 << 18,
                   'hasAttribute': 1 << 19,
                   'inCategory': 1 << 20,
                   'hasCategories': 1 << 21,
                   'also': 1 << 22,
                   'pertainsTo': 1 << 23,
                   'similarTo': 1 << 24,
                   'entails': 1 << 25,
                   'partOfSpeech': 1 << 26}


class Dictionary(ABC):
    def __init__(self):
        self.Dir = 'dictionary'
        self.XMashapeKey = ''
        self.ResponseEntries = 0
        self.website = 'www.wordsapi.com'
        self.docs = 'www.wordsapi.com/docs'

        if not os.path.isdir(self.Dir):
            os.mkdir(self.Dir)

    def add_response_entries(self, entries):
        self.ResponseEntries |= entries

    def override_response_entries(self, entries):
        self.ResponseEntries = entries

    def remove_response_entries(self, entries):
        self.ResponseEntries &= ~entries

    def get_info(self, word):
        info = ''
        filename = '{dir}//{filename}.json'.format(dir=self.Dir, filename=word)

        # checking if word is already in local dictionary
        if not self.XMashapeKey:
            raise ValueError('X-Mashape-Key not set. It can be initialized by modifying the \'X-Mashape-Key\' entry in '
                             '\'settings_dict.json\' file or by deleting it and rerunning the program.')
        if not os.path.exists(filename):
            r = requests.get('https://wordsapiv1.p.mashape.com/words/' + word,
                             headers={
                                 "X-Mashape-Key": self.XMashapeKey,
                                 "Accept": "application/json"
                             }
                             )
            if r.status_code == 404:
                info += '{word}: Not found.'.format(word=word)
                return info
            with open(filename, 'wb') as f:
                f.write(r._content)

        # reading data
        with open(filename, 'rb') as f:
            data = json.load(f)
            if 'results' in data.keys():
                info += '____________________________________\n'
                print_new_line = False
                for result in data['results']:
                    for key in result.keys():
                        if key in ResponseDataMap.keys():
                            if ResponseDataMap[key] & self.ResponseEntries:
                                print_new_line = True
                                info += '{key}:\n'.format(key=key)
                                if isinstance(result[key], str):
                                    # i.e. if result[key] has only one entry
                                    info += '\t{item};\n'.format(item=result[key])
                                else:
                                    for item in result[key]:
                                        info += '\t{item};\n'.format(item=item)
                    if print_new_line:
                        info += '____________________________________\n'
                        print_new_line = False
            if 'pronunciation' in data.keys():
                info += 'Pronunciation: {val}\n'.format(val=data['pronunciation'])
            if 'frequency' in data.keys():
                info += 'Frequency (from 1 to 7): {val}\n'.format(val=data['frequency'])
        return info
