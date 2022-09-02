import numpy as np
import argparse as argp
import pickle
import re
import os
import sys

'''python3 generate.py model.pkl --prefix '' 4'''

class MyNgramsModel:
    def __int__(self):
        self.text = ''
        parser = argp.ArgumentParser()
        parser.add_argument('--input_dir', nargs='?', default='stdin')
        parser.add_argument('model', nargs='?')
        arg = parser.parse_args()
        self.model = arg.model

        if arg.input_dir != 'stdin':  # file input
            with open(arg.input_dir, 'r') as f:
                self.text = f.read()
        else:  # stdin
            self.text = input()

    def fit(self):
        # Convert to lowercases
        self.text = self.text.lower()

        # Replace all none alphanumeric characters with spaces
        self.text = re.sub(r'[^а-яА-Яa-zA-Z]', ' ', self.text)

        # Break sentence in the token, remove empty tokens
        self.text = [token for token in self.text.split(" ") if token != ""]
        self.count_word = {}
        for i in range(len(self.text)):
            if self.text[i] not in self.count_word:
                self.count_word[self.text[i]] = 1
            else:
               self.count_word[self.text[i]] += 1

        self.count_pair = {}
        for i in range(1, len(self.text)):
            if (self.text[i - 1], self.text[i]) not in self.count_pair:
                self.count_pair[(self.text[i - 1], self.text[i])] = 1
            else:
                self.count_pair[(self.text[i - 1], self.text[i])] += 1

        self.prob_word = {}
        for i in range(len(self.text)):
            if self.text[i] not in self.prob_word:
                self.prob_word[self.text[i]] = self.count_word[self.text[i]] / len(self.text)

        self.prob_pair = {}
        for i in self.count_pair.keys():
            # print(i[0])
            self.prob_pair[i] = self.count_pair[i] / self.count_word[i[0]]
        #print(self.prob_pair)
        # P(s[i]) = P(s[i]|s[i-1])
        # Пологаем, что s[0] у нас есть всегда (сид или задан)
        # P(s[i]|s[i-1]) = количество пар (s[i-1], s[i]) в тексте и делим на s[i-1]
        # выбираем  s[i] с самой большой вероятностью

    def generate(self, prefix='', length=1):
        if prefix == '':
            prefix = self.text[int(np.random.choice(len(self.text), 1))]
        print(prefix, end=' ')
        prefix = prefix.lower()
        # Replace all none alphanumeric characters with spaces
        prefix = re.sub(r'[^а-яА-Яa-zA-Z]', ' ', prefix)
        # Break sentence in the token, remove empty tokens
        prefix = [token for token in prefix.split(" ") if token != ""]
        prev = prefix[-1]
        for i in range(length):
            tmp_max_prob = 0.0
            for j in self.count_word.keys():
                if (j, prev) in self.prob_pair and self.prob_pair[(j, prev)] > tmp_max_prob:
                    tmp_max_prob = self.prob_pair[(j, prev)]
            may_word = []
            for j in self.count_word.keys():
                if (j, prev) in self.prob_pair and self.prob_pair[(j, prev)] == tmp_max_prob:
                    may_word.append(j)
            #print(len(may_word))
            word = ''
            if len(may_word) == 0:
                word = self.text[int(np.random.choice(len(self.text), 1))]
            else:
                word = may_word[int(np.random.choice(len(may_word), 1))]
            print(word, end=' ')
            prev = word

    def save_model(self):
        with open(self.model, 'wb') as out:
            pickle.dump(self, out)



    def debug(self):
        print(self.text)


def start():
    parser = argp.ArgumentParser()
    parser.add_argument('model', type=str)
    parser.add_argument('--prefix', type=str, default='Мы')
    parser.add_argument("length", type=int)
    arg = parser.parse_args()

    model_new = MyNgramsModel()
    with open(arg.model, 'rb') as f:
        model_new = pickle.load(f)
        model_new.generate(arg.prefix, arg.length)

start()