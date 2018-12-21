import requests
import json
import os
from tqdm import tqdm
from hazm import *

class ElasticUtils():

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.base_path = 'http://{}:{}/elasticbot'.format(server_ip, server_port)
        self.first_time = self.__setup_index()
        if self.first_time:
            self.__add_corpus()
        self.normalizer = Normalizer()

    def __add_corpus(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'persian_corpus.json'), 'r') as fh:
            corpus = json.load(fh)

        for i in range(len(corpus)):
            corpus[i]['exact_input'] = corpus[i]['input']
        
        print('Sending dialogues to elasticsearch ...')
        for corp in tqdm(corpus):
            r = requests.post(self.base_path + "/dialogue", json=corp)

    def __setup_index(self):
        body = {
        "settings": {
            "analysis": {
            "char_filter": {
                "zero_width_spaces": {
                    "type":       "mapping",
                    "mappings": [ "\\u200C=> "] 
                }
            },
            "filter": {
                "persian_stop": {
                "type":       "stop",
                "stopwords":  "_persian_" 
                }
            },
            "analyzer": {
                "rebuilt_persian": {
                "tokenizer":     "standard",
                "char_filter": [ "zero_width_spaces" ],
                "filter": [
                    "lowercase",
                    "decimal_digit",
                    "arabic_normalization",
                    "persian_normalization",
                    "persian_stop"
                ]
                }
            }
            }
        },
        "mappings": {
            "dialogue": {
                "properties": {
                    "input": {
                        "type":  "text" 
                    },
                    "output": {
                        "type":  "text" 
                    },
                    "exact_input": {
                        "type":  "keyword" 
                    },
                    "tag": {
                        "type":  "keyword" 
                    }
                }
            }
        }
        }

        r = requests.put(self.base_path, json=body)
        if 'resource_already_exists_exception' in r.text:
            print('Successfully set up the index')
            return False
        elif '"acknowledged":true' in r.text:
            print('Successfully set up the index')
            return True
        else:
            print('Encountered an error while seting up index: {}'.format(r.text))
            return None


    def respond(self, input_text, size=2):
        input_text = self.normalizer.normalize(input_text)
        r = requests.post(self.base_path + '/dialogue/_search', json={
            "query": {
            "bool": {
                "should": [
                {
                    "term" : {
                    "exact_input": {
                        "value": input_text,
                        "boost": 100
                    }
                    }
                },
                {
                    "multi_match" : {
                    "query" : input_text,
                    "fields": ["input^3", "output"],
                    # "fuzziness": 2
                    }
                }
                ]
            }
            },
            "size": size
        })

        max_score = json.loads(r.text)['hits']['max_score']
        hits = json.loads(r.text)['hits']['hits']
        if max_score:
            return hits[0]['_source']
        else:
             return None

    def learn(self, user_teach):
        user_teach['input'] = self.normalizer.normalize(user_teach['input'])
        user_teach['output'] = [self.normalizer.normalize(user_teach['output'])]
        user_teach['tag'] = 'user_teach'
        user_teach['exact_input'] = user_teach['input']
        requests.post(self.base_path + "/dialogue", json=user_teach)
